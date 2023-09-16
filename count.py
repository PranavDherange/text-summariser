import json
from collections import defaultdict
import statistics

# Load JSON data from a file
with open('movies_ratings_reviews.json', 'r') as json_file:
    data_dict = json.load(json_file)
#https://www.imdb.com/title/tt0076361/reviews
#Get the number of keys
sum_len = 0
calc_arr = []
rating_dict = defaultdict(int)
rating_set = set()

for movie_id,array in data_dict.items():
    if len(array)>0:
        sum_len += len(array)
        calc_arr.append(len(array))
        for rating in array:
            rating_dict[rating["rating"]] += 1
            rating_set.add(rating["rating"])
            if rating["rating"] in [900, 10166794, 4242, 851222, 2222, 6325, 78, 90, 245, 636, 15231]:
                print(movie_id)
#print(data_dict["tt10003008"])
# for movie_id,array in data_dict.items():
#     if len(array)> 15:
#         for rating in array:
            # rating_dict[rating["rating"]] += 1
            # rating_set.add(rating["rating"])
            # if rating["rating"] not in [900, 10166794, 4242, 851222, 2222, 6325, 78, 90, 245, 636, 15231]:
            #     print(movie_id)


print(f"Sum of reviews is {sum_len}")
num_keys = len(data_dict)
print(f"Minimum number of reviews is {max(calc_arr)}")
# Print the number of keys
print("Number of keys:", num_keys)
print(f"All ratings distibution is {rating_dict}")
print(f"All the ratings are {rating_set}")
print(f"Avg no of ratings is {sum_len/num_keys}")
avg = 0
summ = 0
no =0
for rating,number in rating_dict.items():
    if rating in range(1,11):
        summ += rating*number
        no += number
std_arr = rating_dict.values()
print(type(std_arr))
std_dev = statistics.stdev(std_arr)
print(f"Avg rating is {summ/no}")
print(f"Std deviation of data is {std_dev}")



