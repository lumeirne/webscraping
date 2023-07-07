#import necessary libraries make sure that they are installed
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

# function to get Product Name
def getProductName(soup):
    try:
        name = soup.find('span', attrs={"id": 'productTitle'}).text.strip()
    except AttributeError:
        name = ''

    return name

#to get product price
def getProductPrice(soup):
    try:
        price = soup.find('span', attrs={'class': 'a-price-whole'}).text.strip()
    except AttributeError:
        price = ''

    return price

#to get rating
def getProductRating(soup):
    try:
        rating = soup.find('span', attrs={'class': "a-icon-alt"}).text.strip()
    except AttributeError:
        rating = ''

    return rating

#to find the number of reviews
def getNumberofReviews(soup):
    try:
        numofreviews = soup.find('span', {'class': 'a-size-base'}).text.strip()
        numbers = re.findall(r'\d+', numofreviews)
        num = ''
        for i in numbers:
            num += i

        totalnumber = int(num)
    except AttributeError:
        totalnumber = ''

    return totalnumber

#to get manufacturer
def getManufacturer(soup):
    # Find the element with "Manufacturer" label
    manufacturer_element = soup.find('span', class_='a-text-bold', string=re.compile(r'Manufacturer'))

    if manufacturer_element:
        # Get the text of the next sibling element
        manufacturer = manufacturer_element.next_sibling.next_sibling.text.strip()
    else:
        manufacturer = ''

    return manufacturer

# to get ASIN
def getASIN(soup):
    # Find the element with "ASIN" label
    asin_element = soup.find('span', class_='a-text-bold', string=re.compile(r'ASIN'))

    if asin_element:
        # Get the text of the next sibling element
        asin = asin_element.next_sibling.next_sibling.text.strip()
    else:
        asin = ''

    return asin

# to get Description
def getProdDescription(soup):
    description_element = soup.find('div', id='productDescription')

    if description_element:
        # Get the text of the first <span> element inside the description
        description = description_element.find('span').text.strip()
    else:
        description = ''

    return description

# main function to scrape the data
def ScrapeData():
  
    url = input('Enter the url: ')
    # Set headers to mimic a web browser
    Headers = ({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    })

    # Send a GET request to the URL
    pageResponse = requests.get(url, headers=Headers)

    # Create a BeautifulSoup object from the page content
    soup = BeautifulSoup(pageResponse.content, 'html.parser')

    # Find all the links on the page
    links = soup.findall('a', attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style'})

    productURLS = []

    # Extract the href attribute of each link and store the complete URL in productURLS list
    for link in links:
        getLinkhref = link.get('href')
        productURLS.append('https://www.amazon.in' + getLinkhref)

    productName = []
    productPrice = []
    productRating = []
    noOfReviews = []
    productManufacturer = []
    productASIN = []
    productDescription = []

    # Iterate over each product URL
    for lnks in productURLS:
        # Send a GET request to the product URL
        page = requests.get(lnks, headers=Headers)
        soupPage = BeautifulSoup(page.content, 'html.parser')

        # Extract the product details using the defined functions
        productName.append(getProductName(soupPage))
        productPrice.append(getProductPrice(soupPage))
        productRating.append(getProductRating(soupPage))
        noOfReviews.append(getNumberofReviews(soupPage))
        productManufacturer.append(getManufacturer(soupPage))
        productASIN.append(getASIN(soupPage))
        productDescription.append(getProdDescription(soupPage))

    # Create a dictionary to store the scraped data
    scrapedData = {}
    scrapedData['Product URL'] = productURLS
    scrapedData['Product Name'] = productName
    scrapedData['Manufacturer'] = productManufacturer
    scrapedData['ASIN'] = productASIN
    scrapedData['Description'] = productDescription
    scrapedData['Product Price'] = productPrice
    scrapedData['Product Rating'] = productRating
    scrapedData['Number of Reviews'] = noOfReviews

    # Convert the dictionary to a DataFrame
    productDetailsdf = pd.DataFrame(scrapedData)

    # Save the DataFrame to a CSV file
    productDetailsdf.to_csv('Product Details.csv', index=False)

    return productDetailsdf


content = ScrapeData()
print(content)