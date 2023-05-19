# Leaflet
[Leaflet](https://leafletjs.com/) is an open-source JavaScript library for highly interactive, mobile-friendly maps.

There are two ways to use Leaflet:
1. [Leaflet](https://leafletjs.com/) for plain JavaScript projects.
2. [react-leaflet](https://react-leaflet.js.org/), which is for React projects. [See our documentation](/mapping/react-leaflet.md) for some guidance on how to use it.

## Leaflet with vanilla JS
The Leaflet library is a tool to use when:
1. you need a ["slippy map"](https://wiki.openstreetmap.org/wiki/Slippy_Map)
2. your map has a lot of interactions, more than you can manage with an SVG
3. you have some GeoJSON or custom geographical features

[The Leaflet documentation](https://leafletjs.com/) is the best place to learn the basics of Leaflet. 

### Limitations
Leaflet with vanilla JavaScript can lead to an unorganized and hard-to-use codebase. If you have a map that might have a lot of extra functionality, then we'd recommend using [react-leaflet](/mapping/react-leaflet.md).

### Examples from DataMade projects
- [Searchable Map Template](https://github.com/datamade/searchable-map-template-csv)
- [Justice Divided](https://github.com/datamade/justice-divided/blob/master/js/district_map.js)
- [Cal FWD CDI site](https://github.com/datamade/california-dream-index/blob/master/cdi/static/js/detailMap.js)
- [Councilmatic](https://github.com/datamade/django-councilmatic/blob/5b074f376667766e4b6dbf093871d294bb35fc51/councilmatic_core/templates/councilmatic_core/council_members.html#L105)


### Examples from Leaflet's documentation
- [Quickstart](https://leafletjs.com/examples/quick-start/)
- [Using GeoJSON with Leaflet](https://leafletjs.com/examples/geojson/)
- [Interactive Choropleth Map](https://leafletjs.com/examples/choropleth/)

#### Further reading
- [Map templates for Leaflet](https://handsondataviz.org/leaflet.html)

### A Note on Leaflet Accessibility
[Their accessibility docs](https://leafletjs.com/examples/accessibility/) describe some features that come built into Leaflet. These are: 
- the map is keyboard navigable by default, and 
- the strong recommendation to add alt attributes to markers

Although not described in their docs at the time of writing, sifting through issues on Leaflet’s repo shows there is a feature where polygons with tooltips are meant to have screen-readers read those tooltips as the shape's alt attribute. When testing the map on the homepage of the [Chicago Recovery Plan's dashboard](https://chirecoveryplan.com/) with VoiceOver, this feature was cumbersome. Each shape was read aloud as “graphics symbol” instead of something like “Fuller Park”. Through a series of commands, you can eventually get it to read the tooltip, but doing that for each area isn't ideal.

There is a possibility that this is a VoiceOver specific issue, but we would need access to some other screen readers to be sure.