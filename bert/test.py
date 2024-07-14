from datasets import load_dataset
from transformers import AutoTokenizer

dataset = load_dataset("yelp_review_full")
def tokenize_function(examples):
    tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-cased")
    return tokenizer(examples["text"], padding="max_length", truncation=True)
tokenized_datasets = dataset.map(tokenize_function, batched=True)
