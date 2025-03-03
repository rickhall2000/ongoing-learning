from transformers import AutoModelForCausalLM, BitsAndBytesConfig
import torch 

model = AutoModelForCausalLM.from_pretrained(
    model_name_or_path='/name/or/path/to/model',
    load_in_4bit=True,
    device_map='auto',
    torch_dtype=torch.bfloat16,
    quantization_config=BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type='nf4'
    ),
)

