from turtle import color
import folium
import pandas as pd

df = pd.read_excel('cl_dataset.xlsx', index_col=0)

lat = list(df['lat'])
lon = list(df['long'])
easl = list(df['Altitud'])

# name = list(df['Nombre'])

def gen_color(elevacion):
  if elevacion > 6000:
    return 'black'
  elif 4500 <= elevacion <= 6000:
    return 'darkred'
  elif 3000 <= elevacion < 4500:
    return 'red'
  elif 1500 <= elevacion < 3000:
    return 'orange'
  else:
    return 'green'

map = folium.Map(location=[-41.10, -72.50], zoom_start=10, tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name="Volcanes")


for lt, ln, el in zip(lat, lon, easl):
  # jic: popup = folium.Popup(str(var),parse_html=True)
  fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=6, popup=str(el)+" msnm", 
                                    fill_color=gen_color(el), color='grey', fill_opacity=0.7))
  

# df_json = pd.read_json("chile.json")
# reg_data = list(df_json['properties']["NOM_REG"])

fgp = folium.FeatureGroup(name="Población")

fgp.add_child(folium.GeoJson(data=open("chile.json", 'r', encoding='utf-8-sig').read(),
               style_function=lambda x: {'fillColor':'green' if x['properties']['POBL2010'] < 1000000
                                         else 'orange' if 1000000 <= x['properties']['POBL2010'] < 2000000
                                         else 'red'})
)

map.add_child(fgv)
map.add_child(fgp)

map.add_child(folium.LayerControl())

map.save("TestMap.html")

