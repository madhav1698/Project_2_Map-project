import folium
import pandas as pd
import json
 
data = pd.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

def color_producer(elevation):
    if elevation<1000:
        return "green"
    elif 1000<=elevation <3000:
        return "orange"
    else:
        return "red"
 
html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""
 
map = folium.Map(location=[38.58, -99.09], zoom_start=5, tiles="Stamen Toner") #coordinates of usa
fgp= folium.FeatureGroup(name = "Population")

fgp.add_child(folium.GeoJson(data=(open("world.json","r",encoding="utf-8-sig").read()),
style_function=lambda x: {"fillColor":"green" if x["properties"]["POP2005"]<100000 
else "orange" if 1000000<= x["properties"]["POP2005"] < 20000000 else "red"})) #choosing color depemnding on population density

fgv=folium.FeatureGroup(name="Volcanoes")
for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html= html % (name, name, el), width=200, height=100) #only for html 
    fgv.add_child(folium.CircleMarker(location=[lt, ln],radius=8, popup=folium.Popup(iframe), icon = folium.Icon(color = "green"),
    fill_color=color_producer(el),color="grey",fill_opacity=.7)) #adding marker and showing lat and lon as we hover or click

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map_html_popup_advanced.html")





