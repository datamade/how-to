const path = require("path")
const webpack = require("webpack") // eslint-disable-line no-unused-vars
const BundleTracker = require("webpack-bundle-tracker")

const config = {
  context: __dirname,
  entry: {
    base: "./{{cookiecutter.app_name}}/static/js/base.js",
  },
  output: {
    path: path.resolve(__dirname, "assets/bundles/"),
    filename: "[name]-[hash].js",
    chunkFilename: "[name]-[hash].js",
  },
  plugins: [
    new BundleTracker({
      path: __dirname,
      filename: "webpack-stats.json"
    })
  ],
  devServer: {
    watchFiles: ["{{cookiecutter.app_name}}/static/**/*.js"],
    host: "0.0.0.0",
    port: 3000,
    compress: false,
    allowedHosts: ["localhost"],
  },
  watchOptions: {
    poll: 1000,
  },
  resolve: {
    extensions: [".js", ".jsx", ".geojson"],
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        loader: "babel-loader",
        options: {
          presets: ["@babel/preset-env", "@babel/preset-react"]
        },
      },
      {
        test: /\.geojson$/,
        type: "json",
      },
      {
        test: /\.css$/i,
        use: [
          // Creates `style` nodes from JS strings
          "style-loader",
          // Translates CSS into CommonJS
          "css-loader",
        ],
      },
      {
        test: /\.(jpg|png|mp4)$/,
        use: {
          loader: "url-loader",
        },
      },
    ],
  },
}

module.exports = (env, argv) => {
  /*
   * /app/webpack-stats.json is the roadmap for the assorted chunks of JS
   * produced by Webpack. During local development, the Webpack server
   * serves our bundles. In production, Django should look in
   * /app/static/bundles for bundles.
   */
  if (argv.mode === "development") {
    config.output.publicPath = "http://localhost:3000/static/bundles/"
  }

  if (argv.mode === "production") {
    config.output.publicPath = "/static/bundles/"
  }

  return config
}
