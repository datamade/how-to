# Adding External Auth

## BACKGROUND

TODO

## Setting up django-allauth

Update your application's `requirements.txt` file to add `django-allauth` as a dependency. Remember to rebuild your application container to ensure that your dependencies are up to date.

Using the [documentation](https://django-allauth.readthedocs.io/en/latest/installation.html) as a reference, we'll need to add several lines of `django-allauth` configuration to `INSTALLED_APPS` in `settings.py`. Some lines will be specific to the social account provider you use, and are specified in the docs. You can also include multiple providers. If we're using Github as an example:

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites', # new
    
        'allauth', # new
        'allauth.account', # new
        'allauth.socialaccount', # new
        'allauth.socialaccount.providers.github', # new and specific
    
        # custom apps go here...
    ]

Then at the bottom of `settings.py` we need to specify that we're using the allauth backend, add a `SITE_ID` since `allauth` uses this, and (optionally) configure client settings for all of our `SOCIALACCOUNT_PROVIDERS` 

    AUTHENTICATION_BACKENDS = [
        ...
        # Needed to login by username in Django admin, regardless of `allauth`
        'django.contrib.auth.backends.ModelBackend',
    
        # `allauth` specific authentication methods, such as login by e-mail
        'allauth.account.auth_backends.AuthenticationBackend',
        ...
    ]
    SITE_ID = 1

	# Provider specific settings
	SOCIALACCOUNT_PROVIDERS = {
	    'github': {
	        # For each OAuth based provider, either add a ``SocialApp``
	        # (``socialaccount`` app) containing the required client
	        # credentials, or list them here:
	        'APP': {
	            'client_id': '123',
	            'secret': '456',
	            'key': ''
	        }
	    }
	}
*Note: as mentioned in the code, if you omit the `APP` settings in `SOCIALACCOUNT_PROVIDERS`, you will have to configure them in the admin instead.*

Now that we have it installed, we need to add allauth to our `urls.py` file. If using wagtail, make sure to insert this path above wagtail's.

	urlpatterns = [
	    ...
	    path('accounts/', include('allauth.urls')), # new
	    ...
	]

Then, run migrations to update the existing database.

	docker-compose run --rm app python manage.py migrate

TODO: talk about setting up an app on the providers' side to get the id and secret

## Specifying scope

TODO
