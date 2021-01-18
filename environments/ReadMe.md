# Environments

## Dev(elopment)

docker-compose provides the magic for bringing up the virtual environment. The yml file can be launched from VS code with 
the appropriate Docker plugin installed.

However, you will need a .env file with the environment variable settings and to create an S3 bucket. For the .env file,
simply stick it in the root of the project. To create the bucket, open a console on the localstack container and run the following
command:

    awslocal s3 mb s3://alldaydj

This assumes you want to call the bucket "alldaydj".

To get the latest image, remember to pull!

    docker-compose --env ../../.env pull

## Bootstrapping

An element of configuration is requred to bootstrap an environment from scratch. In this example, we'll walk through setting up a development environment. Start by opening a console on the web-backend container and running the following:

    python manage.py bootstrap login admin@alldaydj.net <password>

This create the login.dev.alldaydj.net public tenancy used to manage user sessions. With this in place, you probably want a user tenancy or two:

    python manage.py createtenantuser t1.admin@alldaydj.net <password>
    python manage.py createtenantuser t1.user@alldaydj.net <password>
    python manage.py createtenant t1 t1.admin@alldaydj.net
    python manage.py jointenantuser t1.user@alldaydj.net t1

In our example, we create an admin and standard user, the t1 tenancy and join the standard user to the tenancy. Note that the admin user is the owner of the tenancy in this example.