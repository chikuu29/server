

from transformers import BertTokenizer, BertModel

import spacy


# Try initializing spaCy and BERT again
try:
    nlp = spacy.load("en_core_web_sm")
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    print("spaCy and BERT are initialized successfully!")
except Exception as e:
    print("An error occurred:", e)