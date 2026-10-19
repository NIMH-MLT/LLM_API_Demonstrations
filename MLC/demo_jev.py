import os
import requests

#
# This code applies the three types of supported questions to a single input.
#
# - goes to openrouter.ai (the API provided by Typesafe is a bit different)
# - verify=False (to get around the NIH cert issues on the NIH network or VPN, otherwise download cert)
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

response = requests.post(
    "https://openrouter.ai/api/alpha/decisions",
    headers={
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
    },
    verify=False,
    json={
        "model": "typesafe/jev-1.13",
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
