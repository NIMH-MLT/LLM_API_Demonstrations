from ollama import chat
from ollama import ChatResponse

# use for debugging only, very small model that can be installed with "ollama pull tinyllama"
model='tinyllama'
# use for testing, should still run pretty quickly, and can be installed with "ollama pull qwen3.5:9b"
#model='qwen3.5:9b'

## initialization

# initialize 'messages' to keep conversation history
# - messages is just a list, one entry per utterance
# - each entry is a dictionary with the 'role' (who is saying this) and the 'content' (what was said)
messages = []
user_input = 'Why is the sky blue?'
messages.append({'role': 'user', 'content': user_input })
print('user says: %s' % user_input)

## first turn

# first call to the model goes with the initial message/prompt in 'messages'
model_output = chat(model=model, messages=messages)

# extract the response from the model output
# (it contains many other things)
response = (model_output['message'])['content']
print('assistant says: %s\n' % response)

## now go into a loop of prompt/response, always adding to the conversation history
## (exit by typing nothing, 'quit', or 'exit')

while True:
    user_input = input("user says: ").strip()
    if user_input.lower() in {'','quit', 'exit'}:
        break

    messages.append({'role': 'user', 'content': user_input})

    model_output = chat(
        model=model,
        messages=messages
    )

    response = (model_output['message'])['content']
    print('assistant says: %s\n' % response)

    messages.append({"role": "assistant", "content": response})

    
## print the whole conversation

print('\nprintout of the entire conversation\n')
    
for idx,message in enumerate(messages):
    print('utterance %d:\t%s' % (idx,message['content']))
