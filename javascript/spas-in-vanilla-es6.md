# Single-Page Apps in Vanilla ES6

Plain old HTML and a JavaScript file or two offer a simple developer experience
during development and deployment.

This document contains guidance on when to use this stack, and some tips for
publishing your work.

## When to use Vanilla ES6

Does your site need:

- A single page?
- A minimally complicated map?
- Lightweight data, e.g., a single JSON or CSV file or querying via external requests

Does your site need:

- More than one page?
- Data?
- Complex maps, charts, or other visualizations?

Then it's probably better suited for Gatsby. [Head over to our Gatsby docs to
learn more](gatsby/).

## Prerequisites

For a maximally productive time, you'll want to familiarize yourself with
[our JavaScript stack], namely the `yarn` package manager and build tool in
addition to ES6 itself.

## Patterns

### Development

If your app doesn't have any dependencies, or if you can ship them with your
code or source them from a CDN, simply create an `index.html` file and a
`main.js` file, and off you go.

You can serve your files in local development like:

```bash
python3 -m http.server
```

Note, though, that if you're using ES6 syntax, this approach may not work in
all browsers.

If you're targeting a broader user base, and/or if you prefer the ease of using
a CLI to manage packages, we recommend using `yarn` to install dependencies
and Browserify and Babelify to bundle third-party packages with your code and
compile them to ES5 for maximum compatibility. 

...

Simply define a `package.json` file.

```json
{
  ...
  "dependencies": {
    "browserify": "^17.0.0",
    "babelify": "...",
    ...
  },
  "scripts": {
    "develop": "yarn install && (watchify docs/js/main.js -o docs/js/bundle.js & python3 -m http.server)",
    "build": "yarn install && browserify docs/js/main.js -o docs/js/bundle.js"
  }
  ...
}
```

...

### Deployment

Static sites can be hosted seamlessly on GitHub Pages.

### Examples

- [IHS Displacement Risk Map](https://github.com/datamade/ihs-displacement-risk-in-chicago)
- @fgregg's [Public Land Survey](https://github.com/fgregg/public-land-survey)
- [National Wastewater Surveillance System Data Standard Validator](https://github.com/datamade/nwss-data-standard/demo)