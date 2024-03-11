import json
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re

# Function to extract integers from a string
def get_int(fetched_item):
    integer_fetched = ""
    for i in fetched_item:
        if i.isdigit():
            integer_fetched += i
    return integer_fetched

async def fetch_reviews(session, movie_id):
    url = f'https://www.imdb.com/title/{movie_id}/reviews'
    try:
        async with session.get(url) as response:
            if response.status == 200:
                text = await response.text()
                return text
            else:
                print(f"Failed to retrieve data for {movie_id}. Status code: {response.status}")
    except Exception as e:
        print(f"Error occurred when fetching data for {movie_id}: {e}")
    return None

async def process_movie_ids(movie_ids, my_dict):
    rate_limit = 5  # Adjust this based on your needs
    semaphore = asyncio.Semaphore(rate_limit)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for movie_id in movie_ids:
            task = asyncio.ensure_future(process_movie_id(semaphore, session, movie_id, my_dict))
            tasks.append(task)
        return await asyncio.gather(*tasks)

async def process_movie_id(semaphore, session, movie_id, my_dict):
    async with semaphore:
        print(f"Processing movie ID: {movie_id}") 
        response_text = await fetch_reviews(session, movie_id)
        if response_text:
            soup = BeautifulSoup(response_text, 'html.parser')
            reviews_data = []

            # Find all the review containers
            review_elements = soup.find_all('div', class_='imdb-user-review')
            # Find all the rating elements
            review_rating_element_array = soup.find_all('span', string=re.compile("^\d+$"))

            # Iterate through both ratings and reviews simultaneously
            for review_rating_element, review_element in zip(review_rating_element_array, review_elements):
                rating = int(get_int(review_rating_element.get_text(strip=True)))
                review_text_element = review_element.find('div', class_='text show-more__control')

                if review_text_element and rating:
                    review = review_text_element.get_text(strip=True)
                    reviews_data.append({
                        'rating': rating,
                        'review': review
                    })
            my_dict[movie_id] = reviews_data

# Load movie_ids from file
with open('/root/text_summariser/text-summariser/horror_movies.txt', 'r') as horrorlist:
    movie_ids = [line.strip() for line in horrorlist]

# Initialize the dictionary to hold the data
my_dict = {}

# Run the async functions
loop = asyncio.get_event_loop()
loop.run_until_complete(process_movie_ids(movie_ids, my_dict))

# Save to JSON (or any further processing)
with open('data.json', 'w') as json_file:
    json.dump(my_dict, json_file)

# Calculate the number of movies with zero ratings
no_length_count = sum(1 for reviews in my_dict.values() if len(reviews) == 0)
print(f"Total number of movies with zero ratings: {no_length_count}")
