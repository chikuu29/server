import os
from transformers import BertTokenizer, BertModel
from NLP_Model.loadModel import *
import spacy
# from findcsv import *

from NLP_Model.findcsv import find_document
import torch

current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate up one directory to reach the project root
project_dir = os.path.dirname(current_dir)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

from collections import Counter
import re

# # Try initializing spaCy and BERT again
# try:
#     nlp = spacy.load("en_core_web_sm")
#     tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
#     model = BertModel.from_pretrained('bert-base-uncased')
#     print("spaCy and BERT are initialized successfully!")
# except Exception as e:
#     print("An error occurred:", e)


# Function to get BERT embeddings
def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(1)
    return embeddings

# # Function to calculate cosine similarity
def calculate_similarity(embedding1, embedding2):
    return cosine_similarity(embedding1, embedding2)


# Function to extract keywords from text
def extract_keywords(text):
    # Tokenize text into words
    words = re.findall(r'\b\w+\b', text.lower())
    # Count word frequencies
    word_freq = Counter(words)
    # Return top 10 most common words
    return [word for word, _ in word_freq.most_common(10)]



def findtoptenresumeforjob(job_id):

    csv_file = 'job.csv'
    key = 'job_id'
    value=job_id
    job_postings_df = find_document(csv_file, key, value)
    # job_postings_df = pd.read_csv('../csv/job.csv')  
    path =os.path.join(project_dir, 'csv_files','resume.csv')
    resumes_df = pd.read_csv(path)  
   
    if len(job_postings_df) == 0:
        return {"success":False,"message":"Job Not Found"}
    

    resumes_df.fillna('', inplace=True)
    job_postings_df.fillna('', inplace=True)

    job_postings_df['embeddings'] = job_postings_df['project_description'].apply(lambda x: get_bert_embeddings(x))
    resumes_df['embeddings'] = resumes_df['work_experience'].apply(lambda x: get_bert_embeddings(x))


    # # Initialize dictionary to store top jobs for each resume along with keywords
    # top_jobs_with_keywords_for_resume = {resume['resume_id']: [] for _, resume in resumes_df.iterrows()}

    # # Calculate similarity and rank results
    # for _, resume in resumes_df.iterrows():
    #     for _, job in job_postings_df.iterrows():
    #         similarity_score = calculate_similarity(job['embeddings'], resume['embeddings'])[0][0]
    #         keywords = extract_keywords(job['project_description'])  # Extract keywords from job description
    #         top_jobs_with_keywords_for_resume[resume['resume_id']].append({
    #             'job_id':job['job_id'],
    #             'Job_Title': job['project_title'],
    #             'similarity_score': similarity_score,
    #             'keywords': keywords
    #         })


    # # Display top jobs for each resume along with keywords
    # for resume_filename, top_jobs_info in top_jobs_with_keywords_for_resume.items():
    #     # top_jobs_info_sorted = sorted(top_jobs_info, key=lambda x: x.get('Similarity Score', 0), reverse=True)[:10]
    # #    print(f"Top 10 Jobs for {resume_filename}:")
    #    topTenData=[]
    #    top_jobs_info_sorted = sorted(top_jobs_info, key=lambda x: x['similarity_score'], reverse=True)[:10]
    #    for idx, job_info in enumerate(top_jobs_info_sorted, start=1):
    #        topTenData.append(job_info)
      
      # # Initialize dictionary to store top resumes for each job along with keywords
    top_resumes_with_keywords_for_job = {job['project_title']: [] for _, job in job_postings_df.iterrows()}

        # Calculate similarity and rank results
    for _, job in job_postings_df.iterrows():
            for _, resume in resumes_df.iterrows():
                similarity_score = calculate_similarity(job['embeddings'], resume['embeddings'])[0][0]
                keywords = extract_keywords(resume['work_experience'])  # Extract keywords from resume
                top_resumes_with_keywords_for_job[job['project_title']].append({
                    'resume_id': resume['resume_id'],
                    'similarity_score': similarity_score,
                    'keywords': keywords
                })

        # Display top resumes for each job along with keywords
    for job_title, top_resumes_info in top_resumes_with_keywords_for_job.items():
            # print(f"Top 10 Resumes for {job_title}:")
            top_resumes_info_sorted = sorted(top_resumes_info, key=lambda x: x['similarity_score'], reverse=True)[:10]
            topTenData=[]
            for idx, resume_info in enumerate(top_resumes_info_sorted, start=1):
                topTenData.append(resume_info)
                # print(f"{idx}. Resume: {resume_info['Resume']} - Similarity Score: {resume_info['Similarity Score']}")
                # print("   Keywords:", ", ".join(resume_info['Keywords']))
            # print()


    return {"success":True,"message":"NLP Succesfully Run","result":topTenData}


# findmatch=findtoptenresumeforjob("76b11919-f8e8-4fcf-9744-4fd55e7dd31b")


# print(findmatch)


