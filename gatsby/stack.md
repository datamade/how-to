# The DataMade Gatsby Stack

1. [Gatsby](https://www.gatsbyjs.org/) (obviously) - static site generator
2. [React](https://reactjs.org/) - JavaScript library for building user interfaces
3. [Node.js](https://nodejs.org/en/) / [npm](https://www.npmjs.com/) - runtime environment (run JavaScript outside of a browser) and bundled package manager
4. [Yarn](https://yarnpkg.com/) - package manager
5. [ESLint](https://eslint.org/) - linter
5. [Netlify](https://www.netlify.com/) - deployment platform
6. [Docker](https://www.docker.com/products/docker-desktop) / [Docker Compose](https://docs.docker.com/compose/) - container engine

## Some example setups

- Basic static app: [`static-app-template`](https://github.com/datamade/static-app-template/) (to be iterated upon)
- Static app with `recharts` charts: [`how-to-recharts`](https://github.com/datamade/how-to-recharts/)
- Static app with `react-leaflet` map: [`lisc-cnda-map`](https://github.com/datamade/lisc-cnda-map/)

## Managing packages and plugins

`package.json` and `package-lock.json`

- https://medium.com/hackernoon/do-i-really-need-package-lock-json-file-321ce29e7d2c

Yarn and npm are equivalent (?).

> when you call yarn or npm with an argument that the CLI doesn't recognize (in this case, start), it will read the scripts section of the package.json and call the commands defined there.

More on npm scripts:

- https://docs.npmjs.com/misc/scripts
- https://medium.freecodecamp.org/introduction-to-npm-scripts-1dbb2ae01633

```bash
# The application's entry point is "yarn" so we only need to pass the "add" command.
# Running "yarn add" will fail, saying the command "yarn" does not exist.
docker-compose run --rm app add ${PACKAGE}
```

This will update `package.json` and `yarn.lock`.

Then, if the package you installed is a Gatsby plugin, add the package to
`gatsby-config.js`:

```javascript
module.exports = {
  plugins: [
    '${PACKAGE}',
  ],
}
```

If the plugin comes with a stylesheet, e.g., Leaflet, you can add it like this
to automatically pull in styles via CDN.

```javascript
module.exports = {
    plugins: [{
      resolve: 'gatsby-plugin-react-leaflet',
      options: {
        linkStyles: true // Enable/disable loading stylesheets via CDN
      }
    }],
}
````
