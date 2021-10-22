# Netlify

This document records best practices for deploying static sites to
[Netlify](https://netlify.com), DataMade's preferred static hosting provider.

## Contents

- [Background: What is a static site?](#background-what-is-a-static-site)
- [Deploy a static site to Netlify](#deploy-a-static-site-to-netlify)
    - [Create a Netlify site and publish the first build](#set-up-a-static-site-deployment)
    - [Set up a custom domain](#set-up-a-custom-domain)
    - [Add a `netlify.toml` config file to the repo](#add-a-netlifytoml-config-file-to-the-repo)
    - [Set up Slack notifications](#set-up-slack-notifications)

## Background: What is a static site?

Although the term evades strict definition, for DataMade's purposes, "static sites"
are defined as sites that don't require any backend functionality,
meaning that all business logic and data storage can be performed in HTML, CSS, and JavaScript on
the client side. At DataMade, we prefer building static sites using Gatsby;
for help getting started with building a Gatsby app, see our [Gatsby documentation](/gatsby/).
and come back here when you're ready to deploy your app.

## Deploy a static site to Netlify

The following instructions will help you set up a static site deployment with
Netlify.

### Create a Netlify site and publish the first build

1. Log into the Netlify console at https://app.netlify.com using the DataMade
   Netlify account. (The credentials can be found in the shared DataMade LastPass under `Netlify`.)
   We currently use a shared account because we don't have access to Netlify Teams.
2. In the console, choose `New site from Git` to configure your app.
3. Select the `GitHub` provider. Netlify will ask you to authenticate with GitHub. We
   use [Business Cat](http://github.com/business-cat) for this purpose. Get credentials
   for Business Cat, authenticate with Netlify, and choose the repo you want to integrate from
   the dropdown menu.
4. For the `Branch to deploy` option, select `deploy`. If you don't have a `deploy` branch
   yet, create one off of `main` so that you can verify the Netlify deployment.
5. For the `Build command` option, input whatever command you use to generate
   a build of the site (e.g. `yarn build`).
6. For the `Publish directory` option, input the directory that houses your built
   assets. For Gatsby sites, this directory is typically called `public/`.
7. Select `Deploy site` and view your deployed site at the link Netlify provides.

If your deployment was successful, Netlify will automatically deploy your site
when changes are made to the `deploy` branch.

### Set up a custom domain

1. Navigate back to https://app.netlify.com and select your site from the list of
   DataMade sites.
2. Navigate to `Settings > Site information`.
3. Select `Change site name` and change it to match the URL for the site
   (e.g. `datamade.us`).
4. On the Settings page, navigate to `Domain management` using the sidebar.
5. Select `Add domain alias` and type in the URL for the site (e.g. `datamade.us`).
6. Netlify will display a modal providing instructions on how to update your DNS
   records to point to the Netlify deployment. Send these instructions to Derek
   or Forest so that they can follow the instructions in the domain registrar.
7. In the options menu next to the domain name on the `Domain management` console
   in Netlify (`...`), select `Set as primary domain`.
8. In a minute or two, visit your domain to verify that it's pointing to Netlify
   and has provisioned an appropriate SSL cert.

### Add a `netlify.toml` config file to the repo

Once you've deployed your site in the Netlify console, you can keep your deployment configuration
under version control by defining a `netlify.toml` config file in the root of your project repo.

For an example of a simple `netlify.toml` file, see the [DataMade website
repo](https://github.com/datamade/datamade.us/blob/main/netlify.toml). For
full reference, see the [Netlify docs](https://www.netlify.com/docs/netlify-toml-reference/).

This step isn't required for your deployment to work, but it's considered a best practice to keep
configurations under version control whenever possible.

### Set up Slack notifications

See our documentation for [setting up Slack notifications for your Netlify
builds](/logging/slack.md#push-netlify-notifications-to-slack).
