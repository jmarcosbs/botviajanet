from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright 
import json 

url = "https://www.viajanet.com.br/shop/flights/results/roundtrip/FLN/BCN/2024-03-07/2024-03-13/1/0/0?di=1-0"

api = "Get the search? value in the future"
 
with sync_playwright() as p: 
	def handle_response(response): 
		global api
		# the endpoint we are insterested in 
		if ("search?" in response.url): 
			api = json.dumps(response.json())
 
	browser = p.chromium.launch() 
	page = browser.new_page() 
	page.on("response", handle_response) 
	page.goto(url, wait_until="networkidle") 
	page.context.close() 
	browser.close()

priceData = json.loads(api)

flights = {}

i=0

for item in priceData['items']:
	i += 1
	flights[f"flight{i}%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"] = item['item']

for chave in flights:
	print(flights[chave]['priceDetail'])


# for chave in flights:
# 	print(f"{chave} $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

prices = []

daysDifference = flights

# for item in flights:
# 	try:
# 		if isinstance(item['item']['priceDetail']['mainFare']['amount'], int):
# 			prices.append(item['item']['priceDetail']['mainFare']['amount'])
# 			#print(f"Preço total: {item['item']['priceDetail']['mainFare']['amount']}")
# 	except Exception as e:
# 		None

# lowestValue = 10000

# for price in prices:
# 	if price < lowestValue:
# 		lowestValue = price
		
# print(f"Valor mais baixo: {lowestValue}")

#for item in priceData['items']:
	#print(item['item'])

#with open('items-json.json', 'w') as arquivo_json:
    #json.dump(type(priceData), arquivo_json)
