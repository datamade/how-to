# Stripe
Stripe offers an api, webhooks, and a dashboard that we can use to integrate ecommerce into apps that need it.

<!-- TODO: table of contents -->

## Test Mode
Stripe has a separate [testing environment](https://docs.stripe.com/test-mode) with its own keys and [test cards](https://docs.stripe.com/testing#cards) to try things out. You can even set up separate webhooks and products that can be imported to live mode whenever you're ready. Test mode will be denoted by a banner at the top of the dashboard. If you have automatic email receipts being sent to customers, this won't be active in test mode.

## Subscription Management with a Hosted Checkout
[This subscription tutorial](https://testdriven.io/blog/django-stripe-subscriptions/) covers a lot of the essentials for setting up stripe with django, and we'll be describing some specifics we can take to tailor it to our purposes. The basic flow for subscriptions will be to redirect the user to Stripe's checkout, create a webhook that listens to a few subscription related events, and save relevant data to the database after the webhook is called.

From that tutorial, it's worth following the steps for:
- [adding stripe and finding your keys](https://testdriven.io/blog/django-stripe-subscriptions/#add-stripe)*
- [creating products on the dashboard](https://testdriven.io/blog/django-stripe-subscriptions/#create-a-product)*
- [setting up models](https://testdriven.io/blog/django-stripe-subscriptions/#database-model)
- [passing in the publishable key](https://testdriven.io/blog/django-stripe-subscriptions/#get-publishable-key) while [creating a checkout session](https://testdriven.io/blog/django-stripe-subscriptions/#create-checkout-session)**
- [setting up a webhook](https://testdriven.io/blog/django-stripe-subscriptions/#stripe-webhooks) (we'll be fleshing this out more below)

<small>* Be sure to get keys and ids into a `.env` file as we normally do.</small>
<small>** The success and cancel redirects here can be anything you'd like as long as you keep the session id. In Parserator, we just [redirected back to the account page](https://github.com/datamade/parserator.datamade.us/blob/22d71ef5e220fdc08838ea4e0bf4273e53bae978/parserator_web/views.py#L820-L821) in order to avoid making dedicated success/cancel pages.</small>

So you've got your keys, your models are ready, and you're sending users to a Stripe hosted checkout page for a subscription. That's great! Here are some extra things to consider.

### Webhooks
At this point, the webhooks on Stripe are set up to listen for the `checkout.session.complete` event. This event is great for creating a new `StripeCustomer` object. If we're operating under the assumption of a recurring subscription, we'll need some additional events that denote updates and cancellations.

#### Receiving Webhook Events
Here's a list of some useful webhook events:

- `checkout.session.complete` - after the checkout process successfully finishes
- `customer.subscription.updated` - after a customer's subscription details change in any way
- `customer.subscription.deleted` - after a customer's subscription has fully been cancelled


#### Testing Webhooks
The tutorial above mentions testing webhooks locally using the Stripe CLI. This is useful for quickly making sure events you need are handled correctly. However, once it's time to test on a review app, or if you're locally working on parts that communicate with Stripe after receiving a webhook request, it becomes more useful to use one of the test webhooks created on the dashboard.

Head to the [Stripe developer dashboard](https://dashboard.stripe.com/test/developers) and select the Webhooks tab while in test mode. Create a webhook with the events you need, and enter your app's url ending with the path to the webhook you've made. This will be different for each case.

- For review apps, that could look something like `https://<review-app-subdomain>.herokuapp.com/stripe-webhook/`
- For local dev, use a service like [Ngrok](https://ngrok.com/docs/getting-started/) to expose your local environment. It's easiest if you can set a consistent url that you don't have to change much.

Make sure the webhook signing secret is added to your environment variables and you're good to go! Remember to disable that webhook when you're done testing.

### Configuring Stripe's Checkout
<!-- TODO: settings to consider regarding subscription cancellations. maybe i meant cancelling the subscription process? idk -->


#### Prepopulating customer email during checkout
If your users provide emails, you can prepopulate that field by passing in a `customer_email` while creating the checkout session.

```
checkout_session = stripe.checkout.Session.create(
    client_reference_id=request.user.id if request.user.is_authenticated else None,
    customer=<stripe customer id>,
    customer_email=<email string>,
    success_url=<success url> + '&session_id={CHECKOUT_SESSION_ID}',
    ...
```
<small>Note: Stripe expects the literal string `{CHECKOUT_SESSION_ID}` when receiving the success url so that it can replace it with an appropriate value.</small>

### Customer Portal
Customers can use a customizable portal to manage their subscriptions. Change settings for this portal by heading to the Stripe dashboard, and clicking Settings > Billing > Customer portal. Here you can change the portal's header, choose whether or not cancelled subscriptions take effect immediately, allow customers to change subscriptions, and more.

Once the portal is configured, we'll need to set up a view to create the appropriate url in order for the customer to be redirected to their version of this portal. In this example, we're returning the url from the view, then using a script on the page to request the resulting url and redirect.

```
# views.py
portal_session = stripe.billing_portal.Session.create(
    customer=<stripe customer id>,
    return_url=request.build_absolute_uri(reverse('account-detail')),
)
return JsonResponse({'sessionUrl': portal_session['url']})

# stripe_config.js
manageBtn.addEventListener("click", () => {
    // Get Portal Session url
    fetch(<url for our portal creation view>)
        .then((result) => {
            return result.json();
        })
        .then((data) => {
            // Redirect to Stripe Portal
            window.location.href = data.sessionUrl
        });
});
```

### Multiple Subscription tiers
<!-- TODO: creating a separate button for each on our app -->


### Models
<!-- TODO: extra fields that would be useful to include, like billing dates -->
