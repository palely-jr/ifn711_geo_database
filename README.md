# ifn711_geo_database
Project

First Install all the python and django
 Python - https://www.python.org/downloads
Install the virtualenvwrapper
 - pip3 install virtualenvwrapper-win

run this command to create a virtual env (using the virtual environment keeps your main python config clean)
mkvirtualenv my_django_environment
Install Django
pip3 install django~=3.1
py -m django --version - This command allows you to check what version

After, you'll want to on the command line change into the uni_project directory which contains
manage.py

Then install my sql workbench
https://dev.mysql.com/downloads/windows/installer/8.0.html
follow the installation
        -    Ensure you make your username and password for your localhost admin and password (as this settings file uses this for db connection)
you'll then want to create a 'users' (users is the name of the database you create) database inside of your local host.


to start your virtual environment run 'workon xxx' (xxx being your created environment)
then type
    pip install mysqlclient
    pip install reverse-geocoder
    python manage.py migrate
this command will create the tables within your locally created mysql 
then type
    python manage.py runserver
** if any issues arise on the command line, it will be a need for extra pip plugins
** they should be easily to install following command instructions

this will start the server at localhost:8000


