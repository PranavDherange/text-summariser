import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification, Trainer, TrainingArguments
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import json

# Load data
with open('/root/text_summariser/text-summariser/horror_movies_ratings_reviews_updated.json', 'r') as json_file:
    data_dict = json.load(json_file)

reviews = []
ratings = []

for movie_id, elements in list(data_dict.items())[:1500]:
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

# Dataset class
class ReviewDataset(Dataset):
    def __init__(self, reviews, multilabels, tokenizer, max_length=256):
        self.reviews = reviews
        self.multilabels = multilabels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.reviews)

    def __getitem__(self, idx):
        review = self.reviews[idx]
        label = self.multilabels[idx]
        encoding = self.tokenizer.encode_plus(
            review,
            add_special_tokens=True,
            max_length=self.max_length,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.float)
        }


# Load RoBERTa tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("DataMonke/distilbert-base-uncased-sentiment-analysis-movie-reviews")
model = AutoModelForSequenceClassification.from_pretrained("DataMonke/distilbert-base-uncased-sentiment-analysis-movie-reviews", num_labels=3, ignore_mismatched_sizes=True)

def custom_compute_loss(p, batch):
    logits = p.logits
    labels = batch['labels']
    loss_fct = nn.BCEWithLogitsLoss()
    return loss_fct(logits, labels)
# Create dataset and data loader
dataset = ReviewDataset(reviews=reviews, multilabels=multilabels, tokenizer=tokenizer)
#train_loader = DataLoader(dataset, batch_size=8, shuffle=True)

class CustomTrainer(Trainer):

    def compute_loss(self, model, inputs, return_outputs=False):
        """
        Compute the loss using BCEWithLogitsLoss
        """
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits
        loss_fct = nn.BCEWithLogitsLoss()
        loss = loss_fct(logits, labels)
        return (loss, outputs) if return_outputs else loss

# Now, instead of using the Trainer class, you'll use CustomTrainer:



# Training setup
training_args = TrainingArguments(
    per_device_train_batch_size=8,
    num_train_epochs=3,
    logging_dir="./logs",
    output_dir="./output"
)

trainer = CustomTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=dataset,
#     compute_loss=custom_compute_loss
# )

# Train
trainer.train()

# Save model and tokenizer
model.save_pretrained("./sentiment_roberta")
tokenizer.save_pretrained("./sentiment_roberta")

# Test function
def test_model(model, test_reviews, tokenizer):
    test_inputs = tokenizer(test_reviews, padding=True, truncation=True, return_tensors="pt")
    model.eval()
    with torch.no_grad():
        outputs = model(**test_inputs)
        logits = outputs.logits
        probabilities = torch.sigmoid(logits)
        print(f"Proabailities are {probabilities}")
        predictions = (probabilities > 0.5).int()
        return predictions

# Test
test_reviews = test_reviews = ["This was originally a super-serial, composed of feature-length episodes, and like Feuillade's LES VAMPIRES, was meant to play not only as a serial, but as a series. However, the only remaining copy of this is a cut-down of all six episodes, about an hour and a quarter in length, held by the George Eastman House and available at the moment for viewing on their website. My thanks to them for making this and several dozen other movies of the Teens and early Twenties more generally available.While the are some great technical strengths to the movie, including some wonderful photography (notice the strong use of framing not by irising, as was still very common at this time, but by using structure and set decoration to change the effective frame size) and toning (a process in which the black silver nitrate is replaced by other compounds with colors, resulting in white whites, black blacks but colors instead of grays) and a good story which asks the question: is the soul born with the body, or the gift of god? Unfortunately, I find the style of acting to be rather over the top, involving a lot of rolling eyes. The net effect is very watchable, but not great.", "A man who was manufactured in a laboratory is tormented by his inability to feel love and so embarks on a reign of evil. Originally a hugely popular 6-part serial from Germany, Homunculus existed only as this 69-minute film, sections of which are severely degraded. As each episode of the original series was an hour long, this version provides only a fraction of it's story, and clearly suffers as a result. Danish actor Olaf Fonss overacts terribly even for a film this old, and although Homunculus is clearly a tormented figure haunted by his origins, it's impossible to feel any kind of sympathy for him. A new 200-minute version which will undoubtedly provide more depth and clarity has now been pieced together from fragments found in various archives", 'Great film.\nI am not one for silent films but this captures the imagination enough to hold attention.\nthe visual effects are nice. I like the spectral images.\nvery cool piece of work.','I hate this movie']
predicted_labels = test_model(model, test_reviews, tokenizer)
for review, label_set in zip(test_reviews, predicted_labels):
    sentiment = []
    if label_set[0] == 1:
        sentiment.append('bad')
    if label_set[1] == 1:
        sentiment.append('neutral')
    if label_set[2] == 1:
        sentiment.append('good')
    print(f"Review: {review}\nPredicted Sentiment: {', '.join(sentiment)}\n{'-'*50}")












