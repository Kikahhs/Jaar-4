import folium

KEY = "2EFwrr14ACvBDfJt4K0j"
STIJL = "dataviz"  

colours = [
    "darkslategray", "crimson", "salmon", "saddlebrown", "peru",
    "darkorange", "goldenrod", "khaki", "olivedrab", "mediumseagreen",
    "forestgreen", "teal", "cadetblue", "skyblue", "steelblue",
    "navy", "slateblue", "mediumpurple", "orchid", "palevioletred",
]


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

    def kaart(self, tours, alle_coordinaten):
        kaart = maak_kaart()  
        legend_dict = {}

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