import streamlit as st
import requests
import pandas as pd

# --- SETTINGS ---
TOKEN = "58FREGzMeLl978tXYDz0cTenSmLxgUsuNoA2WmXNO3I"  # Replace with your Developer Token
API_URL = "https://api.producthunt.com/v2/api/graphql"

# --- GRAPHQL QUERY ---
query = """
query {
  posts(first: 10, order: VOTES) {
    edges {
      node {
        name
        tagline
        votesCount
        commentsCount
        topics {
          edges {
            node { name }
          }
        }
        url
      }
    }
  }
}
"""

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# --- STREAMLIT UI ---
st.title("🔥 Product Hunt Trending Insights")
st.write("Explore top trending products, their tags, and engagement.")

# Fetch data
with st.spinner("Fetching trending products from Product Hunt..."):
    response = requests.post(API_URL, json={"query": query}, headers=headers)
    data = response.json()

# Parse data
products = []
for edge in data.get("data", {}).get("posts", {}).get("edges", []):
    node = edge["node"]
    topics = ", ".join([t["node"]["name"] for t in node["topics"]["edges"]])
    products.append({
        "Name": node["name"],
        "Tagline": node["tagline"],
        "Votes": node["votesCount"],
        "Comments": node["commentsCount"],
        "Topics": topics,
        "URL": node["url"]
    })

df = pd.DataFrame(products)

# Display table
st.dataframe(df)

# Download as CSV
csv = df.to_csv(index=False)
st.download_button("Download as CSV", data=csv, file_name="producthunt_trending.csv", mime="text/csv")
