# About SVG files
SVG files, or scalable vector graphic files, are a unique image type that work well for making maps. Maps made with SVG files allow us access to the discrete geographies within the map using JavaScript. This makes SVG maps a powerful tool when working with front-end frameworks like React.js.

### When to use (and not use) SVG maps

SVG maps are particularly handy if:
* you do not need topographical or detailed geographic information.
* you need to reflect large amounts of data, particularly in React or Gatsby.
* you need or prefer client-side rendering, as with Gatsby apps.
* you are building a choropleth or a highly interactive map.
* you can find an SVG file of the geography or geographies you need, whether through the [`svg-maps` repo](#react-svg-maps-and-svg-maps) or elsewhere.

SVG maps are not well-suited for:
* working with Jinja or Django Template Language -- this is likely possible, but the tooling we use for working with SVGs is specific to React. Working with SVG maps outside of React or Gatsby will require exploring other tools and/or building functionality from scratch.
* making slippy / tiled maps.
* detailed geographic information, examples include:
	* geocoding.
	* placing pins of specific locations on a map.
	* switching between geographic resolutions (state, county, city, census tract).
	* laying shapes over a map that do not correspond to the shapes that make up the SVG file.


## `react-svg-maps` and `svg-maps`
[`react-svg-map`](https://www.npmjs.com/package/react-svg-map) allows you to turn the shapes that make up an SVG file into React components. It has a complimentary repository of SVG maps, called [`svg-maps`](https://github.com/VictorCazanave/svg-maps). Each map is contained in its own folder and has its own installation instructions. [Here](https://github.com/VictorCazanave/svg-maps/tree/master/packages) is the full list of available maps.

If the map you want to use is not already a part of the `svg-maps` repository, [Wikimedia Commons](https://commons.wikimedia.org/w/index.php?search=filemime%3Aimage%2Fsvg%2Bxml&title=Special%3ASearch&profile=advanced&fulltext=1&advancedSearch-current=%7B%22fields%22%3A%7B%22filetype%22%3A%22image%2Fsvg%2Bxml%22%7D%7D&ns6=1) is a good place to start looking for an SVG map. Keep in mind that it is easier to remove lines than to add them in most cases, so if you’re deciding between an SVG map that is too simple and one that is too complex, opting for the complex one will usually be the better choice.

If the map you need is not in the `svg-maps` repo, you can still use it in your code. These are the steps to do so:
1. Download the `svg-maps` repository and follow the instructions to generate a JSON representation of the SVG map.
2. If you wish to contribute to the `svg-maps` repository, follow all the instructions in that README to format your map consistently with the other maps available.
3. Copy the JSON file into your project repository and add it to the `images` folder in your React or Gatsby project.
4. Use [this proof of concept](https://github.com/fatima3558/gatsby-svg-map) as a guide to render your SVG map, paying particular attention to the `src/images/svg/` directory and the `USMap` component.

You can also submit a PR for the map you generated to the `svg-maps` repository so that your map is made available to others in the future! [Here](https://github.com/VictorCazanave/svg-maps/blob/master/CONTRIBUTING.md) are the contributing instructions for the `svg-maps` repo.

### Further reading and examples

Keep in mind that since SVG files are geometric representations of the image, understanding how to read an SVG file can help you edit it so that it meets your needs. [This article](https://www.sitepoint.com/svg-101-what-is-svg/) provides a bit more context about what SVG files are, and [this article](https://www.smashingmagazine.com/2019/03/svg-circle-decomposition-paths/) explains how to manually calculate the path of a circle, which will expose you to some basic SVG concepts that will allow you to tweak your SVG file.

Once you have your JSON version of the SVG map, you can treat this like any other props and build a map component using the `react-svg-map` package. This package takes your map’s geographies and allows you to pass props into each of the geometries programmatically. For a living example of an SVG map, check out the [Sunrise Movement’s Green Jobs site](https://greenjobsdata.com/). Unfortunately, this repository is private and not owned by DataMade, so the source code is unavailable to users unaffiliated with the Sunrise Movement.

For simpler examples of the `react-svg-maps` library in action, check out some [live examples](https://victorcazanave.github.io/react-svg-map/) and the corresponding [example code](https://github.com/VictorCazanave/react-svg-map/tree/master/examples/src/components).

Happy mapping!
