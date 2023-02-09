# Adding External Auth

## BACKGROUND

Django comes with a built-in authentication system for users but it does not provide support for third-party (social) authentication via services like Github, Gmail, or Facebook. Fortunately, [django-allauth](https://django-allauth.readthedocs.io/en/latest/index.html) does in just a few steps.

## Setting up django-allauth

Update our application's `requirements.txt` file to add `django-allauth` as a dependency. Remember to rebuild our application container to ensure that your dependencies are up to date.

Using the [documentation](https://django-allauth.readthedocs.io/en/latest/installation.html) as a reference, we'll need to add several lines of `django-allauth` configuration to `INSTALLED_APPS` in `settings.py`. Some lines will be specific to the social account provider you use, and are specified in the docs. We can also include multiple providers. If we're using Github as an example:

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

Then at the bottom of `settings.py` we need to specify that we're using the allauth backend and add a `SITE_ID` since `allauth` uses this.

    AUTHENTICATION_BACKENDS = [
        ...
        # Needed to login by username in Django admin, regardless of `allauth`
        'django.contrib.auth.backends.ModelBackend',
    
        # `allauth` specific authentication methods, such as login by e-mail
        'allauth.account.auth_backends.AuthenticationBackend',
        ...
    ]

    SITE_ID = 1

Now that we have it installed, we need to add allauth to our `urls.py` file. If using wagtail, make sure to insert this path above wagtail's.

	urlpatterns = [
	    ...
	    path('accounts/', include('allauth.urls')), # new
	    ...
	]

Then, run migrations to update the existing database.

	docker-compose run --rm app python manage.py migrate


Now that things are setup on our end, we'll connect to the providers' side. The django-allauth docs have [provider specific sections](https://django-allauth.readthedocs.io/en/latest/providers.html) with links to help set up our app, and each provider will have their own process to follow. [Github's section](https://django-allauth.readthedocs.io/en/latest/providers.html#github) has a link to their app registration page, as well as a sample callback url to provide.

Upon registering our app, we will be provided with a client id and a client secret. At this point we can either go through the django admin and set up a new 'social application' with these credentials while also adding our site to the list of chosen sites:

![image](https://user-images.githubusercontent.com/114717958/217929079-a862a439-95af-4e84-a284-4a7592d4ac1e.png)


Or configure client settings for our `SOCIALACCOUNT_PROVIDERS` in `settings.py` and add them there:

	# Provider specific settings
	SOCIALACCOUNT_PROVIDERS = {
	    'github': {
	        # For each OAuth based provider, either add a ``SocialApp``
	        # (``socialaccount`` app) containing the required client
	        # credentials, or list them here:
	        'APP': {
	            'client_id': 'ex.123',
	            'secret': 'ex.456',
	            'key': ''
	        }
	    }
	}

From there, if we navigate to our login page (ex. localhost:8000/accounts/login) we should be seeing a page that has the capacity to sign someone in regularly, and also has links to sign in with our added providers!

![image](https://user-images.githubusercontent.com/114717958/217928845-9337e412-11c5-4e59-a1d2-a07b3f3092ed.png)


## Specifying scope

Some providers allow us to specify the scope. The settings for this are also specific to each provider.

For example in GitHub, if we want more than just read-only access to a user's public data, we can specify the scope in `settings.py` as follows.

	SOCIALACCOUNT_PROVIDERS = {
	    'github': {
	        'SCOPE': [
	            'user',
	            'repo',
	            'read:org',
	        ],
        }
	}

