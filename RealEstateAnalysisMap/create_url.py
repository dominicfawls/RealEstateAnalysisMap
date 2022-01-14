# Function to create nicely formatted URL for retrieving information
def create_url(number, zip_code):
    if number == 1:
        url = 'https://www.trulia.com/for_sale/' + str(zip_code) + \
            '_zip/fsbo,resale_lt/'
    else:
        url = 'https://www.trulia.com/for_sale/' + str(zip_code) + \
            '_zip/fsbo,resale_lt/' + str(number) +'_p/'
    return url

#/SINGLE-FAMILY_HOME_type/
