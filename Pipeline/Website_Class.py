#Change: unnecessry comments and import statments check for necerry exception handling
# -*- coding: utf-8 -*-
# !pip install -r requirements_scraper.txt
#from azure.ai.textanalytics import TextAnalyticsClient
#from azure.core.credentials import AzureKeyCredential
#import spacy
import requests
import warnings
warnings.filterwarnings('ignore')
# For defining regular expression
import json
import re 
# To clean html page
from bs4 import BeautifulSoup
# for parsing all the tables present
# on the website
# from html_table_parser import HTMLTableParser
# To open an Image
# from PIL import Image
import time
# For converting image to text
#import pytesseract
from lxml import html
import io
import urllib
# To join base url with another url
from urllib.parse import urljoin, urlsplit
import http
import socket
import unidecode
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fuzzywuzzy import fuzz, process 
from selenium import webdriver

import config

# Add options to the selenium driver
chrome_options = Options()
#chrome_options.add_argument("--window-size=1920,1080")
#chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument("--user-agent=Chrome/77")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--disable-setuid-sandbox") 
chrome_options.add_argument("--disable-extensions") 
#chrome_options.add_argument("start-maximized") 
chrome_options.add_argument("disable-infobars")
#chrome_options.add_argument("--remote-debugging-port=9222")  # th
chrome_options.add_argument("--disable-dev-shm-usage")



"""Getting the HTML Page"""

class Website():

    def __init__(self):
        self.local_config = config.Local_config()
        self.constant_config = config.Constant_config()
        self.Threshold = self.constant_config.Threshold
        self.Keywords = self.constant_config.Keywords
        self.CHROMEDRIVER_PATH = self.local_config.WEBDRIVER_PATH
        self.WINDOW_SIZE = self.constant_config.WINDOW_SIZE
        chrome_options.add_argument("--window-size=%s" % self.WINDOW_SIZE)

    # The function returns the driver with the appropriate url
    # if redirection occurs, the the url after the page is redirected)
    def open_url(self,driver,url):
        """
        input: 
            driver: webdriver object of selenium
            url: to be opened in selenium driver
        output: 
            driver: selenium webdriver object with the url opened in it
            true_url:  url of the opened in the webdriver
        """
        print(url)
        try:  
            url=url.strip()
            if url.startswith('http')==False:
                url='http://'+url
            driver.get(url)
            time.sleep(5)

            # fetch the url of the opened website
            # in selenium to handle redirection
            true_url=driver.current_url
            print(true_url)
            return driver,true_url
        except Exception as e:
            if url.startswith('https'):
                url=url.replace('https','http')
            elif url.startswith('http'):
                url=url.replace('http','https')
            else:
                url='http://'+url
            try:
                url=url.strip()
                if url.startswith('http')==False:
                    url='http://'+url
                driver.get(url)
                time.sleep(5)

                # fetch the url of the opened website
                # in selenium to handle redirection
                true_url=driver.current_url
                print(true_url)
                return driver,true_url
            except Exception as e:
                with open('error_url_log.json','a') as file:
                    json.dump({'Type':'Scraper','URL':url,'timestamp':time.time()},file)
                    file.write('\n')          
            
                return str(e),''
                print(e)


    # The function returns the html page of the specified link        
    def html_page(self,driver,link):
        """
        Input: 
            link: The link of which the html 
            page is required
        Output:
            code: 0 for successful retrieval of
                html page
                1 for unsuccesful retrieval of
                html page
                2 for connection error
            soup: Beautiful soup of the page or 
                '' in case of unsuccessful attempt
            true_link: link of the page retrived  
        """
        try:    
            # get the driver with the opened link and 
            # link opened in the driver
            driver,true_link= self.open_url(driver,link)
            print("openURL")

            # get the html page of opened link
            soup = BeautifulSoup(driver.page_source,'lxml')
        except (ConnectionError, socket.timeout) as e:
            print('ConnectionError or Timeout', true_link)
            return 2, '',''
        except Exception as e:
            print(link)
            print(str(e)+ ' : ' +link)
            return 1,'',''
        return 0, soup,true_link

    """Getting the sitemap of website"""
    # Returns the sitemap keywords of a website using the links in the website    
    def website_sitemap(self,Website_links):
        """
        Input: Website_links: List of all links found on the website
        Output: list of keywords in company sitemap 
        """
        sitemap=set()
        for item in Website_links:
            sitemap.update(urlsplit(item).path.replace('-',' ').split('/'))
        return list(sitemap)


    """Getting the links on HTML page"""
    #This function implements fuzzy logic on urls
    def fuzzy_logic(self,string):
        """
        input: 
            string: the string for which we require best match of keyword
        output:
            fuzzy_keyword_ratio[0]: Keyword with best fuzzy score
            fuzzy_keyword_ratio[1]: Fuzzy score of the Keyword
        """  

        # Apply partial ratio to get the best matching keyword
        # from the Keywords
        fuzzy_keyword_ratio=process.extractOne(string,self.Keywords,
                                            scorer=fuzz.partial_ratio)
        return fuzzy_keyword_ratio[0],fuzzy_keyword_ratio[1]

    # This function returns the relevant links based on 
    # keywords from list of links
    def filter_links(self,links):
        """
        Input: links: set of links to be filtered
        Output: relevant_links: filtered links based on the
                                threshold for fuzzy score
        """
        relevant_links=set()
        
        # iterate over links and add only those links
        # to relevant links which have a fuzzy score of atleast
        # Threshold 
        for link in links:
            partial_link=urlsplit(link).path.replace('-',' ')
            if self.fuzzy_logic(partial_link)[1]>=self.Threshold:
                relevant_links.add(link)
        return relevant_links

    # This function gives all the links that are present on the webpage
    def website_links(self,driver,url):
        """
        Input: url: Main url whose links are to be extracted
        Output:  ('','',None) in case of unsuccessful retrieval of page
                (relevant_links, website_sitemap_keywords,True) in case of links with keywords matching present
                (all_links, website_sitemap_keywords, False) in case of no matching links found 
        """
        code,soup,true_url=self.html_page(driver,url)
        
        # code=0 means successful retrieval of html page
        if code == 0:
            # Store links in set to avoid duplicacy
            external_links = set()
            internal_links = set()
            # Find all elements with tag 'a'
            for line in soup.find_all('a'):
                # Get 'href' attribute
                link = line.get('href')
                if not link:
                    continue
                # If link doesnot start with 'http', 
                # we need to join it with url.    
                if link.startswith('http'):
                    external_links.add(link)
                else:
                    internal_links.add(link)

            # Creating full internal links.
            full_internal_links = {
                urljoin(true_url, internal_link) 
                for internal_link in internal_links
            }

            # get the domain of the true_url
            base_url=urlsplit(true_url).netloc
            base_url=base_url.replace("www.", "")
            links=[]
            # Add to links list.
            for link in external_links.union(full_internal_links):
                # get the domain of the link
                base_link=urlsplit(link).netloc
                # add to links only if domain is same as the true_link
                if base_url not in base_link:
                    continue
                links.append(link) 
            all_links=set(links) 
            
            # Get links with desired fuzzy score or more
            relevant_links=self.filter_links(all_links)
            print(len(relevant_links))
            print(relevant_links)
            # if no relevant links, return all links found on homepage
            # and flag False
            if len(relevant_links)==0:
                return all_links,self.website_sitemap(all_links), False
            else:
                # add url to relevant links
                relevant_links.add(url)   
            
            # return relevant links and flag True    
            return relevant_links,self.website_sitemap(all_links),True 
        else:
            #if code=1 or code=2 return '' and flag None:
            return [],[],'Failed'


    # This function removes all extra white spaces
    def collapse_white_spaces(self,txt):
        """Collapse multiple white spaces into one white space
        """
        clean_txt = ''
        prev = None
        for c in txt:
            if c == ' ' and prev == ' ':
                continue
            else:
                clean_txt += c
            prev = c
        return clean_txt

    def chunkIt(self,seq, num):
        avg = len(seq) / float(num)
        out = []
        last = 0.0

        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg

        return out

    '''
    # This function authenticates text analytics API credentials 
    # and returns text analytics client object
    def authenticate_client(key = text_analytics_key, endpoint = text_analytics_endpoint):
        """
        Input:key: text analytics API key
            endpoint: text analytics API endpoint
        Output: text analytics client if valid credentials else None
        """
        try:
            
            #Authenticate the azure service using key
            text_analytics_credential = AzureKeyCredential(key)
            # Initialize text analytics client
            text_analytics_client = TextAnalyticsClient(
                endpoint=endpoint, 
                credential=text_analytics_credential)
            return text_analytics_client
        
        except:
            
            print("Invalid credentials")
            return None  
    '''



    """
    #This function recognizes the entities present in text
    def entity_recognition(documents,client):
        '''
        Input: documents: list of strings, text on which entity recognition is to be performed
            client: Azure text analytics API client
        Output: list of categorized entities along with their meta data       
        '''
        try:
            # Use Text Analytics API client to recognize entitites from text
            result = client.recognize_entities(documents = documents)
            '''#Print the recognized entities along with their meta data
            print("Named Entities:\n")
            for entity in result.entities:
                print("\tText: ", entity.text, "\n\tCategory: ", entity.category, "\n\tSubCategory: ", entity.subcategory,
                        "\n\tConfidence Score: ", round(entity.confidence_score, 2)) ''' 
        except Exception as err:
            print("Encountered exception. {}".format(err))
        return [[entity.text for entity in item.entities if entity.category=='Person'] for item in result]

    """
    '''
    # This function removes the person description strings from list of strings
    def removed_personal_description(list_of_strings,company_name,threshold_for_entity_and_company_name_fuzzy_score=90):
        """
        Input: list_of_strings: list of strings from which person descriptions need to be removed
                company_name: string name of the company 
                threshold_for_entity_and_company_name_fuzzy_score
        Output:Non_person_description_strings: list of strings excluding the person description strings
        """
        client=authenticate_client()
        if client:
            # this collects all non person description strings from list_of_strings
            Non_person_description_strings = []
            chunked_list=chunkIt(list_of_strings,len(list_of_strings)//5+1)
            person_entities=[]
            for chunk in chunked_list:
                person_entities.extend(entity_recognition(chunk,client))
            
            assert len(list_of_strings)==len(person_entities)
            for i in range(len(list_of_strings)):
                
                # iterate over each entity in entities
                for entity in person_entities[i]:      
                        # find entity text's partial ratio with company name
                        fuzzy_score=fuzz.partial_ratio(entity,company_name)
                        # if any person entity that is not company name is present, the string is person description 
                        # so this would not be included in output list
                        if fuzzy_score <=threshold_for_entity_and_company_name_fuzzy_score:
                            break
                        else:
                            # remove person entities that are company names
                            person_entities[i].remove(entity)
                # if no person entities found in string, add the string to Non_person_description_strings          
                if len(person_entities[i])==0:
                    Non_person_description_strings.append(list_of_strings[i])
                else:
                    print(list_of_strings[i])
            return Non_person_description_strings        
        else:
            return list_of_strings

    '''


    # This function cleans the html page by removing html tags and
    # javascript snippets,lowercases the text, removes non_alpha numeric characters,
    # removes extra spaces , accented characters,stopwords and replaces numbers with words
    def clean_text(self,text,lowercase=True,white_spaces=True,remove_person_description=False,company_name=None):
        """
        Input: text: text to be cleaned
        Output: text: text after preprocessing
        """
        # Extract list of webpage text from soup if text is not string object 
        if not isinstance(text,(str,list)):
            for data in text(['style', 'script','a']):
            # Remove tags
                data.decompose()
            text=[text_content for text_content in text.stripped_strings]

        # Remove string control characters.
        text= [re.compile(r'[\n\r\t]').sub(" ", string) for string in text]

        # Lowercase the text
        if lowercase==True:
            text = [text_content.lower() for text_content in text]
        # remove whitespaces from text    
        if white_spaces==True:
            text=[self.collapse_white_spaces(string) for string in text]
        if remove_person_description:
            text=self.removed_personal_description(text,company_name)
            
        return text

    '''
    """Getting the text from images of webpage"""
    # This function returns the text of an image using 
    # pytesseract by taking image url as an input
    def azure_ocr(image_url):
        """
        Input: image_url: url of the image whose text
                        is to be extracted
        Output: text of the image or '' in case of 
                unsuccessful attempt 
        """
        try:
            data = {'url': image_url}
            response = requests.post(
            text_recognition_url, headers=headers, json=data)
            response.raise_for_status()

            # Extracting text requires two API calls: One call to submit the
            # image for processing, the other to retrieve the text found in the image.

            # Holds the URI used to retrieve the recognized text.
            operation_url = response.headers["Operation-Location"]

            # The recognized text isn't immediately available, so poll to wait for completion.
            analysis = {}
            poll = True
            while (poll):
                response_final = requests.get(
                    response.headers["Operation-Location"], headers=headers)
                analysis = response_final.json()
                time.sleep(1)
                if ("analyzeResult" in analysis):
                    poll = False
                if ("status" in analysis and analysis['status'] == 'failed'):
                    poll = False

            polygons=''
            if ("analyzeResult" in analysis):
                for line in analysis["analyzeResult"]["readResults"][0]["lines"]:
                    # Extract the recognized text, with bounding boxes.
                    polygons = polygons+' '+line["text"]
            return clean_text([polygons],lowercase=True,white_spaces=True)           
        except Exception as e:
            return ''
    '''

    '''
    # This function returns the text of an image using 
    # pytesseract by taking image url as an input
    def pytesseract_ocr(image_url):
        """
        Input: image_url: url of the image whose text
                        is to be extracted
        Output: text of the image or '' in case of 
                unsuccessful attempt 
        """
        try:
            # Send a GET request to the image_url.
            response = requests.get(image_url,verify = False)

            # Open Image in PIL
            img = Image.open(io.BytesIO(response.content))

            # Converting image to string using pytesseract
            text = pytesseract.image_to_string(img)
            return clean_text([text],lowercase=True,
                white_spaces=True)
        except Exception as e:
            return ''

    '''
    '''
    # This function collects all the image urls of the webpage 
    # and passes them to image_to_text function to finally get 
    # the text of all images on the webpage 
    def Website_image_text(url):
        """
        Input: page: soup object of the webpage
        Output: images: dictionary containing {filename: image text}
                        as entries
        """
        # Get the original webpage html content
        page = requests.get(url,verify=False)

        # convert the data received into searchable HTML
        extractedHtml = html.fromstring(page.content)

        # use an XPath query to find the image link (the 'src' attribute
        # of the 'img' tag).
        imageSrc = extractedHtml.xpath("//img/@src") 
    
        # Create empty images dictionary
        images=[]

        # Iterate over all images in imgSrc
        for image in imageSrc:
            if image.startswith("http"):
                # start with http, therefore take this as the full link
                imageLink = image
            else:
                if image.startswith('/')==False:
                    image='/'+image

                # does not start with http, therefore construct the full url 
                # from the base url plus the absolute image link
                imageLink = urljoin(url, image)

            # get the domain of our base url    
            base_url=urlsplit(url).netloc
            base_url=base_url.replace("www.", "")
            
            # skip images which dont have the same domain as the
            # main url
            if base_url not in imageLink:
                continue   
            
            # Extract file name from link   
            filename = imageLink.split("/")[-1] 
            
            # get the text of the image 
            image_text=azure_ocr(imageLink)
            #image_text=pytesseract_ocr(imageLink)
            
            # skip images with '' or ' ' as text
            if image_text==['']or image_text==[' ']:
                continue
            # create key value pair of filename and image text
            # in the images dictionary    
            images.extend(image_text) 
        return images
    '''

    '''
    # This function returns all the tables on the webpage
    def Website_tables(page):
        """
        Input: page: soup object of the page whose tables
                    are to be extracted
        Output: table_list: dictionary with entries 
                            {table_number:table as list of list}             
        """
        # Define the html contents of a URL.
        xhtml = page.decode('utf-8')

        # Define the HTMLTableParser object
        p = HTMLTableParser()
        
        # Feed the html contents in the
        # HTMLTableParser object
        p.feed(xhtml)
        
        # Create empty tables dictionary
        table_list=[]
        
        for i in range(0,len(p.tables)):
            #storing the obtained tables as list of lists in tables dictionary 
            table_list.append(p.tables[i])  
        return table_list
    '''

    #The function extracts the metadata namely title,description and keywords available on the webpage 
    def meta_data(self,soup):
        """
        Input: soup object of the page whose meta data 
                is required
        Output: metadata: metadata of the page        
        """
        metadata = []

        # Title of the webpage
        title = soup.title.string
        metadata.extend(self.clean_text([title],lowercase=True,
                                white_spaces=True))

        # Finding all meta tags
        meta = soup.find_all('meta')

        # Extracting description and keywords from meta tags
        for tag in meta:
            if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['description', 'keywords']:
                metadata.extend(self.clean_text([tag.attrs['content']],lowercase=True,
                                        white_spaces=True))
        return metadata
    # The function checks whether a string is composed
    # entirely of special characters
    def special_characters(self,s):
        """
        Input: s: string to be checked
        Output: True if string contains only special characters
                False if string contains characters other than special characters
        """
        if not re.match(r'^[_\W]+$', s):
            return True
        else:
            return False

    # This function uses the above functions to get all the 
    # content of a particular url
    def page_scraper(self,driver,url,company_name=None):
        """
        Input:
            url: URL of the page to be scraped
        Output:
            page_content,page_meta_data,page_table : page content contains list of website text and 
                                                            text from images(if OCR performed),
                                                            page_meta_data contains list of meta data text from website 
                                                            and page_table contains tables from webpage
            else '','',[] in case of unsuccessful attempt
        """
        # Create empty page_content dictionary

        try:
            print(url)
            #driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,chrome_options=chrome_options)
            #driver = webdriver.Chrome(chrome_options=chrome_options)
            
            # Get the entire html page of url, code = 0 means successfull retrieval of page
            code,page,true_url = self.html_page(driver,url)
            if code==0:
                #text=driver.find_element_by_tag_name("body").text.split('\n')
                # Clean obtained page
                cleantext=self.clean_text(page,lowercase=True,white_spaces=True,remove_person_description=False,company_name=company_name)
                
                
                # Add key value pairs for meta_data, text, image and tables of page in page_content
                Image_counter = False
                if Image_counter:
                    page_content=(cleantext+self.Website_image_text(url))                    
                    page_meta_data=self.meta_data(page)
                else:
                    page_content=(cleantext)
                    page_meta_data=self.meta_data(page)

                page_content=list(filter(None, page_content))            
                page_content=[value for value in page_content if self.special_characters(value)]
                
                page_meta_data=list(filter(None, page_meta_data))            
                page_meta_data=[value for value in page_meta_data if self.special_characters(value)] 
                #page_table=Website_tables(page)
                #driver.close()
            else:
                print("Couldn't scrape " + url)
                page_content=''
                page_meta_data=''
                #page_table=[]            

        except Exception as e:
            print("Couldn't scrape " + url)
            page_content=''
            page_meta_data=''
            #page_table=[] 
            print('Error: '+str(e))   
        #return page_content,page_meta_data,page_table
        return page_content,page_meta_data

    # This function saves the directory structure of the website
    # in a scraped_log file
    def directory_logger(self,url,links):
        """
        Input:
            url: main URL of website
            links: directory of the website    
        """
        # create the key value pair of url and the links present
        directory={url:links}

        # open the scraper_log.txt file in append mode
        file = open("scraper_log.txt", "a")
        
        # append the directory in the file 
        file.write(str(directory))

        # add a new line to the file
        file.write('\n') 

        # close the file
        file.close()

    # This functions combines the above functions to get the 
    # content of all the required pages of a website
    def website_scraper(self,url,company_name=None):
        """
        Input: 
            url: URL of the website to be scraped
        Output:
            webpage_content: scraped content of website
            sitemap: sitemap keywords of website
            meta_data_content: metadata content of website
            table_data:tables of pages scraped in the website
            flag: True if there were relevant matched pages found
                False if no relevant pages were found        
        """
        driver = webdriver.Chrome(executable_path=self.CHROMEDRIVER_PATH,chrome_options=chrome_options)
        print(url)
        #driver = webdriver.Chrome(chrome_options=chrome_options)
        # Get all links in Homepage
        links_website,sitemap,flag=self.website_links(driver,url)
        print("links_website")
        # flag=None denotes unsuccessful extraction of website links
        if flag== None:
            driver.close()
        
            return '','Failed'
        else:  
            if flag==False:
                # add entire website directory to log file
                self.directory_logger(url,links_website)
                links_website={url}  
            website_data=[]
            #table_data=[]
            meta_data_content=[]
            # iterate over all links
            for link in links_website:
                #page_content,page_meta_data,tables=page_scraper(link)
                page_content,page_meta_data=self.page_scraper(driver,link,company_name=company_name)
                if page_content not in [None,[]]:
                        website_data.extend(page_content)
                #if tables not in [None,[]]:
                #        table_data.extend(tables)        
                if page_meta_data not in [None,[]]:
                        meta_data_content.extend(page_meta_data)
                print(link)
            driver.quit()
            
            #return website_data,sitemap,meta_data_content,table_data,flag
            return website_data,sitemap,meta_data_content,flag
        
    # This function returns a dictionary containing all the data of a company    
    def complete_data(self,data_dictionary):
        """
        Input: data_dictionary: dictionary of data of one company
        Output: data_dictionary: dictionary with all the data for the company
        """
        #scraped_data,sitemap,web_meta_data,table_data,flag=website_scraper(data_dictionary['company_url'])4
        web_data,sitemap,web_meta_data,flag=self.website_scraper(data_dictionary['company_url'],company_name=data_dictionary['company_name'])

        # remove all empty strings from lists and add to the dictionary with appropriate key    
        data_dictionary['web_data']=web_data
        #data_dictionary['web_table']=table_data
        data_dictionary['sitemap']=list(filter(None, sitemap))
        data_dictionary['meta_data']=web_meta_data
        # If there is no data in keys with scraped data the put flag='Failed'
        if  data_dictionary['web_data']==[] and  data_dictionary['sitemap']==[] and data_dictionary['meta_data']==[]:
            flag='Failed'
            print(flag)
        data_dictionary['scraping_counter']=flag
        return data_dictionary
