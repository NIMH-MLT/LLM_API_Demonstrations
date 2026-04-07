from openai import OpenAI
from ollama import chat
from ollama import ChatResponse

api='ollama'
#api='openAI'

# use for debugging only, very small model that can be installed with "ollama pull tinyllama"
#model='tinyllama'
# use for testing, should still run pretty quickly, and can be installed with "ollama pull qwen3.5:9b"
model='qwen3.5:9b'

## initialization

# client initializaton
if api == 'openAI':
    client = OpenAI(
        base_url="http://localhost:11434/v1/",
        api_key="ollama",  # required by the client, ignored by Ollama
        )
elif api == 'ollama':
    # no need
    pass
else:
    assert False

# initialize 'messages' to keep conversation history
# - messages is just a list, one entry per utterance
# - each entry is a dictionary with the 'role' (who is saying this) and the 'content' (what was said)
# - openAI initializes with a "system" message (e.g. what is the system supposed to be/do?)

messages = []

# initialization message
if api == 'openAI':
    messages.append({'role': 'system', 'content': 'You are a concise helpful assistant.'})
elif api == 'ollama':
    # no need
    pass
else:
    assert False

user_input = 'Why is the sky blue?'
messages.append({'role': 'user', 'content': user_input })
print('user says: %s' % user_input)

## first turn

# first call to the model goes with the initial message/prompt in 'messages'
if api == 'openAI':
    model_output = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        )
elif api == 'ollama':
    model_output = chat(
        model=model,
        messages=messages,
        )
else:
    assert False
    
# extract the response from the model output
# (it contains many other things)
if api == 'openAI':
    response = model_output.choices[0].message.content
elif api == 'ollama':
    response = (model_output['message'])['content']
else:
    assert False
    
print('assistant says: %s\n' % response)

## now go into a loop of prompt/response, always adding to the conversation history
## (exit by typing nothing, 'quit', or 'exit')

while True:
    user_input = input("user says: ").strip()
    if user_input.lower() in {'','quit', 'exit'}:
        break

    messages.append({'role': 'user', 'content': user_input})

    if api == 'openAI':
        model_output = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            )
    
        response = model_output.choices[0].message.content
    elif api == 'ollama':
        model_output = chat(model=model, messages=messages)
        
        response = (model_output['message'])['content']
    else:
        assert False
        
    print('assistant says: %s\n' % response)

    messages.append({"role": "assistant", "content": response})

    
## print the whole conversation

print('\nprintout of the entire conversation\n')
    
for idx,message in enumerate(messages):
    print('utterance %d:\t%s' % (idx,message['content']))
