from zip_map_file_arlington import create_zip_file
from get_info import get_house_info
from visualization_arlington import create_map
import json

arlington_zips = [
    '22201',
    '22202',
    '22203',
    '22204',
    '22205',
    '22206',
    '22207',
    '22209',
    '22213'
    ]

# Create JSON file using create_zip_file function
create_zip_file(arlington_zips)

# Create dictionaries to house relevant information
arlington_dict = {}
average_dict = {}
number_for_sale_dict = {}

# Get data from Trulia for each zip code using get_house_info function
for zip_code in arlington_zips:
    arlington_dict[zip_code] = get_house_info(int(zip_code))
print('Retrieved information for ' + str(len(arlington_dict)) + ' zip codes\n')

# Sort collected data from above into created dictionaries
for zip_code, zip_dict in arlington_dict.items():
    try:
        values = zip_dict.values()
        values_list = list(values)
        average = sum(values_list) / len(values_list) #Calculate avg house cost
        average_dict[zip_code] = int(average)
        number_for_sale_dict[zip_code] = len(zip_dict)
    except ZeroDivisionError:
        continue
print('Calculated averages for ' + str(len(average_dict)) + ' zip codes\n\n')

# Add collexted data to JSON file for easy mapping
with open(r'arlington_zips.json') as json_file:
    geo_json_dict = json.load(json_file)
    for zip_code_dict in geo_json_dict['features']:
        if zip_code_dict['properties']['ZCTA5CE10'] in average_dict.keys():
            zip_code_dict['properties']['average_cost'] = \
                average_dict[zip_code_dict['properties']['ZCTA5CE10']]
            zip_code_dict['properties']['average_cost_str'] = \
                "${:,}".format(zip_code_dict['properties']['average_cost'])
            zip_code_dict['properties']['number_for_sale'] = \
                number_for_sale_dict[zip_code_dict['properties']['ZCTA5CE10']]

with open('arlington_zips.json', 'w') as json_file:
    json.dump(geo_json_dict, json_file)

# Create a choropleth map using create_map function
create_map(
    mapped_feature = 'Average Cost',
    map_title = 'arlington_map.html',
    map_json_file = 'arlington_zips.json',
    num_zip_codes = len(arlington_zips),
    )
