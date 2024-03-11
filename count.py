import json
from collections import defaultdict
import statistics
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


# Load the pretrained model and tokenizer
model_path = "/root/text_summariser/text-summariser/sentiment_roberta"  # Path to where the pretrained model and tokenizer are saved
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

def word_count(string):
    count = 0
    string=string.strip()
    for i in range(len(string)-1):
        if string[i]==" " and string[i+1] !=" ":
            count += 1
    return count + 1


# Load JSON data from a file
with open('all_movies_ratings_reviews_for_training.json', 'r') as json_file:
    data_dict = json.load(json_file)
#https://www.imdb.com/title/tt0076361/reviews
#Get the number of keys
sum_len = 0
calc_arr = []
rating_dict = defaultdict(int)
rating_count = defaultdict(int)
rating_set = set()
length = 0
for movie_id,array in data_dict.items():
    if len(array)>0:
        sum_len += len(array)
        calc_arr.append(len(array))
        length += 1
        for rating in array:
            # When tokenizing, add the truncation=True argument
            inputs = tokenizer(rating["review"], return_tensors="pt", truncation=True, max_length=512)


            rating_dict[rating["rating"]] += 1
            rating_set.add(rating["rating"])

for movie_id,array in data_dict.items():
    rating_count[len(array)]+=1

print(f"Sum of reviews is {sum_len}")
num_keys = len(data_dict)
print(f"Maximum number of reviews is {max(calc_arr)}")
# Print the number of keys
print("Number of keys:", length)
print(f"All ratings distibution is {rating_dict}")
print(f"All the ratings are {rating_set}")
print(f"Avg no of ratings is {sum_len/length}")
avg = 0
summ = 0
no =0
std_array = []
tr =0
for rating,number in rating_dict.items():
    if rating in range(1,11):
        tr += number
        summ += rating*number
        no += number
        for i in range(number):
           std_array.append(rating)
std_array.sort()
print(len(std_array))
print(f"First interval's max value is {std_array[len(std_array)//3]}")
print(len(std_array)//3)
print(f"Second interval's max value is {std_array[2*len(std_array)//3]}")
std_dev = statistics.stdev(std_array)

print(f"Avg rating is {summ/no}")
print(f"Std deviation of data is {std_dev}")

print(f"68% of data points are in range {summ/no - std_dev} and {summ/no + std_dev}")

quantile1 = np.percentile(std_array, 33)
quantile2 = np.percentile(std_array, 66)

print(f"33rd Percentile: {quantile1}")
print(f"66th Percentile: {quantile2}")

# Now you can divide your dataset based on these quantiles
interval1 = [x for x in std_array if x <= quantile1]
interval2 = [x for x in std_array if quantile1 < x <= quantile2]
interval3 = [x for x in std_array if x > quantile2]

print(f"Length of Interval 1 (1-{quantile1}): {len(interval1)}")
print(f"Length of Interval 2 ({quantile1+1}-{quantile2}): {len(interval2)}")
print(f"Length of Interval 3 ({quantile2+1}-10): {len(interval3)}")

print(f"Total number of corrected reviews {tr}")

print(f"Total ratings count us {rating_count}")

rat_arr = []
for num_rev,movies in rating_count.items():
    if num_rev > 0:
        for i in range(movies):
            rat_arr.append(num_rev)

quan1 = np.percentile(rat_arr, 33)
quan2 = np.percentile(rat_arr, 50)

print(f"33rd Percentile: {quan1}")
print(f"50th Percentile: {quan2}")

# Now you can divide your dataset based on these quantiles
inter1 = [x for x in std_array if x <= quan1]
inter2 = [x for x in std_array if quan1 < x <= quan2]
inter3 = [x for x in std_array if x > quan2]
