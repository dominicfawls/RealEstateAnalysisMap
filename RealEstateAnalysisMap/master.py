from RealEstateAnalysisMap.zip_map_file import create_zip_file_nova
from RealEstateAnalysisMap.zip_map_file_arlington import create_zip_file_arlington
from RealEstateAnalysisMap.get_info import get_house_info
from RealEstateAnalysisMap.visualization import create_map
from RealEstateAnalysisMap.visualization_arlington import create_map_arlington
import json

# This master file contains the contents of the two main files
# (arlington_va_average and fairfax_arlington_average)
# but converts the contents into easily useable functions
# for package use.

# Function to create Northern Virginia Map (from fairfax_arlington_average.py)
def create_nova_map():
    nova_zips_int = [
        22030,
        20171,
        22003,
        22033,
        22031,
        20120,
        22015,
        22102,
        20170,
        22042,
        22306,
        22079,
        22312,
        20191,
        22309,
        22101,
        22315,
        22310,
        22041,
        20190,
        22153,
        22152,
        20121,
        22180,
        22182,
        22032,
        22043,
        22150,
        22311,
        22303,
        20151,
        22046,
        22124,
        22066,
        22039,
        22151,
        20194,
        22044,
        22181,
        20124,
        22308,
        22307,
        22060,
        22027,
        22201,
        22202,
        22203,
        22204,
        22205,
        22206,
        22207,
        22209,
        22213,
        22314,
        22301,
        22302,
        22304,
        22305,
        22311,
        22312
        ]

    # Converts nova_zips_int to list of strings
    nova_zips = []
    for zip_code in nova_zips_int:
        nova_zips.append(str(zip_code))

    # Create JSON file of zip code information from master VA file
    create_zip_file_nova(nova_zips)
    print('Gathering Northern Virginia Map Data')
    # Create dictionaries to house relevant information
    nova_dict = {}
    average_dict = {}
    number_for_sale_dict = {}

    # Get data from Trulia for each zip code using get_house_info function
    for zip_code in nova_zips:
        nova_dict[zip_code] = get_house_info(int(zip_code))
    print('Retrieved information for ' + str(len(nova_dict)) + ' zip codes\n\n')

    # Sort collected data from above into created dictionaries
    for zip_code, zip_dict in nova_dict.items():
        try:
            values = zip_dict.values()
            values_list = list(values)
            average = sum(values_list) / len(values_list) #Calculate avg house cost
            average_dict[zip_code] = int(average)
            number_for_sale_dict[zip_code] = len(zip_dict)
        except ZeroDivisionError:
            continue
    print('Calculated averages for ' + str(len(average_dict)) + ' zip codes\n\n')

    # Add collected data to JSON file for easy mapping
    with open(r'fairfax_arlington_zips.json') as json_file:
        geo_json_dict = json.load(json_file)
        for zip_code_dict in geo_json_dict['features']:
            if zip_code_dict['properties']['ZCTA5CE10'] in average_dict.keys():
                zip_code_dict['properties']['average_cost'] = \
                    average_dict[zip_code_dict['properties']['ZCTA5CE10']]
                zip_code_dict['properties']['average_cost_str'] = \
                    "${:,}".format(zip_code_dict['properties']['average_cost'])
                zip_code_dict['properties']['number_for_sale'] = \
                    number_for_sale_dict[zip_code_dict['properties']['ZCTA5CE10']]

    with open('fairfax_arlington_zips.json', 'w') as json_file:
        json.dump(geo_json_dict, json_file)

    # Create a choropleth map using create_map function
    create_map(
        mapped_feature = 'Average Cost',
        map_title = 'fairfax_arlington_map.html',
        map_json_file = 'fairfax_arlington_zips.json',
        num_zip_codes = len(nova_zips_int)
        )
    print("Map has been created.\n\n")

# Function to create Arlington Map (from arlington_va_average.py)
def create_arlington_map():
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
    create_zip_file_arlington(arlington_zips)

    # Create dictionaries to house relevant information
    arlington_dict = {}
    average_dict = {}
    number_for_sale_dict = {}

    # Get data from Trulia for each zip code using get_house_info function
    for zip_code in arlington_zips:
        arlington_dict[zip_code] = get_house_info(int(zip_code))
    print('Retrieved information for ' + str(len(arlington_dict)) + ' zip codes\n\n')

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
    create_map_arlington(
        mapped_feature = 'Average Cost',
        map_title = 'arlington_map.html',
        map_json_file = 'arlington_zips.json',
        num_zip_codes = len(arlington_zips),
        )
    print("Map has been created.\n\n")
