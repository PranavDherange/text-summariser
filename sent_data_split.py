import json
from sklearn.model_selection import train_test_split
import os

# Load the data
with open('sentiment/testing_data.json', 'r') as f:
    data_dict = json.load(f)

# Flatten the data to a list of samples
all_samples = []
for movie_id, elements in data_dict.items():
    for element in elements:
        all_samples.append({
            "movie_id": movie_id,
            "rating": element["rating"],
            "review": element["review"]
        })

# Split the data into training and testing sets (80% - 20%)
train_samples, test_samples = train_test_split(all_samples, test_size=0.2, random_state=42)

# Split the training data into 10 equal parts
num_parts = 10
train_subsets = []
split_size = len(train_samples) // num_parts

for i in range(num_parts):
    start_idx = i * split_size
    end_idx = (i + 1) * split_size if i != num_parts - 1 else None  # To handle any leftover samples in the last subset
    train_subsets.append(train_samples[start_idx:end_idx])

# Save each training subset and the test set as separate JSON files
for idx, subset in enumerate(train_subsets, 1):
    dir_path = f'sentiment/model_{idx}'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    print(f"Currently preparing dataset_no.{idx}")
    with open(f'{dir_path}/training_subset_{idx}.json', 'w') as f:
        json.dump(subset, f, indent=4)

#Cretaing the whole training data set
with open(f'sentiment/training_whole.json', 'w') as f:
    json.dump(train_samples, f, indent=4)

#Creating the testing data set
with open(f'sentiment/testing_data.json', 'w') as f:
    json.dump(test_samples, f, indent=4)



    {
        movie_id:
            {
                1: "good"
                2: "good"
                3:
                ....
                actual: "good"
                count: "good bad"
            }
    }