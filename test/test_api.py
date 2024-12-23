import requests
import os
import pprint
import yaml
from cs2cad.onshape_parser.my_client import MyClient
from cs2cad.onshape_parser import process_many

c = MyClient(logging=False)

# response = c.documents(mode="public")

query = "gear"

file_path = c.query2yml(query=query, limit=5)
process_many(file_path)


# for item in doc["items"]:
#     print(item["href"])

# if __name__ == "__main__":
#     public_documents = get_public_documents()
#     if public_documents:
#         print("Public Documents:")
#         for doc in public_documents['items']:
#             print(f"Document Name: {doc['name']}, ID: {doc['id']}")
