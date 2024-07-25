import json
from collections import defaultdict
import statistics
import numpy as np
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ProxyError, RequestException
import re

def get_int(fetched_item):
    integer_fetched = ""
    for i in fetched_item:
        if i.isdigit():
            integer_fetched += i
    return integer_fetched
# Load JSON data from a file
with open('horror_reviews_data.json', 'r') as json_file:
    data_dict = json.load(json_file)
#https://www.imdb.com/title/tt0076361/reviews
#Get the number of keys

with open('movies_ratings_reviews_updated.json', 'r') as json_file:
    data_dict1 = json.load(json_file)
sum_rating = 0
number_keys = len(data_dict)
print(number_keys)
collection = 0
for movies_id in data_dict.keys():
    if movies_id in data_dict1.keys():
        for dictionary in data_dict1[movies_id]:
            sum_rating += dictionary["rating"]
            collection += 1

print(f"Total number collected is {collection}")
print(f"Avg horror movies rating as collected is {sum_rating/collection}")




