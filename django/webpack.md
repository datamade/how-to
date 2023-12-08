# Webpack

Webpack is a JavaScript based static module bundler. We use Webpack to compress and bundle files such as CSS, images, or text files for use by an app's client.

Webpack has excellent documentation [here](https://webpack.js.org/concepts/).

# Webpack + Django

We use [django-webpack-loader](https://github.com/django-webpack/django-webpack-loader) to help Django play nicely with Webpack.  After Webpack creates bundles, it records their locations in `webpack-stats.json`. `django-webpack-loader` simply reads that file and allows you to succinctly reference your bundles in Django templates.

For example if your `weback.config.js` entrypoints look like this:

```js
    const config = {
      context: __dirname,
      entry: {
        bundleA: "./workplace/static/js/utils/bundleA.js",
        bundleB: "./workplace/static/js/bundleB.js",
        bundleC: "./workplace/static/js/bundleC.js",
      },
...
```

you can reference `bundleA` in a template like this:

```
  {% load render_bundle from webpack_loader %}
  {% render_bundle 'bundleA' js %}
```

# Local Development vs. Production

When developing locally, we use [webpack-dev-server](https://webpack.js.org/configuration/dev-server/). This is a server that both serves our static assets from memory and automatically recreates bundles + reloads webpages when their files are changed.

In production, we don't need to run `webpack-dev-server`. We simply tell Webpack to bundle our assets when building our Docker image. `django-webpack-loader` will then find the bundles (using `webpack-stats.json`) when they're requested by the client.


# Example Projects

[Workplace DI](https://github.com/datamade/workplace-di/) is a good example of how we use webpack in a real project.

To get an idea of how Webpack is set up, look over to `webpack.config.js` in that project's root directory. There, you'll find the bundle entrypoints that are later referenced in `workplace/templates/workplace/`. For the differences in how Webpack is used locally vs. in production, head to `Dockerfile.dev` and `Dockerfile`, respectively.

Workplace DI also happens to be one of the first projects that use Webpack here at Datamade. You can check out [this pull request](https://github.com/datamade/how-to/pull/349) to see how we transitioned that project.
