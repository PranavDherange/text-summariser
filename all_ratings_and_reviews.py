import json
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ProxyError, RequestException
import re

# Function to extract integers from a string
def get_int(fetched_item):
    integer_fetched = ""
    for i in fetched_item:
        if i.isdigit():
            integer_fetched += i
    return integer_fetched

# Load movie_ids from file
with open('horror_movies.txt', 'r') as horrorlist:
    movie_ids = [line.strip() for line in horrorlist]

my_dict = {}
max_retries = 3  # Set the maximum number of retries per movie_id

for i in movie_ids:
    tconst_param = i
    url = f'https://www.imdb.com/title/{tconst_param}/reviews'

    for attempt in range(max_retries):
        try:
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                reviews_data = []

                # Find all the review containers
                review_elements = soup.find_all('div', class_='imdb-user-review')
                # Find all the rating elements
                review_rating_element_array = soup.find_all('span', string=re.compile("^\d+$"))

                # Iterate through both ratings and reviews simultaneously
                for review_rating_element, review_element in zip(review_rating_element_array, review_elements):
                    rating = int(get_int(review_rating_element.get_text(strip=True)))
                    review_text_element = review_element.find('div', class_='text show-more__control')

                    if review_text_element and rating:  # Only add to reviews_data if both review and rating exist
                        review = review_text_element.get_text(strip=True)

                        reviews_data.append({
                            'rating': rating,
                            'review': review
                        })
                my_dict[i] = reviews_data
                # if len(reviews_data) == 0:
                #     print(f"MY DICT IS {my_dict[i]}")


                if len(reviews_data) > 0:

                    with open('movies_ratings_reviews.json', 'w') as json_file:
                        json.dump(my_dict, json_file)
                    print(len(reviews_data))

            else:
                print(f"Failed to retrieve data for {i}. Status code: {response.status_code}")
            break  # Break out of retry loop if request was successful or there was a non-proxy related error

        except ProxyError:
            print(f"ProxyError occurred when fetching data for {i}. Attempt {attempt + 1}/{max_retries}")
        except RequestException as e:
            print(f"Error occurred when fetching data for {i}: {e}")
            break  # If it's not a proxy error, break out of retry loop to avoid unnecessary retries
