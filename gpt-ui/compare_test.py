from transformers import BertTokenizer, BertModel
import torch

# Load the BioBERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained("monologg/biobert_v1.1_pubmed")
model = BertModel.from_pretrained("monologg/biobert_v1.1_pubmed")

term1 = "thick head"
term2 = "headache"
term3 = "cough"

# Tokenize and convert to embeddings
tokens1 = tokenizer(term1, return_tensors="pt")
tokens2 = tokenizer(term2, return_tensors="pt")
tokens3 = tokenizer(term3, return_tensors="pt")

# Obtain embeddings from BioBERT
embeddings1 = model(**tokens1).last_hidden_state.mean(dim=1)
embeddings2 = model(**tokens2).last_hidden_state.mean(dim=1)
embeddings3 = model(**tokens3).last_hidden_state.mean(dim=1)

# Calculate cosine similarity
similarity = torch.nn.functional.cosine_similarity(embeddings1, embeddings2)
print(f"Similarity between '{term1}' and '{term2}': {similarity.item()}")

similarity = torch.nn.functional.cosine_similarity(embeddings1, embeddings3)
print(f"Similarity between '{term1}' and '{term3}': {similarity.item()}")

similarity = torch.nn.functional.cosine_similarity(embeddings2, embeddings3)
print(f"Similarity between '{term2}' and '{term3}': {similarity.item()}")