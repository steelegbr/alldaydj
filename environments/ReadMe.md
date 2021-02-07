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


## Users

You will need to create a superuser for initial login:

    python manage.py createsuperuser
