import deeplake
from transformers import AutoTokenizer, TrainingArguments, AutoModelForCausalLM
import torch
from torch import nn
from trl import SFTTrainer
from trl.trainer import ConstantLengthDataset
from peft import LoraConfig, TaskType

ds = deeplake.load('hub://genai360/FingGPT-sentiment-train-set')
ds_valid = deeplake.load('hub://genai360/FingGPT-sentiment-valid-set')


def prepare_sample_text(example):
    text = f"""{example['instruction'].text()}\n]nContent:
{example['input'].text()}\n\nSentiment: {example['output'].text()} """
    return text

tokenizer = AutoTokenizer.from_pretrained("facebook/opt-1.3b")

train_dataset = ConstantLengthDataset(
    tokenizer,
    ds,
    formatting_func=prepare_sample_text,
    infinite=True,
    seq_length=1024
)

eval_dataset = ConstantLengthDataset(
    tokenizer,
    ds_valid,
    formatting_func=prepare_sample_text,
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
    output_dir="./OPT-fine-tuned-FinGPT-CPU",
    dataloader_drop_last=True,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    num_train_epochs=10,
    logging_steps=5
    per_device_train_batch_size=12,
    per_device_eval_batch_size=12,
    learning_rate=1e-4,
    lr_scheduler_type="cosine",
    warmup_steps=100,
    gradient_accumulation_steps=1,
    gradient_checkpointing=False,
    fp16=False,
    bf16=True,
    weight_decay=0.05,
    ddp_find_unused_parameters=False,
    run_name="OPT-fine-tuned-FinGPT-CPU",
    report_to="wandb"
)

model = AutoModelForCausalLM.from_pretrained(
    "facebook/opt-1.3b", torch_dtype=torch.bfloat16)

for param in model.parameters():
    param.requires_grad = False
    if param.ndim == 1:
        param.data = param.data.to(torch.float32)

model.grad_checkpointing_enable()
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
    peft_config=lora_config,
    packing=True
)

model = PeftModel.from_pretrained(model, "finetuned-FinGPT-CPU")
model.eval()
model = model.merge_and_unload()
model.save_pretrained("finetuned-FinGPT-CPU/merged")

inputs = tokenizer("""What is the sentiment of this news? Please choose an answer from {strong negative/moderately negative/mildly negative/neutral/mildly positive/moderately positive/strong positive}, then provide some short reasons.\n\n
Content: UPDATE 1-AstraZeneca sells rare cancer drug to Sanofi for up to S300 mln.\n\nSentiment: """, return_tensors="pt").to("cuda:0")

generation_output = model.generate(**inputs,
                                    return_dict_in_generate=True,
                                    output_scores=True,
                                    max_length=256,
                                    num_beams=1,
                                    do_sample=True,
                                    repetition_penalty=1.5,
                                    length_penalty=2.)

print(tokenizer.decode(generation_output['sequences'][0]))


