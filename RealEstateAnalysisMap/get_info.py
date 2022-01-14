import requests
from bs4 import BeautifulSoup
from RealEstateAnalysisMap.create_url import create_url

# Create a dictionary of address:price listings for all houses/condos in zip
def get_house_info(zip_code):
    house_info = {} # Create empty dictionary
    page_number = 1 # Starting page number
    loop = True
    # Create a loop that will call all pages of a search and add to dictionary
    while loop == True:
        url = create_url(page_number, zip_code)
        r = requests.get(url)

        # Find all address and prices on search URL
        page = BeautifulSoup(r.text, 'html.parser')

        if page.findAll('div', {'data-testid':'srp-no-results-message'}):
            break

        #print(r.status_code)
        address_info = page.findAll('div', {'data-testid':'property-address'})
        pricing_info = page.findAll('div', {'data-testid':'property-price'})

        # Add each address and price on the page to the dictionary
        for address, price in zip(address_info, pricing_info):
            address = address.text
            price = int(price.text.strip('+$,').replace(',',''))

            # Don't include houses that are not applicable based on...
            # House is new construction, doesn't have address
            if address.startswith('PCI'):
                continue
            # House is not in requested zip code
            elif not address.endswith(str(zip_code)):
                loop = False
                break

            house_info[address] = price

        page_number+=1

    return house_info
