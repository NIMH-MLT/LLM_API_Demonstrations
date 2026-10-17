import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

## This demo loads a model from the NIMH model repository on biowulf, and sets up a chat
##
## The conversation pattern is identical:
## - at every turn, the whole conversation thus far is sent to the LLM
## - at the end of the turn, the new utterances have to be added into the conversation history
## The only thing that changes is the inference call (a network API call -> model.generate()).

# point at the local model folder
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

# initialization message - the "system prompt"
system_prompt = 'You are a helpful assistant.'
#system_prompt = 'You are a very unhelpful assistant.'

messages.append({'role': 'system', 'content': system_prompt})

# start with a sample question
user_input = 'Why is the sky blue?'
messages.append({'role': 'user', 'content': user_input})
print('user says: %s' % user_input)


def generate_reply(messages):
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
            max_new_tokens=256,
            do_sample=True,
            temperature=0.7,
            )

    # generate() returns the full sequence (prompt + completion), so slice off
    # the prompt to get just the new tokens, then decode to text.
    new_tokens = output_ids[0, input_len:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


## first turn

response = generate_reply(messages)
print('assistant says: %s\n' % response)
messages.append({'role': 'assistant', 'content': response})

## now go into a loop of prompt/response, always adding to the conversation history
## (exit by typing nothing, 'quit', or 'exit')

while True:
    user_input = input("user says: ").strip()
    if user_input.lower() in {'', 'quit', 'exit'}:
        break

    messages.append({'role': 'user', 'content': user_input})

    response = generate_reply(messages)

    print('assistant says: %s\n' % response)

    messages.append({"role": "assistant", "content": response})


## print the whole conversation

print('\nprintout of the entire conversation\n')

for idx, message in enumerate(messages):
    print('utterance %d:\t%s' % (idx, message['content']))
