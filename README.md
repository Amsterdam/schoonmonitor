# Dashboard clean of the City of Amsterdam #

WIP dashboard map with CROW scores (Objective scoring system of how dirty an area is) and Meldingen openbare ruimte (Open311) the City of Amsterdam.
This is a wip showing the possiblities of using the Openstack, Docker and the DJANGO REST Framework plus Leaflet.

### Install procedure ###
download and install <a href="https://www.docker.com">docker</a></br>

```
git clone https://github.com/Amsterdam/schoonmonitor.git schoonmonitor
cd schoonmonitor
docker-compose build database
docker-compose up database
```

Create a local environment and activate it:
```
virtualenv --python=$(which python3) venv
source venv/bin/activate
```

Install the packages 
```
pip install -r ./web/requirements.txt
```

Before you can login to the site, you must create the tables and an admin useraccount in the database:
```
./web/manage.py migrate
./web/manage.py createsuperuser
```

Load the data (data is not provided, still working on openstack connection)
```
./importer/import.py
```


You can run the website locally with using only the database in a docker by using:
```
docker-compose up database
./web/manage.py runserver
```

The site can be found on http://localhost:8000</br>
The docker postgres database can be found on localhost:5403

To start the website in a docker you can use this command:
```
docker-compose build web
docker-compose up web
```

The site can be found on http://localhost:8117</br>
