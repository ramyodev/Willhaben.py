import requests

print(1)
response = requests.get("https://www.willhaben.at/iad/kaufen-und-verkaufen/marktplatz?&rows=100").content
print(2)