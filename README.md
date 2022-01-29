# Mercado-Libre-Scrapper
Mercadolibre's webScrapper developed using Selenium and Beautifulsoups. Exports a csv file with the collected data.

See requieriments (bs4, xlmx, requests, selenium + webdriver Mozilla Firefox)

MAIN PARAMETERS:

#DRIVER PATH
GECKO='''C:/Users/yamil/Desktop/geckodriver.exe'''

#OUTPUT'S FILE NAME.
CSV_FILE_NAME="SEARCH.csv"

#HOW MANY PAGES WILL BE SCRAPPED
NUMBER_OF_PAGES=5

#SEARCH CRITERIA
SEARCH_CRITERIA='sennheiser'
    
#Scraps the data of every search result page.
["FECHA","PÁGINA","TITULO","PRECIO","PRECIO CON DESCUENTO","DESCUENTO %","TIENDA OFICIAL","CANTIDAD CUOTAS","REVIEWS","STARS","COLORES DISPONIBLES","FULL","HIGHLIGHTS","FECHA ARRIVO","TIPO DE ENVÍO","TAGS","URL"]
