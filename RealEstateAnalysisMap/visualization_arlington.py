import folium
import branca
import geopandas as gpd

def create_map(mapped_feature, map_title, map_json_file, num_zip_codes):

    map_file = gpd.read_file(map_json_file)
    map_file = map_file[['ZCTA5CE10', 'average_cost', 'average_cost_str',
        'number_for_sale', 'geometry']]

    map = folium.Map(location = [38.879890, -77.107558], zoom_start = 12)

    avg_colormap = branca.colormap.LinearColormap(
        colors=['#FFFFFF','#F3FC35','#FB6814','#F21005', '#CF0000'],
        vmin=map_file['average_cost'].min(),
        vmax=map_file['average_cost'].max()
        ).scale(300000, 2000000)
    avg_colormap.caption = 'Average Cost - Scale'

    num_colormap = branca.colormap.LinearColormap(
        colors=['#FFFFFF','#F3FC35','#12E05A'], #['yellow', 'orange', 'red']
        vmin=map_file['number_for_sale'].min(),
        vmax=map_file['number_for_sale'].max()
        ).scale(1,60)
    num_colormap.caption = 'Number of Houses on Market - Scale'

    averages_map = folium.GeoJson(
        map_file,
        name = 'House Cost Averages',
        style_function=lambda x: {
            'fillColor':avg_colormap(x['properties']['average_cost']),
            'color': 'black',
            'weight': .5,
            'fillOpacity': .6,
            'caption': 'Average House For Sale Cost'
        },
        control=True,
        overlay=True,
        show=True,
        highlight_function=lambda x: {
            'fillColor': '#000000',
            'color': '#000000',
            'fillOpacity': .5,
            'weight': .1
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['ZCTA5CE10', 'average_cost_str', 'number_for_sale'],
            aliases=['Zip Code', 'Average House Cost',
                'Number of Houses for Sale'],
            style=("background-color: white; color: #333333;")
                + ("font-family: arial; font-size: 12px; padding: 10px;"),
        )
    )

    num_for_sale_map = folium.GeoJson(
        map_file,
        name = 'Number of Houses on Market',
        style_function=lambda x: {
            'fillColor':num_colormap(x['properties']['number_for_sale']),
            'color': 'black',
            'weight': .5,
            'fillOpacity': .6,
            'caption': 'Number of Houses on Market'
        },
        control=True,
        overlay=True,
        show=False,
        highlight_function=lambda x: {
            'fillColor': '#000000',
            'color': '#000000',
            'fillOpacity': .5,
            'weight': .1
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['ZCTA5CE10', 'average_cost_str', 'number_for_sale'],
            aliases=['Zip Code', 'Average House Cost',
                'Number of Houses for Sale'],
            style=("background-color: white; color: #333333;")
                + ("font-family: arial; font-size: 12px; padding: 10px;"),
        )
    )

    avg_colormap.add_to(map)
    num_colormap.add_to(map)
    map.add_child(averages_map)
    map.add_child(num_for_sale_map)
    folium.LayerControl().add_to(map)
    map.save(outfile = map_title)
