import deeplake
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from trl import SFTTrainer
from trl.trainer import ConstantLengthDataset
from peft import LoraConfig, PeftModel
import torch
import torch.nn as nn

# Connect to the training and testing datasets
ds = deeplake.load('hub://genai360/GAIR-lima-train-set')
ds_test = deeplake.load('hub://genai360/GAIR-lima-test-set')

tokenizer = AutoTokenizer.from_pretrained("facebook/opt-1.3b")

def prepare_sample_text(example):
    """Prepare the text from a sample of the database"""
    text = f"""Question: {example['question'].text()}\n\nAnswer: {example['answer'].text()}"""
    return text

train_dataset = ConstantLengthDataset(
    tokenizer,
    ds,
    formatting_func=prepare_sample_text,
    infinte=True,
    seq_length=1024
)

eval_dataset = ConstantLengthDataset(
    tokenizer,
    ds_test,
    formatting_func=prepare_sample_text,
    infinte=True,
    seq_length=1024
)

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

training_args = TrainingArguments(
    output_dir="./OPT-fine_tuned-LIMA-CPU",
    dataloader_drop_last=True,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    num_train_epochs=10,
    logging_steps=5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    learning_rate=1e-4,
    lr_scheduler_type="cosine",
    warmup_steps=10,
    gradient_accumulation_steps=1,
    bf16=True,
    weight_decay=0.05,
    run_name="OPT-fine_tuned-LIMA-CPU",
    report_to="wandb"
)

model = AutoModelForCausalLM.from_pretrained("facebook/opt-1.3b", torch_dytpe=torch.bfloat16)

for param in model.parameters():
    param.requires_grad = False
    if param.ndim == 1:
        param.data = param.data..to(torch.float32)
        
model.gradient_checkpointing_enable()
model.enable_input_require_grads()

class CastOutputToFloat(nn.Sequential):
    def forward(self, x):
        return super().forward(x).to(torch.float32)
model.lm_head = CastOutputToFloat(model.lm_head)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    peft_config=lora_config,
    packing=True
)

def print_trainable_parameters(model):
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
            
    print(f"""trainable params: {trainable_params} || all params: {all_param} || trainable%: {100 * trainable_params / all_param:.2f}%""")
    
trainer.train()

model = PeftModel.from_pretained(
    model,
    "./OPT-fine_tuned-LIMA-CPU",
)
model.eval()

model = model.merge_and_unload()
model.save_pretrained("./OPT-fine_tuned-LIMA-CPU/merged")

inputs = tokenizer("Question: Write a recipe with chicken.\n\nAnswer:", return_tensors="pt")

generation_output = model.generate(**inputs,
                                   return_dict_in_generate=True,
                                   output_scores=True,
                                   max_length=256,
                                   num_beams=1,
                                   do_sample=True,
                                   repitition_penalty=1.5,
                                   length_penalty=2.)

print(tokenizer.decode(generation_output.sequences[0]))

