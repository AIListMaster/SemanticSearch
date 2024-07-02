from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic
from fastapi.security.http import HTTPBasicCredentials
import pandas as pd
import torch
import os
from typing import List
from app.security import verify_credentials
from app.base.embeddings import get_corpus_embeddings, get_embeddings
from app.search.search import semantic_search
from app.base.models import TextData
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Basic auth setup
security = HTTPBasic()


@app.get("/")
def index():
    return "Semantic search API"


@app.on_event("startup")
async def load_data():
    global merged_df, corpus_embeddings
    tensor_file_path = 'app/data/corpus_embeddings.pt'

    # Read CSV data - Needed to produce results.
    merged_df = pd.read_csv('app/data/merged_tables_live.csv')

    if os.path.exists(tensor_file_path):
        # Load tensors from file
        corpus_embeddings = torch.load(tensor_file_path)
    else:
        corpus_embeddings = get_corpus_embeddings(merged_df['combined_text'].tolist())
        # Save tensors to file
        torch.save(corpus_embeddings, tensor_file_path)


@app.post("/search", response_model=List[dict])
async def search(query: TextData):
    top_results, cos_scores = semantic_search(query.input, corpus_embeddings)
    results = []
    for idx in top_results:
        idx = int(idx)
        results.append({
            "User ID": merged_df.iloc[idx]['User ID'].item(),
            "Full Name": merged_df.iloc[idx]['Full Name'],
            "Email": merged_df.iloc[idx]['Email'],
            "Designation": merged_df.iloc[idx]['Designation'],
            "Similarity Score": cos_scores[idx].item()
        })

    return results


@app.post("/embed")
async def get_embedding(data: TextData, credentials: HTTPBasicCredentials = Depends(security)):
    verify_credentials(credentials)
    try:
        # Generate embeddings
        embedding = get_embeddings(data.input)
        return {"embedding": embedding}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
