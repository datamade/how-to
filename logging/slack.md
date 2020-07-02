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
Sentry to forward exceptions to Slack. Navigate to the Settings dashboard for
your project, choose "Alerts" in the sidebar, and select "New alert rule".

On the "New Alert" page, choose to create an "Issue Alert", and configure
rule conditions to send a notification whenever the condition `An event is seen`
is met. Add an action to send a Slack message to the `DataMade` workspace with
the slug of your channel, and optionally include `environment` or `user` in your tags.

Hit `Save rule` and test to make sure your rule sends a Slack notification (the
[Django integration docs](https://docs.sentry.io/platforms/python/django/) provide
an example of how to perform this kind of test).

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
