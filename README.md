# Mercado-Libre-Scrapper
Exports a csv file with the collected data. It's a Mercadolibre's webScrapper developed using Selenium and Beautifulsoups as a content parser. 
For every excecution it returns a data table with the following data:
Date, Page n°, title, price, discount price (if exists), discount percentage, if the shop is verified or not, payment split/if is avaiable, Reviews amount, Rating, colors available, highlights, estimed arrival time, deliver type, tags, post url.

#REQUIERIMENTS
Please install all the dependencies before running.

#USAGE
1)The user must fill the following fields:
    SEARCH_CRITERIA= [str:WHAT ARE WE GOING TO SEARCH]
    NUMBER_OF_PAGES=[int:HOW MANY PAGES WILL BE SCRAPPED]
2)Run the code.
