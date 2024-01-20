from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright 
import json 
from datetime import datetime, timedelta
import concurrent.futures
import time


print(f"Iniciando busca... [{time.strftime('%X')}]")

############ Setting variables
timeStart = time.time()
countriesToArrive = ["BCN", "MAD", "LIS", "OPO"]
minDateToTravel = datetime(2024, 4, 3)
maxDateToTravel = datetime(2024, 5, 10)
minDaysToTravel = 25
maxDaysToTravel = 34
differenceOfDays = maxDateToTravel - minDateToTravel
url = "https://www.viajanet.com.br/shop/flights/results/roundtrip/FLN/BCN/2024-03-07/2024-03-13/1/0/0?di=1-0"
#api = "Get the search? value in the future"
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




####### GET POSSIBLES DEPARTURES AND ARRIVES
def getPossiblesDeparturesAndArrives(dates, minDays, maxDays):

    possiblesFlights = []
    for date in dates:
        for datemax in dates:
            if (datemax - date).days >= minDays and (datemax - date).days <= maxDays:
                flight = {
                    'departure': date.strftime('%Y-%m-%d'),
                    'arrive': datemax.strftime('%Y-%m-%d'),
                    'totalTravelDays': (datemax - date).days
                }
                possiblesFlights.append(flight)

    return possiblesFlights

    ###############################################

# === Getting percent from search ===
def percentFromSearch():
    totalTimeSearch = 0
    possibleDates = getPossiblesDeparturesAndArrives(travelDates, minDaysToTravel, maxDaysToTravel)
    for date in possibleDates:
        date = date['departure']
        totalTimeSearch += 1

    return totalTimeSearch
        
    



############ Getting price data
def getPriceData(viajanetUrl):
    try:
        with sync_playwright() as p: 
            def handle_response(response): 
                # the endpoint we are insterested in 
                if ("search?" in response.url):
                    global apiJson
                    global apiData
                    apiData = response.json()
                    apiJson = json.dumps(apiData)
            
            browser = p.chromium.launch()
            page = browser.new_page() 
            page.set_default_timeout(60000)
            page.on("response", handle_response) 
            page.goto(viajanetUrl, wait_until="networkidle")
            time.sleep(2)
            page.context.close() 
            browser.close()
    except Exception as e:
        print('Tempo de resposta excedido!')

    return apiData

priceData = getPriceData(url)

######################





###################### Return the lowest price value


def returnTheLowestPrice(data):
    i = 0
    flightsPrices = []
    for item in data['items']: #Return a list with price values
        try:
            i += 1
            flightsPrices.append(item['item']['priceDetail']['mainFare']['amount'])

        except Exception as e:
            None

    lowestFlightPrice = min(flightsPrices)

    return lowestFlightPrice

#################################################









########### Making the code run ####################


def process_country(country):
    possiblesDates = getPossiblesDeparturesAndArrives(travelDates, minDaysToTravel, maxDaysToTravel)
    for departureAndArrive in possiblesDates:
        
        departure = departureAndArrive['departure']
        arrive = departureAndArrive['arrive']
        days = departureAndArrive['totalTravelDays']
        viajanetUrl = f"https://www.viajanet.com.br/shop/flights/results/roundtrip/FLN/{country}/{departure}/{arrive}/1/0/0?di=1-0"

        if getPriceData(viajanetUrl) is not None:
            priceData = getPriceData(viajanetUrl)

            lowestValue = returnTheLowestPrice(priceData)

            print(f"Chegada: {country}- Ida: {departure} - Volta: {arrive} - Dias: {days} - Valor mais baixo: {lowestValue} - link: {viajanetUrl}")

        

with concurrent.futures.ProcessPoolExecutor() as executor:
    results_per_country = executor.map(process_country, countriesToArrive)


timeStop = time.time()

print(f"Tempo de duração da pesquisa: {timeStop - timeStart}")

#####################################################
    