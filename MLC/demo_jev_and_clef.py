import os
import requests
import base64
import sys

#
# This code applies the three types of supported questions to a single input.
# It uses the requests library, which works for both OpenRouter and Ollama.
#
# To run this, you need an openrouter API key stored in the environment variable OPENROUTER_API_KEY.
#
# details of the JSON input:
#
# - "model": the version of Jev being accessed is denoted through the model name
# - "state": this contains the input as structured dictionary, *all* of which is ingested. It could be a single field named "input", if you prefer.
# - "questions": the questions to be asked
#   1) "noul" query - yes or no, probability of yes
#   2) "choice" query - probability over each of several options
#   3) score query - produce a score in an ordered scale of levels (min 2, max 10), described in text
#     (each level is assigned value 0, 1, #options-1)
#     (the score is a probability weighted average of the values)
#

## arguments to switch between jev and other models

#model = "typesafe/jev-1.13"
model = "clef-flash"
#model = "clef"

# where to route the request depends on the model
if model == "typesafe/jev-1.13":
    # openrouter
    url = "https://openrouter.ai/api/alpha/decisions"
    # get the key to be used
    headers={
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
    }
    verify=False
else:
    # local Ollama
    url = "http://localhost:11434/v1/systemone"
    headers={
        "Content-Type": "application/json",
    }
    verify=True
# end of model-dependent parameters

#
# send request
#
    
response = requests.post(
    url,
    headers=headers,
    verify=verify,
    json={
        "model": model,
        "state": {
            "customer_tier": "enterprise",
            "ticket": "My checkout page shows a blank screen after I click Pay. I have tried two browsers.",
        },
        "questions": {
            "is_bug": {
                "type": "noul",
                "instructions": "Is the customer reporting a software defect?",
                "criteria": {
                    "true": "The customer describes broken or unexpected product behavior.",
                    "false": "The customer is asking a question or requesting a feature.",
                },
            },
            "team": {
                "type": "choice",
                "instructions": "Which team should own this ticket?",
                "criteria": {
                    "payments": "Checkout, billing, or payment processing issues.",
                    "frontend": "Rendering, layout, or browser compatibility issues.",
                    "account": "Login, permissions, or profile issues.",
                },
            },
            "urgency": {
                "type": "score",
                "instructions": "How urgent is this ticket?",
                "criteria": [
                    "Can wait for the next release",
                    "Should be fixed this week",
                    "Blocking revenue right now",
                ],
            },
        },
    },
)

## pull out the three different responses

answers = response.json()["answers"]

# 1) "noul" query - yes or no, probability of yes

question = "Is the customer reporting a software defect?"
probability = (answers["is_bug"])["noul"]
print("\n1) noul: probability for \"%s\": %1.2f" % (question,probability))

# 2) "choice" query - probability over each of several options

# which option has highest probability
choice = (answers["team"])["choice"]
# how confident is the model [0,1]
confidence = (answers["team"])["confidence"]
# what are the probabilities for each option
probability_distribution = (answers["team"])["probabilities"]

print("\n2) choice: the answer is %s with confidence %1.2f" % (choice,confidence))
print("probability distribution (sorted high to low):")
for option in sorted(probability_distribution, key=probability_distribution.get, reverse=True):
    probability = probability_distribution[option]
    print("- %1.2f\t%s" % (probability,option))


# 3) score query - produce a score in an ordered scale of levels (min 2, max 10)
# (each level is assigned value 0, 1, #options-1, the score is a probability weighted average of them)

# what is the score
score = (answers["urgency"])["score"]
# how confident is the model [0,1]
confidence = (answers["urgency"])["confidence"]

print("\n3) score: the score is %1.2f with confidence %1.2f" % (score,confidence))

# what are the probabilities for each option
probability_distribution = (answers["urgency"])["probabilities"]

n_levels= len(probability_distribution)

# mapping from values to the levels provided in the query
print("mapping from values to levels, with probabilities")
map_value_to_level = (answers["urgency"])["legend"]
for level in range(0,n_levels):
    level_txt = "%d" % (level)
    probability = probability_distribution[level_txt]
    value = map_value_to_level[level_txt]
    print("%d\t(%1.2f):\t%s" % (level,probability,value))

#
# bonus: image search
#

if model == "typesafe/jev-1.13":
    print("\nJev does not support image inputs, exiting.")
    sys.exit(0)

    
# convert the image to base64 text
with open("the_great_wave.jpeg","rb") as ifd:
    image_data = ifd.read()
image_base64 = base64.b64encode(image_data).decode('utf-8')


response = requests.post(
    url,
    headers=headers,
    verify=verify,
    json={
        "model": model,
        "state": "Please answer questions about the attached image",
        "images": [image_base64],
        "questions": {
            "contains_wave": {
                "type": "noul",
                "instructions": "Does the image contain at least one wave?",
                "criteria": {
                    "true": "There is at least one wave in the image.",
                    "false": "The image contains no waves.",
                },
            },
            "contains_panda": {
                "type": "noul",
                "instructions": "Does the image contain at least one panda?",
                "criteria": {
                    "true": "There is at least one panda in the image.",
                    "false": "The image contains no pandas.",
                },
            },
        },
    },
)

## pull out the responses

print("\nanswers for the image")

answers = response.json()["answers"]

# 1) "noul" query - yes or no, probability of yes

question = "Does the image contain at least one wave?"
probability = (answers["contains_wave"])["noul"]
print("\nnoul: probability for \"%s\": %1.2f" % (question,probability))

question = "Does the image contain at least one panda?"
probability = (answers["contains_panda"])["noul"]
print("\nnoul: probability for \"%s\": %1.2f" % (question,probability))

