import folium

KEY = "2EFwrr14ACvBDfJt4K0j"
STIJL = "dataviz"  

colours = [
    "darkslategray", "crimson", "salmon", "saddlebrown", "peru",
    "darkorange", "goldenrod", "khaki", "olivedrab", "mediumseagreen",
    "forestgreen", "teal", "cadetblue", "skyblue", "steelblue",
    "navy", "slateblue", "mediumpurple", "orchid", "palevioletred",
]
            
winkels =  {
            "Rotterdam": (51.9225, 4.479167),
            "Leiden": (52.158333, 4.493056),
            "Den Haag": (52.0705, 4.3007),
            "Delft": (52.006667, 4.355556),
            "Breda": (51.5888, 4.7760),
            "Utrecht": (52.0907, 5.1214),
            "Amsterdam": (52.3676, 4.9541)
}

def maak_kaart():
    return folium.Map(
        location=[52.1326, 5.2913],
        zoom_start=7,
        tiles=f"https://api.maptiler.com/maps/{STIJL}/{{z}}/{{x}}/{{y}}.png?key={KEY}",
        attr=(
            '© <a href="https://www.maptiler.com/copyright/">MapTiler</a> '
            '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>'
        ),
    )


class OSMVis:

    def kaart(self, tours, alle_coordinaten, ftld, rd):
        kaart = maak_kaart()  
        legend_dict = {}
        stedenlijst = ['Depot', 'Rotterdam', 'Leiden', 'Den Haag', 'Delft', 'Breda', 'Utrecht', 'Amsterdam']
        for i, tour in enumerate(tours):
            tour_coordinates = alle_coordinaten[tour]
            lats, lons = tour_coordinates[:, 0], tour_coordinates[:, 1]
            color = colours[i % len(colours)]  

            folium.PolyLine(
                locations=list(zip(lats, lons)),
                color=color,
                weight=2,
                opacity=0.8,
                tooltip=f"Tour {i}",
            ).add_to(kaart)
            
            for lat, lon in zip(lats, lons):
                folium.CircleMarker(
                    location=(lat, lon),
                    radius=4,
                    color=color,
                    fill=True,
                    fill_color=color,
                ).add_to(kaart)
            legend_dict[i] = color
            for j in tour:
                if j != 0:
                    stad = stedenlijst[j]
                    full_truck_load = int(ftld.get(stad))
                    remainder = int(rd.get(stad))
                    lat, lon = winkels.get(stad)
            
                    folium.Marker(
                        location=(lat, lon),
                        icon=folium.DivIcon(
                            icon_size=(150, 20),
                            icon_anchor=(-5, 25),   # 5 px rechts, 25 px boven het punt
                            html=f"""
                            <div style="font-size: 10pt; color: {color}; font-weight: bold;
                                        white-space: nowrap;">
                                        {full_truck_load} FTL, {remainder} rest
                            </div>
                            """
                        ),
                    ).add_to(kaart)
                    
                
            
                    
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