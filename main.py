from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from typing import List
from app.search.embeddings import get_corpus_embeddings
from app.search.search import semantic_search

app = FastAPI()


class SearchQuery(BaseModel):
    query: str


@app.get("/")
def index():
    return "Semantic search API"


@app.on_event("startup")
async def load_data():
    global merged_df, corpus_embeddings
    merged_df = pd.read_csv('app/data/merged_tables_live.csv')
    merged_df['combined_text'] = merged_df.apply(lambda row: ' '.join([
        str(row['Email']), str(row['Name']), str(row['Full Name']),
        str(row['City']), str(row['Designation']), str(row['Department']),
        str(row['Career Highlights']), str(row['Introduction']),
        str(row['Skills']), str(row['Project_Engagements'])
    ]), axis=1)
    corpus_embeddings = get_corpus_embeddings(merged_df['combined_text'].tolist())


@app.post("/search", response_model=List[dict])
async def search(query: SearchQuery):
    top_results, cos_scores = semantic_search(query.query, corpus_embeddings)
    results = []
    for idx in top_results:
        idx = int(idx)
        results.append({
            "User ID": merged_df.iloc[idx]['User ID'].item(),
            "Full Name": merged_df.iloc[idx]['Full Name'],
            "Email": merged_df.iloc[idx]['Email'],
            "Designation": merged_df.iloc[idx]['Designation'],
            "Skills": merged_df.iloc[idx]['Skills'],
            "Similarity Score": cos_scores[idx].item()
        })

    return results
