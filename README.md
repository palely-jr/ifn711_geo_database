# ifn711_geo_database
Project
First Install all the python and django
Then install my sql workbench
replace the db config in setting.py

create a new database in local sql
create database users;
now migrate from python and make migrations
    python manage.py migrate
    python manage.py runserver
    now running on localhost:8000
then run server

additional links

https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment

additional notes
run these commands if errors after migration
pip install reverse-geolocator
pip install mysqlclient

if error is occuring (email_authentication (has a habit of always sneaking back into builds))
within a text editor or on directory
go to settings.py inside of uni_project/uni_project
inside here go to installed_apps
and delete the line "email_authentication" (or something similarly named at the bottom of the list)
now you can try re run
