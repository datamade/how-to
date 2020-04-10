# Slack

This document describes how to configure different logging services to send
notifications to Slack, DataMade's preferred business chat service.

## Contents

- [Push Sentry notifications to Slack](#push-sentry-notifications-to-slack)
- [Push Netlify notifications to Slack](#push-netlify-notifications-to-slack)
    - [Creating a new Slack webhook URL for Netlify](#creating-a-new-slack-webhook-url-for-netlify)
- [Push Heroku notifications to Slack](#push-heroku-notifications-to-slack)

## Push Sentry notifications to Slack

Once you've [added your project to Sentry](./sentry.md), optionally configure
Sentry to forward exceptions to Slack. From the Sentry dashboard, click Settings,
then Integrations. Find the Slack integration in the list, and click "Configure."

You'll be taken to a list of all DataMade projects in Sentry. Find yours, then
click "Add Alert Rule" and configure the alert you'd like to send. Usually,
we forward all messages in Sentry to the project Slack channel.

## Push Netlify notifications to Slack

Netlify can easily be configured to push deploy notifications to Slack.

Visit your site settings in the Netlify console and select
`Build & deploy > Deploy notifications`. In the notifications panel, select
`Add notification` and choose `Slack integration`. Set up two integrations, one
for the `Deploy succeeded` event and one for the `Deploy failed` event, and set
them to push notifications to the same webhook URL and channel.

For the webhook URL, you can use the URL that is stored in the DataMade shared
LastPass account under `Slack incoming webhook URL for Netlify`. This webhook URL
works because we already created a Slack app for Netlify.

### Creating a new Slack webhook URL for Netlify

If you need to create a new Slack app with a new webhook URL (e.g. if you're setting
up an integration in a Slack tenant that is external to DataMade), you can follow
the [official Slack
documentation](https://slack.com/intl/en-gb/help/articles/115005265063-Incoming-webhooks-for-Slack)
to set up the webhook for use in your Netlify integration.

If you're setting up a new Slack app for a fresh webhook URL, note that from our
experience, it doesn't actually matter whether the Slack app is authorized for the
channel you want to post to since Netlify will use its own configuration for posting
to the channel you've specified. This is what allows us to share the same webhook URL
for many different Netlify sites posting to different Slack channels.

## Push Heroku notifications to Slack

Heroku can send build notifications to Slack via the [Heroku ChatOps
application](https://devcenter.heroku.com/articles/chatops). The DataMade Slack
tenant is already configured to use ChatOps; if you're setting up notifications for
a new Slack tenant, follow Heroku's documentation to set it up.

Once ChatOps is enabled for your Slack tenant, see our [docs for logging
builds from Heroku to Slack](/heroku/deploy-a-django-app.md#set-up-slack-notifications)
for a full list of commands you can run to set up the integration for your app.
