# Mapping with MapLibre and PMTiles

## Introduction to mapping with vector tiles

## MapLibre vs MapBox

MapLibre is a fork of the formerly open-source, now proprietary Mapbox library. Mapbox’s main value proposition is easy integration with their paid services such as vector tile hosting and their basemap styling software, Mapbox Studio. 

However, we can host our own tiles and use open source basemap styling software with MapLibre. This is, of course, cheaper while also allowing us to have complete control over our map’s styling, our data pipeline, and where our data lives.

## PMTiles and its uses

One of the most attractive features of MapLibre is its easy integration with PMTiles vector files. PMTiles is a file format 

Vector tiles are essentially pieces of geographic data that a mapping library uses to render a map. As a user pans and zooms, the map client dynamically requests data that it uses to display the map. Vector tiles offer a significant performance boost on the client side because it avoids the overhead of having to load large, pre-rendered map layers– the map can load exactly what it needs to display and nothing else. 

But where does the map send these requests for vector tiles? Traditionally, these requests need to be sent to a server whose sole purpose is to serve vector tiles. For developers, this means either paying a service like Mapbox Tiling Service or hosting and maintaining your own tile server. 

The PMTiles format mitigates the hosting dilemma by packaging vector tiles into a static, open archive format. A PMTiles file can be self-hosted on Amazon S3 or similar cloud storage to which a map client can direct HTTP range requests for tile data. Then, we can take advantage of the performance of vector tiles without expensive services or tedious server maintenance.

## Building an ETL

Your source data is likely in some GeoJSON variant. To create a PMTiles file, you’ll need to use a few specific libraries in your ETL pipeline:

ogr2ogr - to pre-process GeoJSON data
tippecanoe - to convert GeoJSON to MBTiles (these would normally be hosted by a server)
pmtiles - to convert MBTiles to PMTiles


## Integration with Django

Using MapLibre and PMTiles allows our map application’s server to keep a really light footprint. Ultimately, since all vector tile requests to S3 are all made client-side, we could forgo a server altogether and implement a completely serverless map.

But before you pursue a static application, seriously consider whether you’ll need a database in the future to serve other tangential purposes like user management. 

## Putting it all together

Let’s build a sample project using Django, Maplibre, and PMTiles. It’ll be a map that displays median income data by congressional district.




