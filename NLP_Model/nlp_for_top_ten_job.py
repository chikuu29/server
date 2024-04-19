# Importing necessary libraries
from transformers import BertTokenizer, BertModel
import spacy
from findcsv import *




from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

import torch

# Try initializing spaCy and BERT again
try:
    nlp = spacy.load("en_core_web_sm")
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    print("spaCy and BERT are initialized successfully!")
except Exception as e:
    print("An error occurred:", e)




# Load data
# resumes_df= pd.read_csv('../csv/resumes.csv')
csv_file = 'resumes.csv'
key = 'Filename'
value='Sophia_Bell_CV.docx'
resumes_df = find_document(csv_file, key, value)
job_postings_df = pd.read_csv('../csv/job_postings.csv')

# print(f"resumes_dfs",resumes_dfs)
# print(f"resumesss",resumes_df)

# Fill NaN with empty strings
resumes_df.fillna('', inplace=True)
job_postings_df.fillna('', inplace=True)

# Combine all text columns into one for each DataFrame
# resumes_df['combined'] = resumes_df.apply(lambda row: ' '.join(row), axis=1)
# job_postings_df['combined'] = job_postings_df.apply(lambda row: ' '.join(row), axis=1)


# # Function to calculate similarities and return top 10 matches
# def get_top_matches(df1, df2, top_n=10):
#     # Use TfidfVectorizer to transform texts into TF-IDF vectors
#     vectorizer = TfidfVectorizer()
#     vec1 = vectorizer.fit_transform(df1['combined'])
#     vec2 = vectorizer.transform(df2['combined'])

#     # Calculate cosine similarity between each resume and job posting
#     similarity_matrix = cosine_similarity(vec1, vec2)

#     # Create a DataFrame to store matches
#     match_df = pd.DataFrame(similarity_matrix, index=df1['Filename'], columns=df2['Filename'])

#     # Get top 10 matches for each document
#     top_matches = {}
#     for index, row in match_df.iterrows():
#         sorted_row = row.sort_values(ascending=False)[:top_n]
#         top_matches[index] = sorted_row.index.tolist()
#     return top_matches

# # Get top 10 job postings for each resume and vice versa
# top_resumes_for_jobs = get_top_matches(job_postings_df, resumes_df)
# top_jobs_for_resumes = get_top_matches(resumes_df, job_postings_df)

# # Print example outputs
# print("Top 10 job postings for each resume:")
# print(top_jobs_for_resumes)

# print("\nTop 10 resumes for each job posting:")
# print(top_resumes_for_jobs)



#Best To Ten Match  

# # Function to get BERT embeddings
def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(1)
    return embeddings

# # Function to calculate cosine similarity
def calculate_similarity(embedding1, embedding2):
    return cosine_similarity(embedding1, embedding2)

# # Process job postings and resumes
job_postings_df['embeddings'] = job_postings_df['Project Description'].apply(lambda x: get_bert_embeddings(x))
resumes_df['embeddings'] = resumes_df['Work Experience'].apply(lambda x: get_bert_embeddings(x))

# # Calculate similarity and rank results
# results = []
# for _, job in job_postings_df.iterrows():
#     for _, resume in resumes_df.iterrows():
#         similarity_score = calculate_similarity(job['embeddings'], resume['embeddings'])[0][0]
#         results.append({
#             'Job Title': job['Project Title'],
#             'Resume': resume['Filename'],
#             'Similarity Score': similarity_score
#         })

# # Convert results to DataFrame and sort by similarity
# results_df = pd.DataFrame(results)
# results_df = results_df.sort_values(by='Similarity Score', ascending=False)

# # Print results in a formatted manner
# print("Top Matching Results:")
# print(results_df.head(10).to_string(index=False))




# need to work hear


from collections import Counter
import re

# Function to extract keywords from text
def extract_keywords(text):
    # Tokenize text into words
    words = re.findall(r'\b\w+\b', text.lower())
    # Count word frequencies
    word_freq = Counter(words)
    # Return top 10 most common words
    return [word for word, _ in word_freq.most_common(10)]

# # Initialize dictionary to store top resumes for each job along with keywords
# top_resumes_with_keywords_for_job = {job['Project Title']: [] for _, job in job_postings_df.iterrows()}

# # Calculate similarity and rank results
# for _, job in job_postings_df.iterrows():
#     for _, resume in resumes_df.iterrows():
#         similarity_score = calculate_similarity(job['embeddings'], resume['embeddings'])[0][0]
#         keywords = extract_keywords(resume['Work Experience'])  # Extract keywords from resume
#         top_resumes_with_keywords_for_job[job['Project Title']].append({
#             'Resume': resume['Filename'],
#             'Similarity Score': similarity_score,
#             'Keywords': keywords
#         })

# # Display top resumes for each job along with keywords
# for job_title, top_resumes_info in top_resumes_with_keywords_for_job.items():
#     print(f"Top 10 Resumes for {job_title}:")
#     top_resumes_info_sorted = sorted(top_resumes_info, key=lambda x: x['Similarity Score'], reverse=True)[:10]
#     for idx, resume_info in enumerate(top_resumes_info_sorted, start=1):
#         print(f"{idx}. Resume: {resume_info['Resume']} - Similarity Score: {resume_info['Similarity Score']}")
#         print("   Keywords:", ", ".join(resume_info['Keywords']))
#     print()

# Initialize dictionary to store top jobs for each resume along with keywords
top_jobs_with_keywords_for_resume = {resume['Filename']: [] for _, resume in resumes_df.iterrows()}

# Calculate similarity and rank results
for _, resume in resumes_df.iterrows():
    for _, job in job_postings_df.iterrows():
        similarity_score = calculate_similarity(job['embeddings'], resume['embeddings'])[0][0]
        keywords = extract_keywords(job['Project Description'])  # Extract keywords from job description
        top_jobs_with_keywords_for_resume[resume['Filename']].append({
            'Job Title': job['Project Title'],
            'Similarity Score': similarity_score,
            'Keywords': keywords
        })

# Display top jobs for each resume along with keywords
for resume_filename, top_jobs_info in top_jobs_with_keywords_for_resume.items():
    print(f"Top 10 Jobs for {resume_filename}:")
    top_jobs_info_sorted = sorted(top_jobs_info, key=lambda x: x['Similarity Score'], reverse=True)[:10]
    for idx, job_info in enumerate(top_jobs_info_sorted, start=1):
        print(f"{idx}. Job Title: {job_info['Job Title']} - Similarity Score: {job_info['Similarity Score']}")
        print("   Keywords:", ", ".join(job_info['Keywords']))
    print()



