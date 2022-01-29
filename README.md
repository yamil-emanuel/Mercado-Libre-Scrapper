# Mercado-Libre-Scrapper
WebScrapper developed using Selenium and Beautifulsoups. Exports a csv file with the collected data.
Requieriments: Selenium and BeautifulSoups.

MAIN PARAMETERS:

#SETS THE OUTPUT'S FILE NAME.
CSV_FILE_NAME="SEARCH.csv"

#HOW MANY PAGES WILL BE SCRAPPED
NUMBER_OF_PAGES=5

#SEARCH CRITERIA
SEARCH_CRITERIA='sennheiser'




###MAIN FUNCTIONS.

#COOKIE DISCLAIMER BUTTON
CookieDisclaimer(browser)

#SLEEP RANDOM TIME BETWEEN 1 AND 6 SECS.
sleep(Sleep())

#SEARCH FOR THE CRITERIA
Search(browser,SEARCH_CRITERIA)

#SLEEP RANDOM TIME BETWEEN 1 AND 6 SECS.
sleep(Sleep())
    
#Scraps the data of every search result. ["FECHA","PÁGINA","TITULO","PRECIO","PRECIO CON DESCUENTO","DESCUENTO %","TIENDA OFICIAL","CANTIDAD CUOTAS","REVIEWS","STARS","COLORES DISPONIBLES","FULL","HIGHLIGHTS","FECHA ARRIVO","TIPO DE ENVÍO","TAGS","URL"]

#CREATES THE CSV FILE
data=CaptureData(link,n)

UpdateCSV(data)
        
#sCROLLS DOWN AUTOMATICALLY IN THE BROWSER
NumericPage(browser)

#SETS A RANDOM-LONG PAUSE BETWEEN FUNCTION'S CALL
sleep(Sleep())

#CLOSES THE BROWSER.
browser.quit()
