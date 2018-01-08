# CROW downloader #

Auto login and download script to get all XLS files of every 2, 4 weekly rounds.

### Install procedure ###

```
git clone https://github.com/Amsterdam/schoonmonitor.git schoonmonitor
cd schoonmonitor/crowdownloader
```

Create a local environment and activate it:
```
virtualenv --python=$(which python3) venv
source venv/bin/activate
```

Install the packages 
```
pip install -r requirements.txt
```

Before you can login to the site, you must create and add the login credentials in a config.ini file by using the supplied example file:
```
cat config.ini
```

### How to run ###

Run the script and add the destination folder name
```
./downloaderRounds.py results
```


You can run the importer as docker locally with using only the database in a docker by using:
```
./docker-compose build database
./docker-compose up database
./docker-compose build importer
./docker-compose up importer
```
