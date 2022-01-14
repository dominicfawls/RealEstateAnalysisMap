import json

def create_zip_file(nova_zips):
    # Remove all zip codes from JSON except for Arlington/Fairfax Co./Alexandria
    # Load GeoJSON
    with open('va_virginia_zip_codes_geo.min.json', 'r') as zip_map_file:
        map_data = json.load(zip_map_file)

    # Sort out only information for zips in list above, add to new_features_list
    new_features_list = []
    delete_zip_index = 0
    for zip_dict in map_data['features']:
        if zip_dict['properties']['ZCTA5CE10'] in nova_zips:
            new_features_list.append(zip_dict)

    # Add new features to a new JSON file
    new_json = dict.fromkeys(['type', 'features'])
    new_json['type'] = 'FeatureCollection'
    new_json['features'] = new_features_list

    # Add new properties to zip code to house information found later
    for zip_item in new_json['features']:
        zip_item['properties']['average_cost'] = ''
        zip_item['properties']['average_cost_str'] = ''
        zip_item['properties']['number_for_sale'] = ''

    # Save JSON as updated_file
    open("fairfax_arlington_zips.json", "w").write(
        json.dumps(new_json, sort_keys=True, indent=4, separators=(',', ': '))
    )
