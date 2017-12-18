# CMS Downloader #

Python script to download all the containers, containertypes and wells from www.bammens.nl api into seperate jsons.
The results can be found here as an example: https://github.com/Amsterdam/schoonmonitor/tree/master/cmsdownloader/data.

### Install procedure ###

```
git clone https://github.com/Amsterdam/schoonmonitor.git schoonmonitor
cd schoonmonitor/cmsdownloadcontainer
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

Before you can use the api you must create a config.ini file
```
create a config.ini file with the user and password credentials using the config.ini.example file
```

Run the downloader
```
python afvalcontainers.py
```
