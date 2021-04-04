from lxml import html
import requests
import unicodecsv as csv
import argparse
import json
import io

class ComparableHouse:
   #def __init__(self,prop_num, address,price,bedrooms,bathrooms,area,url):
    def __init__(self,house):
        for k,v in house.items():
            setattr(self, k, v)
        

     #self.prop_num = prop_num
     #self.address = address
     #self.price = price
     #self.bedrooms = bedrooms
     #self.bathrooms = bathrooms
     #self.area = area
     #self.url = url

def clean(text):
    if text:
        return ' '.join(' '.join(text).split())
    return None


def get_headers():
    # Creating headers.
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
    return headers





def save_to_file(response):
    # saving response to `response.html`

    with io.open("response.html", 'w', encoding="utf-8") as fp:
        fp.write(response.text)


def write_data_to_csv(data):
    # saving scraped data to csv.

    with open("properties-%s.csv" % (zipcode), 'wb') as csvfile:
        fieldnames = ['title', 'address', 'city', 'state', 'postal_code', 'price','bedrooms','bathrooms','area', 'facts and features', 'real estate provider', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def get_response(url):
    # Getting response from zillow.com.

    for i in range(5):
        response = requests.get(url, headers=get_headers())
        print("status code received:", response.status_code)
        if response.status_code != 200:
            # saving response to file for debugging purpose.
            save_to_file(response)
            continue
        else:
            save_to_file(response)
            return response
    return None

def get_data_from_json(raw_json_data):
    # getting data from json (type 2 of their A/B testing page)

    cleaned_data = clean(raw_json_data).replace('<!--', "").replace("-->", "")
    properties_list = []

    try:
        json_data = json.loads(cleaned_data)
        search_results = json_data.get('cat1').get('searchResults').get('listResults', [])
        x = 1
        for properties in search_results:
            prop_num = x
            address = properties.get('address')
            property_info = properties.get('hdpData', {}).get('homeInfo')
            price = properties.get('price')
            bedrooms = properties.get('beds')
            bathrooms = properties.get('baths')
            area = properties.get('area')
            property_url = properties.get('detailUrl')
            title = properties.get('statusText')
            data = {'prop_num' : prop_num,
                    'address': address,
                    'price': price,
                    'bedrooms': bedrooms,
                    'bathrooms': bathrooms,
                    'area': area,
                    'url': property_url
                    }
            properties_list.append(data)
            x+=1
        return properties_list

    except ValueError:
        print("Invalid json")
        return None


def parse(zipcode):
    url = "https://www.zillow.com/homes/for_sale/{0}_rb/?fromHomePage=true&shouldFireSellPageImplicitClaimGA=false&fromHomePageTab=buy".format(zipcode)
    response = get_response(url)

    if not response:
        print("Failed to fetch the page, please check `response.html` to see the response received from zillow.com.")
        return None

    parser = html.fromstring(response.text)
    search_results = parser.xpath("//div[@id='search-results']//article")

    if not search_results:
        print("parsing from json data")
        # identified as type 2 page
        raw_json_data = parser.xpath('//script[@data-zrr-shared-data-key="mobileSearchPageStore"]//text()')
        return get_data_from_json(raw_json_data)

    print("parsing from html page")
    properties_list = []
    x=0
    for properties in search_results:
        raw_address = properties.xpath(".//span[@itemprop='address']//span[@itemprop='streetAddress']//text()")
        raw_price = properties.xpath(".//span[@class='zsg-photo-card-price']//text()")
        raw_info = properties.xpath(".//span[@class='zsg-photo-card-info']//text()")
        url = properties.xpath(".//a[contains(@class,'overlay-link')]/@href")

        address = clean(raw_address)
        price = clean(raw_price)
        info = clean(raw_info).replace(u"\xb7", ',')
        broker = clean(raw_broker_name)
        title = clean(raw_title)
        property_url = "https://www.zillow.com" + url[0] if url else None
        is_forsale = properties.xpath('.//span[@class="zsg-icon-for-sale"]')
        

        properties = {'address': address,
                      'city': city,
                      'state': state,
                      'price': price,
                      'url': property_url,}
        if is_forsale:
            properties_list.append(properties)
    return properties_list


def find_comparables_by_zip(zipcode):
    print ("Fetching data for %s" % (zipcode))
    scraped_data = parse(zipcode)
    comparables = []
    if scraped_data:
        
        house1 = ComparableHouse(scraped_data[0])
        house2 = ComparableHouse(scraped_data[1])
        house3 = ComparableHouse(scraped_data[2])
        house4 = ComparableHouse(scraped_data[3])
        house5 = ComparableHouse(scraped_data[4])
        house6 = ComparableHouse(scraped_data[5])
        house7 = ComparableHouse(scraped_data[6])
        house8 = ComparableHouse(scraped_data[7])
        house9 = ComparableHouse(scraped_data[8])
        comparables.append(house1)
        comparables.append(house2)
        comparables.append(house3)
        comparables.append(house4)
        comparables.append(house5)
        comparables.append(house6)
        comparables.append(house7)
        comparables.append(house8)
        comparables.append(house9)
        return comparables
        
        print (comparables)
    



