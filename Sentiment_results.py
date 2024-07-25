import json
from collections import Counter

with open('/root/text_summariser/text-summariser/sentiment_analysis_results.json', 'r') as json_file:
    data_dict = json.load(json_file)




# Function to count matching sentiments
def count_matching_sentiments(movie_data):
    count = 0
    actual_sentiments = movie_data['actual_sentiment']
    for i in range(1, 11):
        if movie_data[str(i)] in actual_sentiments:
            count += 1
    return count

def max_counting_sentiments(movie_data):
    count = 0
    actual_sentiments = movie_data['actual_sentiment']
    sent_list = []
    for i in movie_data.keys():
        if i != "actual_sentiment":
            sent_list.append(movie_data[i])
    new_list = Counter(sent_list)
    return max(new_list), actual_sentiments

def see_sentiment(movie_data):
    count = 0
    actual_sentiments = movie_data['actual_sentiment']
    sent_set = set()
    for i in movie_data.keys():
        if i != "actual_sentiment":
            sent_set.add(movie_data[i])
    return sent_set, set(actual_sentiments)
total_count = 0
match_count = 0
see_count = 0
# Loop over movies and count matching sentiments
for movie_id, movie_data in data_dict.items():
    for review in movie_data.keys():
        total_count += 1
        # match_count = count_matching_sentiments(movie_data[review])
        see_list,true_sentiment = see_sentiment(movie_data[review])
        if true_sentiment.issubset(see_list) or see_list.issubset(true_sentiment):
            see_count += 1
        #print(f"For movie {movie_id}, the max count is {max_count} and actual sentiment is {true_sentiment}")
print(f"Total count is {total_count}")
print(f"Match count is {see_count}")
# accuracy = match_count/total_count
# print(f"Crude Percentage is {accuracy}")