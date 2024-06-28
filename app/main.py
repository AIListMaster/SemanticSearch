from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
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
    user_df = pd.read_csv('app/data/user_table_live.csv')
    skill_df = pd.read_csv('app/data/skill_table_live.csv')
    merged_df = pd.merge(user_df, skill_df, on='User ID')
    merged_df['combined_text'] = merged_df.apply(lambda row: ' '.join([
        str(row['Email']), str(row['Name']), str(row['Full Name']),
        str(row['City']), str(row['Designation']), str(row['Department']),
        str(row['Career Highlights']), str(row['Introduction']),
        str(row['Skill Name']), str(row['Competence Level'])
    ]), axis=1)
    corpus_embeddings = get_corpus_embeddings(merged_df['combined_text'].tolist())


@app.post("/search")
async def search(query: SearchQuery):
    top_results, cos_scores = semantic_search(query.query, corpus_embeddings)
    results = []
    for idx in top_results:
        idx = int(idx)
        results.append({
            "User ID": merged_df.iloc[idx]['User ID'],
            "Name": merged_df.iloc[idx]['Name'],
            "Email": merged_df.iloc[idx]['Email'],
            "Designation": merged_df.iloc[idx]['Designation'],
            "Skill": merged_df.iloc[idx]['Skill Name'],
            "Similarity Score": cos_scores[idx].item()
        })
    return {"results": results}
