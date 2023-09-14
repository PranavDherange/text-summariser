import json
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ProxyError, RequestException

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
                reviews = []
                review_elements = soup.find_all('div', class_='text show-more__control')
                for review_element in review_elements:
                    review_text = review_element.get_text(strip=True)
                    reviews.append(review_text)
                my_dict[i] = reviews
                if len(reviews) > 0:
                    with open('horror_reviews_data.json', 'w') as json_file:
                        json.dump(my_dict, json_file)
                    print(len(reviews))
            else:
                print(f"Failed to retrieve data for {i}. Status code: {response.status_code}")
            break  # Break out of retry loop if request was successful or there was a non-proxy related error

        except ProxyError:
            print(f"ProxyError occurred when fetching data for {i}. Attempt {attempt + 1}/{max_retries}")
        except RequestException as e:
            print(f"Error occurred when fetching data for {i}: {e}")
            break  # If it's not a proxy error, break out of retry loop to avoid unnecessary retries