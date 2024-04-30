

from transformers import BertTokenizer, BertModel
import torch
import spacy
# Check if GPU is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(f"divice",device)
# Try initializing spaCy and BERT again
try:
    nlp = spacy.load("en_core_web_sm")
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased').to(device)
    print("spaCy and BERT are initialized successfully!")
except Exception as e:
    print("An error occurred:", e)