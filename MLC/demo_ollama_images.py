from ollama import chat
import json
import re
import sys
import base64


## Ollama provides its own API, which is similar but not the same as the OpenAI one.


## It starts with a single turn of conversation, so that the function calls are clear.
## It then proceeds to a chatbot-like loop, to show how that is implemented:
## - at every turn, the whole conversation thus far is sent to the LLM
## - at the end of the turn, the new utterances have to be added into the conversation history

api='ollama'

# if running in your mac, this is faster
#model='gemma4:12b-mlx'

# if running on GPUs, this is the right one
model='gemma4:12b'


## load images used in the demo 

# single image, for description
#with open("the_great_wave.jpeg","rb") as ifd:
#    image_data = ifd.read()
#image_wave = base64.b64encode(image_data).decode('utf-8')

# multiple images, for comparisons
#with open("bonsai.jpg","rb") as ifd:
#    image_data = ifd.read()
#image_bonsai = base64.b64encode(image_data).decode('utf-8')

#
# example 1: describe a single image
#

response = chat(
    model=model,
    messages=[{
        'role': 'user',
        'content': 'Describe the contents of the image in no more than one paragraph',
        # Pass paths to both images in the list
        'images': [
            './bonsai.jpg',
        ],
    }]
)

print('\nExample 1: description of the image\n===================================================\n')
print((response['message'])['content'])

#
# example 2: process three images and make an odd-one-out decision
#

response = chat(
    model=model,
    messages=[{
        'role': 'user',
        'content': 'Describe the contents of the three images attached, and decide which one is the odd one out',
        # Pass paths to both images in the list
        'images': [
            './bonsai.jpg',
            './truck.jpg',
            './tricycle.jpg'
        ],
    }]
)

print('\nExample 2: description of the 3 images\n===================================================\n')
print((response['message'])['content'])

#
# example 3: process three images and make an odd-one-out decision, in a structured way
#

#class response_OOO:
#    odd_one_out: str
#    odd_one_out_justification: str
#    odd_one_out_confidence: str


response = chat(
    model=model,
    format='json',
    messages=[{
        'role': 'user',
        'content': '''The three images attached, images[0], images[1], and images[2] each illustrate an instance of one particular thing. Look at all three and decide which one is the odd one out, reasoning as necessary. You will output a JSON dictionary looking like this
{
    \"odd_one_out\": can take values 0, 1, or 2, to indicate one of the three images,
    \"justification\": containing all the text in your reasoning,
}
Do not output anything else besides the JSON dictionary''',
        # Pass paths to both images in the list
        'images': [
            './bonsai.jpg',
            './truck.jpg',
            './tricycle.jpg'
        ],
    }]
)

print('\nExample3: odd one out output\n===================================================\n')

## convert the answer to a dictionary

answer_txt  = (response['message'])['content']
print(answer_txt)

# minimal processing to remove the ```json <stuff> ``` failure mode, if it happened
# (should no longer be needed)
answer_txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", answer_txt.strip())

try:
    answer_dict = json.loads(answer_txt)
    print('\ndictionary output:\n')
    print('- odd-one-out   - %s' % answer_dict['odd_one_out'])
    print('- justification - %s' % answer_dict['justification'])
except:
    print('Consider putting this in a loop until it succeeds')
    assert False


#
# example 4: same as example 3, but pre-load and based 64 encode all images
#

# convert the image to base64 text
with open("./bonsai.jpg","rb") as ifd:
    image_data = ifd.read()
image_base64_bonsai = base64.b64encode(image_data).decode('utf-8')

# convert the image to base64 text
with open("./truck.jpg","rb") as ifd:
    image_data = ifd.read()
image_base64_truck = base64.b64encode(image_data).decode('utf-8')

# convert the image to base64 text
with open("tricycle.jpg","rb") as ifd:
    image_data = ifd.read()
image_base64_tricycle = base64.b64encode(image_data).decode('utf-8')

input_images = [image_base64_bonsai,image_base64_truck,image_base64_tricycle]


response = chat(
    model=model,
    format='json',
    messages=[{
        'role': 'user',
        'content': '''The three images attached, images[0], images[1], and images[2] each illustrate an instance of one particular thing. Look at all three and decide which one is the odd one out, reasoning as necessary. You will output a JSON dictionary looking like this
{
    \"odd_one_out\": can take values 0, 1, or 2, to indicate one of the three images,
    \"justification\": containing all the text in your reasoning,
}
Do not output anything else besides the JSON dictionary''',
        # Pass paths to both images in the list
        'images': input_images,
    }]
)

print('\nExample 4: odd one out output\n===================================================\n')

## convert the answer to a dictionary

answer_txt  = (response['message'])['content']
print(answer_txt)

# minimal processing to remove the ```json <stuff> ``` failure mode, if it happened
# (should no longer be needed)
answer_txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", answer_txt.strip())

try:
    answer_dict = json.loads(answer_txt)
    print('\ndictionary output:\n')
    print('- odd-one-out   - %s' % answer_dict['odd_one_out'])
    print('- justification - %s' % answer_dict['justification'])
except:
    print('Consider putting this in a loop until it succeeds')
    assert False


