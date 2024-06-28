# SemanticSearch
Semantic search using python, sentence_transformers and FastAPI

## Running the FastAPI Application

### Install the required dependencies:

` pip install -r requirements.txt `

### Run the FastAPI application using uvicorn:

` uvicorn main:app --reload  `

Open your browser and go to http://127.0.0.1:8000/docs to access the interactive API documentation provided by FastAPI.

## Explanation
- **main.py:** This is the main entry point of the FastAPI application. It sets up the FastAPI instance, loads data and embeddings on startup using the lifespan middleware, and defines the /search endpoint.
- **embeddings.py:** This module handles loading the pre-trained SentenceTransformer model and generating embeddings.
- **search.py:** This module contains the semantic_search function that performs the semantic search using the embeddings. It imports the model from embeddings.py.
- **models.py:** This module defines the Pydantic model for validating the search query.
- **data/:** This directory contains the CSV files for the user and skill tables.