import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def word_count(string):
    count = 0
    string=string.strip()
    for i in range(len(string)-1):
        if string[i]==" " and string[i+1] !=" ":
            count += 1
    return count + 1

with open('all_movies_ratings_reviews_updated_new.json', 'r') as json_file:
    data_dict = json.load(json_file)

count = 0

for movie_id, array in data_dict.items():
    new_array = []
    for rating in array:
        if word_count(rating["review"]) <= 150:
            count += 1
        else:
            new_array.append(rating)  # keep this rating

    data_dict[movie_id] = new_array

print(f"COUNT IS {count}")

with open('all_movies_ratings_reviews_for_training.json', 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)

print("the work is done!")
