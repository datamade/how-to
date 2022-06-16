# CSS in Django

The Django cookiecutter comes with Bootstrap pre-packaged. If you ever need to override Bootstrap for unique theming, [see this PR](https://github.com/confluency/stormstore-app/pull/39) for an example on how to implement Sass for overriding Bootstrap classes.

## Custom CSS Organization
Sometimes you'll need to write custom CSS. With this in mind, the cookiecutter comes with a CSS file located `css/custom.css`. This CSS file is used in the application's `base.html`. Any CSS added to that file will be imported in every single page on the site, causing the browser to download that file per request. Ideally a browser will cache this CSS, but nonetheless adding your custom CSS to the base file is a good idea **only if you need that CSS for global styles, like for site-wide layout, typography, coloring themes, etc.**

Don't add CSS to the `custom.css` file if you're writing the CSS for a specific page that's not used throughout the site. It's better to create unique CSS files per page or section of the site, so that the CSS is loaded only on the page(s) that needs it. This improves site download speed, which might seem trivial on the surface, but it can get pretty heavy when you're importing third-party CSS from a custom CSS file.

## Using third-party CSS in JavaScript
Often, an NPM library will require you to use some of their CSS. `react-leaflet` is one example of this — the library requires you to import their CSS into your React component, or somehow have those styles available on the webpage where you're creating a map.

You can import this CSS four different ways:
1. Importing the CSS from `node_modules` into the React component. In your React code, you'd declare: `import 'leaflet/dist/leaflet.css'`. The Django cookiecutter should be setup to do this, thanks to the `browserify-css` library. **This is the preferred way.**
2. Importing the CSS from `node_modules` in a custom CSS file. At the top of your CSS file, you'd declare the import like this: `@import url('/node_modules/leaflet/dist/leaflet.css')`. This works similar to option #1, but be sure you're only referencing that CSS file on the page where you need it, and nowhere else.
3. Importing the CSS from a CDN within your HTML template. Fallback to this method if the first two options are giving you trouble. [Here's an example](https://github.com/datamade/ucb-cales/blob/main/cales/templates/cales/projects_map.html#L5). This approach adds the CSS to the HTML file where your React component renders, therefore the CSS is globally available on that webpage and within your React code.
4. Copy/pasting the CSS into a local CSS file and importing that CSS into your HTML template. [Here's an example](https://github.com/datamade/ucb-cales/blob/main/cales/templates/cales/projects_map.html#L6). This is similar to option #3. This might not always work if the third-party library uses CSS processors that aren't supported by your Django app's asset pipeline.

