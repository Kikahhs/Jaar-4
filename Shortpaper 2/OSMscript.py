import folium

import os
 
KEY = "2EFwrr14ACvBDfJt4K0j"

STIJL = "dataviz"  # verander dit naar een andere stijl
 
# Kaart centreren op Nederland

kaart = folium.Map(location=[52.1326, 5.2913], 

                   zoom_start=7, 

                   tiles=f"https://api.maptiler.com/maps/{STIJL}/{{z}}/{{x}}/{{y}}.png?key={KEY}",

                   attr='© <a href="https://www.maptiler.com/copyright/">MapTiler</a> © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>',

)
colours = [
    "darkslategray",
    "crimson",
    "salmon",
    "saddlebrown",
    "peru",
    "darkorange",
    "goldenrod",
    "khaki",
    "olivedrab",
    "mediumseagreen",
    "forestgreen",
    "teal",
    "cadetblue",
    "skyblue",
    "steelblue",
    "navy",
    "slateblue",
    "mediumpurple",
    "orchid",
    "palevioletred",
]

class OSMVis:
    
    def kaart(self, tours, alle_coordinaten):
        legend_dict = {}
        
        for tour in range(len(tours)):
        
            tour_coordinates = alle_coordinaten[tours[tour]]
         
            y0, x0 = tour_coordinates[:, 0], tour_coordinates[:, 1]
         
            color = colours[tour]
         
            folium.PolyLine(
        
                locations=list(zip(y0, x0)),  # (lat, lon)
        
                color=color,
        
                weight=2,
        
                opacity=0.8,
        
                tooltip=f"Tour {tour}",
        
            ).add_to(kaart)
         
            for lat, lon in zip(y0, x0):
        
                folium.CircleMarker(
        
                    location=(lat, lon),
        
                    radius=4,
        
                    color=color,
        
                    fill=True,
        
                    fill_color=color,
        
                ).add_to(kaart)
         
            dn = {tour: color}
        
            legend_dict = {**legend_dict, **dn}
         
        legend_html = """
        <div style="position: fixed; bottom: 30px; left: 30px; z-index: 9999;
        
                    background: white; padding: 10px; border: 1px solid grey;
        
                    border-radius: 5px; font-size: 14px;">
        <b>Routes</b><br>
        
        """
        
        for tour, color in legend_dict.items():
        
            legend_html += (
        
                f'<span style="background:{color}; display:inline-block; '
        
                f'width:12px; height:12px; margin-right:6px;"></span>Route {tour}<br>'
        
            )
        
        legend_html += "</div>"
         
        kaart.get_root().html.add_child(folium.Element(legend_html))
        
        return kaart
    
     