module.exports = {
  siteMetadata: {
    title: `{{cookiecutter.app_verbose_name}}`,
    description: `{{cookiecutter.description}}`,
    author: `DataMade`,
    url: ``,
    image: `/socialcard.png`
  },
  plugins: [
    `gatsby-plugin-react-helmet`,
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `images`,
        path: `${__dirname}/src/images`,
      },
    },
    `gatsby-transformer-sharp`,
    `gatsby-plugin-sharp`,
    {
      resolve: `gatsby-plugin-manifest`,
      options: {
        name: `gatsby-starter-default`,
        short_name: `starter`,
        start_url: `/`,
        background_color: `#663399`,
        theme_color: `#663399`,
        display: `minimal-ui`,
        icon: `src/images/favicon.png`, // This path is relative to the root of the site.
      },
    },
    {
      resolve: `gatsby-plugin-google-analytics`,
      options: {
        // To enable Google analytics, just set up a property and input the tracking ID here
        trackingId: "",
      },
    },
    {
      resolve: "@sentry/gatsby",
      options: {
        dsn: process.env.SENTRY_DSN ? process.env.SENTRY_DSN : "",
      }
    },
  ],
}
