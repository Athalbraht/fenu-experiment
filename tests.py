import requests
from sys import argv

print("Usage: python ADDRESS ENDPOINTS")


URL = f"{argv[1]}"

print(f"Calling {URL}{argv[2]}...")

response = requests.get(URL + argv[2])

print(f"RESPONSE:\n{response}")
print(f"RESPONSE:\n{response.content}")




