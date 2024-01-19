from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright 
import json 
from datetime import datetime, timedelta

############ Setting variables
countriesToArrive = ["BCN", "MAD", "LIS", "OPO"]
minDateToTravel = datetime(2024, 4, 3)
maxDateToTravel = datetime(2024, 5, 10)
minDaysToTravel = 25
maxDaysToTravel = 34
differenceOfDays = maxDateToTravel - minDateToTravel
url = "https://www.viajanet.com.br/shop/flights/results/roundtrip/FLN/BCN/2024-03-07/2024-03-13/1/0/0?di=1-0"
api = "Get the search? value in the future"
####################################################





############### Return a list of dates to analyse
def gerar_lista_datas(data_inicial, data_final): #Return a list of dates to analyse
    lista_datas = []
    data_atual = data_inicial

    while data_atual <= data_final:
        lista_datas.append(data_atual)
        data_atual += timedelta(days=1)

    return lista_datas

travelDates = gerar_lista_datas(minDateToTravel, maxDateToTravel)

################################################





############ Getting price data
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

######################





###################### Return the lowest price value
i = 0
flightsPrices = []

for item in priceData['items']: #Return a list with price values
	try:
		i += 1
		flightsPrices.append(item['item']['priceDetail']['mainFare']['amount'])

	except Exception as e:
		None

lowestFlightPrice = min(flightsPrices)

print('O preço mais baixo é', lowestFlightPrice)

#################################################


########### Making the code run ####################

for country in countriesToArrive:
	
    ####### GET POSSIBLES DEPARTURES AND ARRIVES
    for date in travelDates:
        for datemax in travelDates:
            if (datemax - date).days >= minDaysToTravel and (datemax - date).days <= maxDaysToTravel:
                global toAnalyseDates

                toAnalyseDates = {'possibleFlight':{}}
                toAnalyseDates['possibleFlight']['departure'] = date.strftime('%Y-%m-%d')
                toAnalyseDates['possibleFlight']['arrive'] = datemax.strftime('%Y-%m-%d')
                toAnalyseDates['possibleFlight']['totalTravelDays'] = (datemax - date).days
            
    ################################################
                
    ##################### Searching prices by Dates
    
    for possible in toAnalyseDates:
          print(possible)

##################################################### add comment
          
