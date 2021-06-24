# README

## Important Commands

* python3 -m pip install -r requirements.txt

* python3 manage.py makemigrations
* python3 manage.py migrate

* python3 manage.py runserver

* python3 manage.py createsuperuser

## Steps

1. Clone the repo.
2. Create a env/virtual
3. Install python 3
4. Install the required libraries by command-1 (this will install django aswell)
5. The **blue_mountain** is main repo containing pre-configured .settings and .urls, The **templates** contains required .html templates, **coreengine** contains the .models .urls .views .admin files, currently all logic stored in there.
6. Now to create the database and tables inside it, run the command-3. This will run all the created migrations (coreengine.migrations) to bringing the db upto speed. (all migrations are committed so command-2 not required)
7. Everything good to go. Now run command-4 to start the server.
8. localhost:8000/admin for django admin portal and rest urls can be found in code.


Enjoy Django.
