import re
import torch
from spellchecker import SpellChecker
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def average_amount_of_typos(text):
    spell = SpellChecker()

    # Remove punctuation signs from the text
    text_cleaned = re.sub(r'[^\w\s]', '', text)

    # Split the cleaned text into words and identify misspelled ones
    words = text_cleaned.split()
    misspelled = spell.unknown(words)
    typo_count = len(misspelled)

    # Calculate the average count of typos per word
    word_count = len(words)
    average_typos = typo_count / word_count if word_count > 0 else 0

    return average_typos

def get_perplexity(text):

    # Load pre-trained GPT-2 model and tokenizer
    model_id = "gpt2-large"
    tokenizer = GPT2Tokenizer.from_pretrained(model_id)
    model = GPT2LMHeadModel.from_pretrained(model_id)
    model.eval()

    # Tokenize the text
    tokenized_text = tokenizer.encode(text, return_tensors='pt')

    # Calculate perplexity using GPT-2
    with torch.no_grad():
      outputs = model(tokenized_text, labels=tokenized_text)
      loss = outputs.loss
      perplexity = torch.exp(loss)

    return perplexity

# Detect typos
def check_if_text_is_ai_generated(text):

    amount_of_typos = average_amount_of_typos(text)
    
    perplexity = get_perplexity(text)

    if amount_of_typos > 0.05 or perplexity > 50:
      print("text written by human")
    else:
      print("text is ai generated")

check_if_text_is_ai_generated("the quick brown fox jumps over the lazy dog")
check_if_text_is_ai_generated("This text was written by human please believe me")
