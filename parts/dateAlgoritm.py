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

