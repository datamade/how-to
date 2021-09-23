# 🗺 Mapping, the DataMade way

Maps are flexible and widely understood tools that we use to visualize data.

In order to put together any sort of map (except an SVG map!), you need to make sure you have GeoJSON for any geographies you will want to display. GeoJSON is a JSON format for encoding geographical data. The [GeoJSON website](http://geojson.org) has a reliable example of what this format must look like. For a deeper dive into the format, [this blog](https://macwright.com/2015/03/23/geojson-second-bite.html) post is a good place to start.

Having this information, the next step is to decide what kind of functionality you will need your map to have:
* Need a slippy map, also known as a tiled map? Use [Leaflet](/mapping/leaflet.md)
* Are you planning to use React to render your front-end? Pay special attention to the nuances of [React-Leaflet](/mapping/react-leaflet.md)
* Will you be using custom geographies? Use Leaflet together with PostGIS
* Do you need to show information for geographical features like stores or parks? Make sure to use [Google APIs maps and geocoding](/mapping/google-apis.md)
* If you don’t need a slippy map, don’t need to display geographical features, and you have access to an SVG file of the geographies you will be using, implementing an [SVG map](/mapping/svg-maps.md) is a good choice
