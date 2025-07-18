import requests
from tabulate import tabulate

TOKEN = "58FREGzMeLl978tXYDz0cTenSmLxgUsuNoA2WmXNO3I"
API_URL = "https://api.producthunt.com/v2/api/graphql"

query = """
query {
  posts(first: 5, order: VOTES) {
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

response = requests.post(API_URL, json={"query": query}, headers=headers)
data = response.json()

table = []
for edge in data.get("data", {}).get("posts", {}).get("edges", []):
    node = edge["node"]
    topics = ", ".join([t["node"]["name"] for t in node["topics"]["edges"]])
    table.append([node["name"], node["tagline"], node["votesCount"], node["commentsCount"], topics, node["url"]])

# Print as a nice table
print(tabulate(table, headers=["Name", "Tagline", "Votes", "Comments", "Topics", "URL"], tablefmt="fancy_grid"))
import csv

with open("producthunt_trending.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Tagline", "Votes", "Comments", "Topics", "URL"])
    writer.writerows(table)

print("\nData saved to producthunt_trending.csv")

