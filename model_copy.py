# import torch
# from transformers import RobertaTokenizer, RobertaForSequenceClassification, Trainer, TrainingArguments
import json

# Load RoBERTa tokenizer and model
# tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
# model = RobertaForSequenceClassification.from_pretrained("roberta-base")

# Sample data (replace with your own)
with open('/root/text_summariser/text-summariser/horror_movies_ratings_reviews_updated.json', 'r') as json_file:
    data_dict = json.load(json_file)
print(len(data_dict))
reviews = []
ratings = []

for movie_id, elements in list(data_dict.items()):
    for element in elements:
        reviews.append(element["review"])
        ratings.append(element["rating"])

label_map = {
    1: ["bad"],
    2: ["bad"],
    3: ["bad"],
    4: ["bad", "neutral"],
    5: ["bad", "neutral"],
    6: ["neutral"],
    7: ["neutral", "good"],
    8: ["neutral", "good"],
    9: ["good"],
    10: ["good"]
}

def convert_to_multilabel(rating, label_map):
    labels = label_map[rating]
    return [int("bad" in labels), int("neutral" in labels), int("good" in labels)]

multilabels = [convert_to_multilabel(r, label_map) for r in ratings]

#filtered_data = [(multilabel, review, rating) for multilabel, review, rating in zip(multilabels, reviews, ratings) if multilabel != [0,1,1]]

# Split filtered data back to individual lists
# multilabels, reviews, ratings = zip(*filtered_data)
tuple_labels = [tuple(label) for label in multilabels]
# Count each unique tuple
multi_dict = {}
for label in tuple_labels:
    if label not in multi_dict:
        multi_dict[label] = 0
    multi_dict[label] += 1

print(f"Count of all the metrics are {multi_dict}")
print(len(reviews))



# Tokenize the data
# inputs = tokenizer(reviews, padding=True, truncation=True, return_tensors="pt")
# input_ids = inputs["input_ids"]
# attention_mask = inputs["attention_mask"]

# # Convert labels to tensor
# labels = torch.tensor(labels)

# # TrainingArguments and Trainer classes handle training details and procedures
# training_args = TrainingArguments(
#     per_device_train_batch_size=8,
#     num_train_epochs=3,
#     logging_dir="./logs",
# )

# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=(input_ids, attention_mask, labels),
# )

# trainer.train()

# # After training, you can save the model
# model.save_pretrained("./sentiment_roberta")
# tokenizer.save_pretrained("./sentiment_roberta")
