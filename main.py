from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import randint
from functions import *
import requests
from bs4 import BeautifulSoup
import csv
import datetime

#HOW WILL THE FILE NAMED
CSV_FILE_NAME="SEARCH.csv"
#HOW MANY PAGES WILL BE SCRAPPED
NUMBER_OF_PAGES=5
#WHAT ARE WE GOING TO SEARCH
SEARCH_CRITERIA='sennheiser'

def CaptureData(link,page_n):
    print(('Capturing data in {}').format(link))
    url=requests.get(link)
    soup = BeautifulSoup(url.content, 'lxml')
    #POSTS
    posts=soup.find_all(attrs={'class':'ui-search-result__content-wrapper'})
    #Scrapping info from each posts

    def CapturePage(posts):
        temp=[]
        for element in posts:

            #TITLE
            title_raw=element.find_all(attrs={'class':'ui-search-item__title'})

            #PRICE
            price_raw=element.find_all(attrs={'class':'price-tag-fraction'})

            #DISCOUNTED PRICE
            def IsDiscounted (element):
                #Finding the price-fraction-tag ellement.
                discounted_price=element.find_all(attrs={'class':'price-tag-fraction'})
                temp=[]
                if discounted_price is not None:
                    for x in discounted_price:
                        temp.append(x.get_text())
                else:
                    pass
                if len(temp)>1:
                    return temp[1]
                else:
                    return None

            #N°Reviews
            def ReviewsAmount(element):
                reviews_amount_raw=element.find("span",attrs={'class':'ui-search-reviews__amount'})
                if reviews_amount_raw is not None:
                    final_reviews_amount=reviews_amount_raw.get_text()
                    return final_reviews_amount
            
            #TAGS 
            def IsOfficial(element):
                tags_raw=element.find_all('p')
                temp=[]
                tags_raw=list(tags_raw)
                for element in tags_raw:
                    if element is not None:
                        temp.append(element.get_text())
                    else:
                        pass
                return temp

            #TAGS CATEGORIES. RETURNS A DICTIONARY.
            def Tags(final_tags):
                vendido_por="Vendido por"
                Llega="Llega"
                Envio_gratis="Envío"

                dicc={}

                if final_tags != None:
                    for tag in final_tags:
                        if vendido_por in tag:
                            tag=tag.split(' ')
                            tag=tag[2:]
                            tag=(' ').join(tag)
                            dicc['final_is_official']=tag
                        elif Llega in tag:
                            dicc['final_shipping_type']=tag
                        elif Envio_gratis in tag:
                            dicc['final_arrives_at']=tag           
                else:
                    pass

                return dicc    
        
            #AVAILABLE COLOURS
            def ColourCapture(element):
                colours_raw=element.find_all(attrs={'class':'ui-search-result__content-column ui-search-result__content-column--right'})
                temp=[]
                for x in colours_raw:
                    a=x.find_all(attrs={'class':'andes-list__item-primary'})
                    for i in a:
                        temp.append(i.get_text())
                return temp
            
            #CAPTURE THE STAR'S CALIFICATION. if doesn't exist return None.
            def CaptureStars(element):
                rating=element.find_all('span',attrs={'class':'ui-search-reviews__ratings'})
                
                full_star_raw=element.find_all(attrs={'class':'ui-search-icon ui-search-icon--star ui-search-icon--star-full'})
                full_star=len(list(full_star_raw))

                half_star_raw=element.find_all(attrs={'class':'ui-search-icon ui-search-icon--star ui-search-icon--star-half'})
                if not half_star_raw:
                    return None
                else:
                    return full_star+0.5

            #CAPTURE THE DISCOUNT %
            def DiscountPercentage(element):
                discount_percentage_raw=element.find_all('span')
                temp=[]
                for x in discount_percentage_raw:
                    x=(x.get_text())

                    if "%" in x:
                        temp.append(x)
                    else:
                        pass
                if len(temp)>0:
                    final=temp[0].split('%')
                    return final[0]
                else:
                    return None

            #CAPTURE OTHER HIGHLIGHTS
            def Highlights(element):
                highlights_raw=element.find_all(attrs={'class':'ui-search-styled-label ui-search-item__highlight-label__text'})
                for x in highlights_raw:
                    final_highlight=x.get_text()
                    return final_highlight
            
            #FULL
            def IsFull(element):
                full_raw=element.find_all('svg')
                for x in full_raw:
                    if "ui-search-icon--full" in str(x):
                        return 'Full'
                    else:
                        return None
            
            #COUTAS
            def Cuotas(element):
                cuotas_raw=element.find_all(attrs={'class':'ui-search-item__group__element ui-search-installments ui-search-color--LIGHT_GREEN'})
                for x in cuotas_raw:
                    cuotas=(x.get_text()).split(" ")
                    for word in cuotas:
                        if word.isdigit() ==True:
                            return word
                        else:
                            pass
            
            def UrlCapture(element):
                url=element.find('a')
                return (url['href'])

            final_time=datetime.datetime.now()
            final_page=page_n
            final_cuotas=Cuotas(element)
            final_full=IsFull(element)
            final_discount_percentage=DiscountPercentage(element)
            final_stars=CaptureStars(element)
            final_title=title_raw[0].get_text()
            final_price=(price_raw[0].get_text()).replace('.','')
            final_discounted_price=IsDiscounted(element)
            final_colours=ColourCapture(element)
            final_tags=IsOfficial(element)
            final_reviews_amount=ReviewsAmount(element)
            final_highlights=Highlights(element)
            final_dictionary=Tags(final_tags)
            final_is_official=final_dictionary.get('final_is_official')
            final_shipping_type=final_dictionary.get('final_shipping_type')
            final_arrives_at=final_dictionary.get('final_arrives_at')
            final_url=UrlCapture(element)

            

            

            final=final_time,final_page,final_title,final_price,final_discounted_price,final_discount_percentage,final_is_official,final_cuotas,final_reviews_amount,final_stars,final_colours,final_full,final_highlights,final_arrives_at,final_shipping_type,final_tags,final_url
            temp.append(final)
            

        return temp

    data=CapturePage(posts)
    return data

def CreateCSV():
    #CREATE A CSV FILE WITH THESE ATTRIBUTES: ["FECHA","PÁGINA","TITULO","PRECIO","PRECIO CON DESCUENTO","DESCUENTO %","TIENDA OFICIAL","CANTIDAD CUOTAS","REVIEWS","STARS","COLORES DISPONIBLES","FULL","HIGHLIGHTS","FECHA ARRIVO","TIPO DE ENVÍO","TAGS","URL"]
    print(("Creating {} file.").format(CSV_FILE_NAME))
    with open (CSV_FILE_NAME,'w', newline='') as file:
        writer=csv.writer(file)
        writer.writerow(["FECHA","PÁGINA","TITULO","PRECIO","PRECIO CON DESCUENTO","DESCUENTO %","TIENDA OFICIAL","CANTIDAD CUOTAS","REVIEWS","STARS","COLORES DISPONIBLES","FULL","HIGHLIGHTS","FECHA ARRIVO","TIPO DE ENVÍO","TAGS","URL"])

def UpdateCSV(data):
    #INSERT THE COLLECTED DATA INTO THE CSV FILE.
    print("Updating the database.")
    with open (CSV_FILE_NAME,'a+', newline='') as file:
        writer=csv.writer(file)
        for element in data:
            date=element[0]
            page=element[1]
            title=element[2]
            price=element[3]
            discounted_price=element[4]
            discount_percentage=element[5]
            is_official=element[6]
            cuotas=element[7]
            reviews=element[8]
            stars=element[9]
            colours=element[10]
            full=element[11]
            highlights=element[12]
            arrives_at=element[13]
            shipping_type=element[14]
            tags=element[15]
            url=element[16]
            writer.writerow([date,page,title,price,discounted_price,discount_percentage,is_official,cuotas,reviews,stars,colours,full,highlights,arrives_at,shipping_type,tags,url])

def Sleep():
    #MAKES A STOP OF X AMOUNT OF SECONDS BEFORE CONTINUE.
    n=randint(1,6)
    print(("Sleeping {} secs.").format(n))
    return n

def ScrollDown(browser):
    #SCROLLS DOWN UNTIL THE END OF THE PAGE.

    SCROLL_PAUSE_TIME = 0.5
    print('Scrolling down.')
    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def CookieDisclaimer(browser):
    #CLICK ON "ENTENDIDO" ON THE COOKIE DISCLAIMER POLICY POP-UP
    print(('CookieDisclaimer'))
    cookie_disclaimer=browser.find_element_by_class_name('nav-cookie-disclaimer__button')
    cookie_disclaimer.click()
    print('Finished.')

def Search(browser,criteria):
    #MAKING A SEARCH IN THE MAIN PAGE.
    print(("Searching for {}").format(criteria))
    search_box=browser.find_element_by_class_name("nav-search-input")
    search_box.click()
    search_box.send_keys(criteria + Keys.ENTER)

def NextPage(browser):
    url=browser.current_url
    print(url)
    print('Clicking next button.')  
    ClickNext=browser.find_element_by_xpath('//*[@id="root-app"]/div/div[1]/section/div[3]/ul/li[11]/a')
    ClickNext.click()

def NumericPage(browser):
    print('Click next button')
    continue_link = browser.find_element_by_link_text('Siguiente')

    continue_link.click()
 
def run():
    #OPEN THE BROWSER
    browser = webdriver.Firefox(executable_path='/home/yamil/geckodriver')
    browser.get('http://www.mercadolibre.com.ar/')

    #COOKIE DISCLAIMER BUTTON
    CookieDisclaimer(browser)
    
    #SLEEP RANDOM TIME BETWEEN 1 AND 6 SECS.
    sleep(Sleep())

    #SEARCH FOR THE CRITERIA
    Search(browser,SEARCH_CRITERIA)

    #SLEEP RANDOM TIME BETWEEN 1 AND 6 SECS.
    sleep(Sleep())
    

    for x in range(NUMBER_OF_PAGES):
        link=browser.current_url
        print(('Visiting page N°{}').format(x))

        data=CaptureData(link,x+1)
        UpdateCSV(data)
        ScrollDown(browser)
        NumericPage(browser)
        sleep(Sleep())
        print('------------\n')
    
    browser.quit()
        

run()
