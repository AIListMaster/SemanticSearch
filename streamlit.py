import streamlit as st
import requests


# Function to call the /search endpoint
def search_query(query):
    url = "http://192.168.1.219:8000/search"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "input": query
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()


# Streamlit UI
st.title("Semantic Search Application")
query = st.text_area("Enter your search query:",
                     "Show me all the users having JavaScript skills and their Designation must be Software Engineer")

if st.button("Search"):
    with st.spinner("Searching..."):
        results = search_query(query)
        st.success("Search completed!")
        st.json(results)
