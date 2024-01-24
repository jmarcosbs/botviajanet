from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright 
import json 
from datetime import datetime, timedelta
import concurrent.futures
import time
import multiprocessing
from google.cloud import logging
import asyncio


print(f"Iniciando busca... [{time.strftime('%X')}]")

# Google Cloud
project_id = 'dulcet-glyph-411603'
client = logging.Client(project=project_id)
logger = client.logger('my-log')
# ======

############ Setting variables
timeStart = time.time()
countriesToArrive = ["BCN", "MAD", "LIS", "OPO"]
minDateToTravel = datetime(2024, 4, 3)
maxDateToTravel = datetime(2024, 5, 10)
minDaysToTravel = 25
maxDaysToTravel = 34
minPriceToLook = 4200
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

    

apiData = None
apiJson = None

# ... (seções iniciais do código permanecem inalteradas)

async def getPriceData(viajanetUrl):
    try:
        async with sync_playwright() as p:
            async def handle_response(api_data, api_json, response):
                if "search?" in response.url:
                    data = await response.json()
                    api_data.update(data)
                    api_json.append(json.dumps(data))

            apiData = {}
            apiJson = []

            browser = await p.chromium.launch()
            page = await browser.new_page()
            page.set_default_timeout(60000)
            page.on("response", lambda response: handle_response(apiData, apiJson, response))
            await page.goto(viajanetUrl, wait_until="networkidle")
            await page.wait_for_timeout(10)
            await page.context.close()
            await browser.close()
    except Exception as e:
        print(f'Erro: {e}')

    return apiData

# ... (restante do código permanece inalterado)


async def process_country(country):
    try:
        possiblesDates = getPossiblesDeparturesAndArrives(travelDates, minDaysToTravel, maxDaysToTravel)
        numberOfPossibilities = len(possiblesDates)

        for departureAndArrive in possiblesDates:
            departure, arrive, days = departureAndArrive['departure'], departureAndArrive['arrive'], departureAndArrive['totalTravelDays']
            viajanetUrl = f"https://www.viajanet.com.br/shop/flights/results/roundtrip/FLN/{country}/{departure}/{arrive}/1/0/0?di=1-0"

            global i
            i += 1
            progress = i / numberOfPossibilities * 100

            if await getPriceData(viajanetUrl) is not None:
                priceData = await getPriceData(viajanetUrl)
                lowestPrice = returnTheLowestPrice(priceData)

                print(f"{progress}% Chegada: {country} - Ida: {departure} - Volta: {arrive} - Dias: {days} - Valor mais baixo: {lowestPrice} - link: {viajanetUrl}")

                if lowestPrice <= minPriceToLook:
                    print("Preço alvo encontrado!")

                    token = "6891057872:AAHEN4leh0JQxpmLiR0GN4YB38eHtaGkB2M"
                    chatId = "732421718"
                    telegramMessage = f"Alerta de preço: R${lowestPrice} - {country} - {days} dias - Link: {viajanetUrl}"
                    telegramUrl = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chatId}&text={telegramMessage}"

                    send = requests.get(telegramUrl)  # Send mensagem in Telegram
                    send.json()
    except Exception as e:
        print(f'Erro: {e}')
        logger.log_text(e)

async def main():
    global i
    i = 0
    tasks = []

    async with sync_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        with concurrent.futures.ProcessPoolExecutor(max_workers=-1) as executor:
            for country in countriesToArrive:
                tasks.append(asyncio.ensure_future(process_country(country)))

            await asyncio.gather(*tasks)

        await page.context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
