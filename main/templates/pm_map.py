import folium
import pandas as pd
from folium.plugins import HeatMap

# Load the data
data = pd.read_excel("C:/Users/johns/OneDrive/Documents/Desktop/PFAS_Web/pm_coords.xlsx")

# Initialize the map centered around North Carolina
m = folium.Map(location=[35.7596, -79.0193], zoom_start=7)

# Prepare the data for the heatmap
heat_data = [[row['lat'], row['lng'], row['pm']] for index, row in data.iterrows()]

# Add the heatmap layer
HeatMap(heat_data,radius=15, blur=20).add_to(m)

# Save the map to an HTML file
m.save('pm_heatmap.html')


