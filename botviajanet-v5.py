import requests
import json 
from datetime import datetime, timedelta
import time
import asyncio                            
from playwright.sync_api import sync_playwright


print(f"Iniciando busca...")


############ Setting variables
countriesToArrive = ["BCN", "MAD", "LIS", "OPO"]
minDateToTravel = datetime(2024, 4, 3)
maxDateToTravel = datetime(2024, 5, 10)
minDaysToTravel = 25
maxDaysToTravel = 34
url = "https://www.viajanet.com.br/shop/flights/results/roundtrip/FLN/BCN/2024-03-07/2024-03-13/1/0/0?di=1-0"
####################################################



#======= Return a list of dates to analyse =====

def getPossibleFlights(startDate, endDate):
    dateList = []
    date = startDate

    while date <= endDate:
        dateList.append(date)
        date += timedelta(days=1)

    
    #Get possibles arrives and departures
        
    possiblesFlights = []

    for date in dateList:
        for datemax in dateList:
            if (datemax - date).days >= minDaysToTravel and (datemax - date).days <= maxDaysToTravel:
                flight = {
                    'departure': date.strftime('%Y-%m-%d'),
                    'arrive': datemax.strftime('%Y-%m-%d'),
                    'totalTravelDays': (datemax - date).days
                }
                possiblesFlights.append(flight)

    return possiblesFlights

print(getPossibleFlights(minDateToTravel, maxDateToTravel)[2])





# apiData = None
# apiJson = None

# ############ Getting price data
# import json
# from playwright.sync_api import sync_playwright

# async def getPriceData(viajanetUrl):
#     try:
#         async with sync_playwright() as p:
#             async def handle_response(response, api_data, api_json):
#                 if "search?" in response.url:
#                     data = await response.json()
#                     api_data.update(data)
#                     api_json.append(json.dumps(data))

#             apiData = {}
#             apiJson = []

#             browser = await p.chromium.launch()
#             page = await browser.new_page()
#             page.set_default_timeout(60000)
#             page.on("response", lambda response: handle_response(response, apiData, apiJson))
#             await page.goto(viajanetUrl, wait_until="networkidle")
#             await page.wait_for_timeout(10)
#             await page.context.close()
#             await browser.close()
#     except Exception as e:
#         print(f'Erro: {e}')

#     return apiData


# priceData = getPriceData(url)

# ######################





# ###################### Return the lowest price value


# def returnTheLowestPrice(data):
#     i = 0
#     flightsPrices = []
#     for item in data['items']: #Return a list with price values
#         try:
#             i += 1
#             flightsPrices.append(item['item']['priceDetail']['adultTotal'])

#         except Exception as e:
#             None

#     lowestFlightPrice = min(flightsPrices)

#     return lowestFlightPrice

# #################################################




# ########### Making the code run ####################

# global i
# i = 0
# for country in countriesToArrive:
#     try:
        
#         possiblesDates = getPossiblesDeparturesAndArrives(travelDates, minDaysToTravel, maxDaysToTravel)
#         numberOfPossibilities = len(possiblesDates)
        
#         for departureAndArrive in possiblesDates:
#             departure = departureAndArrive['departure']
#             arrive = departureAndArrive['arrive']
#             days = departureAndArrive['totalTravelDays']
#             viajanetUrl = f"https://www.viajanet.com.br/shop/flights/results/roundtrip/FLN/{country}/{departure}/{arrive}/1/0/0?di=1-0"
            
#             i = i + 1
#             progress = i / numberOfPossibilities * 100

#             if getPriceData(viajanetUrl) is not None:
#                 priceData = getPriceData(viajanetUrl)

#                 lowestPrice = returnTheLowestPrice(priceData)

#                 print(f"{progress}% Chegada: {country} - Ida: {departure} - Volta: {arrive} - Dias: {days} - Valor mais baixo: {lowestPrice} - link: {viajanetUrl}")

#                 if lowestPrice <= minPriceToLook:

#                     print("Preço alvo encontrado!")

#                     token = "6891057872:AAHEN4leh0JQxpmLiR0GN4YB38eHtaGkB2M"

#                     chatId = "732421718"

#                     telegramMessage = f"Alerta de preço: R${lowestPrice} - {country} - {days} dias - Link: {viajanetUrl}"

#                     telegramUrl = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chatId}&text={telegramMessage}"

#                     send = requests.get(telegramUrl)  #Send mensage in Telegram
#                     send.json()
#     except Exception as e:
#         print(f'Erro: {e}')



# print(f"Pesquisa Finalizada.")

# #####################################################
    