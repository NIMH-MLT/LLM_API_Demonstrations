import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

## This demo loads a model from the NIMH model repository on biowulf, and runs it on a given prompt

# local model to use
model_path = '/data/NIMH_ReadOnly/HF_models/models_gemma/gemma-4-12B-it'

## initialization

# load the tokenizer (handles text <-> token-id conversion AND chat-template formatting)
# and the model itself (weights loaded in bf16, placed on GPU if available)
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    dtype=torch.bfloat16,
    device_map='auto',
    )
model.eval()

# initialize 'messages' to keep conversation history
# - messages is just a list, one entry per utterance
# - each entry is a dictionary with the 'role' (who is saying this) and the 'content' (what was said)

messages = []

# initialization message - the "system prompt", broad instructions about the role/attitude of the LLM
# (this is not the prompt itself, and be skipped if desired)
system_prompt = 'You are a helpful assistant.'

messages.append({'role': 'system', 'content': system_prompt})

# prompt
prompt = 'Why is the sky blue?'
messages.append({'role': 'user', 'content': prompt})


# apply_chat_template formats the messages list into the model's expected
# prompt string and tokenizes it. With return_dict=True we get back a dict
# with input_ids and attention_mask, ready to pass to model.generate().
inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors='pt',
    return_dict=True,
).to(model.device)
input_len = inputs['input_ids'].shape[-1]

with torch.no_grad():
    output_ids = model.generate(
        **inputs,
        do_sample=True,
        max_new_tokens=1000000,
        temperature=0.7,
    )

# generate() returns the full sequence (prompt + completion), so slice off
# the prompt to get just the new tokens, then decode to text.
new_tokens = output_ids[0, input_len:]
response = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

print(response)
