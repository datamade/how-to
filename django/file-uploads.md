# File uploads in Django

## Contents

- [Background](#background)
- [Setting up `django-storages`](#setting-up-django-storages)
    - [AWS configuration](#aws-configuration)
        - [Create an S3 bucket](#create-an-s3-bucket)
        - [Create an IAM user](#create-an-iam-user)
    - [Django configuration](#django-configuration)
    - [Docker configuration](#docker-configuration)
    - [Heroku configuration](#heroku-configuration)

## Background

File uploads can be tricky to handle in Django because uploaded files are not stored under
version control, and if your application is deployed on Heroku, your application
filesystem is ephemeral.

We recommend configuring Django to store file uploads in a persistent
bucket on AWS S3 by using the [`django-storages` package](https://django-storages.readthedocs.io/en/latest/).
This guide will walk you through the process of setting up this kind of pattern for your project.

For an example of a project that uses this configuration, DataMade developers
can see [`mn-election-archive`](https://github.com/datamade/mn-election-archive).

## Setting up `django-storages`

### AWS configuration

Configuring AWS requires creating two sets of resources: An S3 bucket to store your
files in, and a programmatic IAM user that is authorized to read and write files from
your bucket.

#### Create an S3 bucket

In order to configure your app to store file uploads in S3, you need to have an S3
bucket to store files in.

Sign into the DataMade AWS tenant and follow the AWS docs for [creating an S3
bucket](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html).
Use the following guidelines:

- Give your S3 bucket the same name as the GitHub repo for your project.
- Create your bucket in the `us-east-1` region whenever possible.
- Block all public access to the bucket.

If you've never created an S3 bucket before, ask a Lead Developer to double-check
your configuration before you start storing files there.

#### Create an IAM user

In order to read and write files to your S3 bucket, your application needs AWS credentials
for an IAM user that has access to the bucket.

Follow the AWS docs for [creating an IAM
user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console).
Use the following guidelines:

- Name your user after the GitHub repo for your project plus the slug `s3-user`,
  e.g. `bga-payroll-s3-user`.
- Select `Programmatic access` and **do not** select `AWS Management Console access`.
- Give your user full read/write permissions for AWS S3, but restrict the resource
  to only the S3 bucket you created and its contents. If you've never done this before,
  ask a Lead Developer for assistance.

Once you've created the user, copy the access key ID and secret key ID that AWS displays to
you. We don't need to store these long-term, since we can always recreate them if we lose them,
but make sure to keep them on hand to use in the next few steps.

### Django Configuration

Before configuring Django, update your application's `requirements.txt` file to
add `django-storages` as a dependency. Remember to rebuild your application container
to ensure that your dependencies are up to date.

`django-storages` can be configured to store files on S3 using variables in your
`settings.py` file. While there are [a wide array of variables you can set for the
package](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings),
we recommend the following settings as a baseline:

```python
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Replace 'my-s3-bucket' with the name of the bucket you created
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', 'my-s3-bucket')

AWS_LOCATION = os.getenv('AWS_LOCATION', 'dev')  # S3 prefix for uploaded objects

AWS_DEFAULT_ACL = None

if os.getenv('AWS_ACCESS_KEY_ID'):
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']

if os.getenv('AWS_SECRET_ACCESS_KEY'):
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
```

### Docker configuration

In order for file uploads to work properly in development, you'll need to
update your environment to pass your AWS credentials to your application container.

Update your `docker-compose.yml` file to mount your local AWS config directory
into your application container so you can upload files as your own user during
development. Add the following value to the `volumes` attribute
of your `app` service:

```diff
services:
  app:
    volumes:
      # Mount the development directory as a volume into the container, so
      # Docker automatically recognizes your changes.
      - .:/app
+     # Mount the AWS credentials folder so you can save uploads to S3 in dev.
+     - $HOME/.aws:/root/.aws:ro
```

In addition, you'll need to adjust the `tests/docker-compose.yml` file to disable
remote file uploads during testing:

```diff
services:
  app:
    enviroment:
+     DJANGO_STATICFILES_STORAGE: django.contrib.staticfiles.storage.StaticFilesStorage
```

### Heroku configuration

Finally, update your Heroku configuration to set the right variables for your
application environments. In each of your staging, production, and review app
enviroments, set the following config variables:

- `AWS_LOCATION`: `django-storages` will use this value to set the prefix (basically,
  the containing folder) for uploaded objects in S3. This is useful for keeping
  development, staging, and production file uploads separate. We recommend
  setting this to the name of the environment, e.g. it should be `production`
  in prod and `staging` for staging or review apps.
- `AWS_ACCESS_KEY_ID`: Set the access key ID you saved during S3 setup above.
- `AWS_SECRET_ACCESS_KEY`: Set the secret access key you saved during S3 setup above.
