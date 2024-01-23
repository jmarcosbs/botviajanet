from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright
import json
from datetime import datetime, timedelta
import concurrent.futures
import time
import multiprocessing
# from google.cloud import logging


print(f"Iniciando busca... [{time.strftime('%X')}]")

# Google Cloud
# project_id = 'dulcet-glyph-411603'
# client = logging.Client(project=project_id)
# logger = client.logger('my-log')
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

apiData = None
apiJson = None

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
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(10)
            page.context.close()
            browser.close()
except Exception as e:
        print(f'Erro: {e}')

print(apiData)

######################




