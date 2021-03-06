<details>
<summary>Contents</summary>
&bull; <a href="#cavalry-fence-builder">Cavalry Fence Builder</a><br>
  &nbsp;&nbsp;&nbsp;&nbsp;&#9702; <a href="#url">URL</a><br>
  &nbsp;&nbsp;&nbsp;&nbsp;&#9702; <a href="#video">Video</a><br>
  &nbsp;&nbsp;&nbsp;&nbsp;&#9702; <a href="#core-features">Core Features</a><br>
  &nbsp;&nbsp;&nbsp;&nbsp;&#9702; <a href="#requirements">Requirements</a><br>
  &nbsp;&nbsp;&nbsp;&nbsp;&#9702; <a href="#run">Run</a><br>
  &nbsp;&nbsp;&nbsp;&nbsp;&#9702; <a href="#run-in-debug-mode">Run in Debug Mode</a><br>
  &nbsp;&nbsp;&nbsp;&nbsp;&#9702; <a href="#run-tests">Run Tests</a><br>
  &nbsp;&nbsp;&nbsp;&nbsp;&#9702; <a href="#server-hosting">Server Hosting</a><br>
  &nbsp;&nbsp;&nbsp;&nbsp;&#9702; <a href="#help">Help</a><br>
  &nbsp;&nbsp;&nbsp;&nbsp;&#9702; <a href="#tips">Tips</a><br>
&bull; <a href="#drawio">draw.io</a><br>
  &nbsp;&nbsp;&nbsp;&nbsp;&#9702; <a href="#url-1">URL</a><br>
  &nbsp;&nbsp;&nbsp;&nbsp;&#9702; <a href="#required-for-building">Required for Building</a><br>
  &nbsp;&nbsp;&nbsp;&nbsp;&#9702; <a href="#build">Build</a><br>
  &nbsp;&nbsp;&nbsp;&nbsp;&#9702; <a href="#run-1">Run</a><br>
  &nbsp;&nbsp;&nbsp;&nbsp;&#9702; <a href="#drawio-license">draw.io License</a><br>
</details>

# Cavalry Fence Builder

Cavalry Fence Builder is a web app for fence installation companies. It allows a fence business to track projects and financial data, calculate quotes, generate material lists, and send quotes to clients and material lists to suppliers.

## URL

https://app.cavalryfence.ca/

## Video

https://youtu.be/8YIqtiUu9Xk

## Core Features

* Draw fence diagrams
* Generate quotes for customers (based on diagrams)
* Email quotes to customers
* Generate material lists for suppliers (based on diagrams)
* Email material lists to suppliers
* Manually edit quotes
* Calculate costs and profits (based on diagrams)
* View a list of projects and filter by status
* View and edit project information (such as diagrams, quotes, pictures, and notes)
* View and edit customer information
* View a summary of the current year's profits/losses
* Import/export tables (such as for accounting, customer information, and material lists)
* View and edit prices for fence materials
* Create individual accounts and associate them with companies
* The server uses certbot to maintain ssl certificate

## Requirements

### Python 3

https://www.python.org/downloads/

### MySQL

https://dev.mysql.com/downloads/mysql/

### mysql-connector

Mac OS (assuming Homebrew is installed):
```bash
xcode-select --install
brew install mysql-connector-c
pip3 install mysql-connector==2.1.4
```

### Flask SQLAlchemy

```bash
pip3 install flask-sqlalchemy
```

### bcrypt

```bash
pip3 install bcrypt
```

### Flask-Security

```bash
pip3 install flask-security
```

### WeasyPrint

Mac OS (assuming Homebrew is installed):
```bash
brew install cairo pango gdk-pixbuf libffi
brew link --force libffi    # If needed
sudo chown -R `whoami`:admin /usr/local/share/man/man5
brew link fontconfig
pip3 install WeasyPrint
```

Other:<br>
http://weasyprint.readthedocs.io/en/stable/install.html

### Pillow

```bash
pip3 install pillow
```

### Requests

```bash
pip3 install requests
```

## Run

1. Start MySQL

2. In the "fencing" folder, run:
```bash
python3 app.py
```

## Run in Debug Mode

1. Start MySQL

2. In the "fencing" folder, run:
```bash
python3 app.py -debug
```

## Run Tests

1. Start MySQL

2. In the "fencing" folder, run:  
must be in the testBranch.  
```bash
python3 testingapp.py
```

3. While that is running, in a new terminal tab/window in the "fencing" folder, run:
```bash
python3 -m unittest discover
```

## Server Hosting

The app is hosted using apache2 with the app.conf file in Documentation/Server.  
The server uses mod_wsgi-express to help interact between apache2 and Flask.  
The server uses certbot to generate and maintain ssl certificates.  
The server files are stored at /var/www/CMPUT401-FenceFriends on the server.  
The server config file is stored at /etc/apache2/sites-available  
  
The mysql db is currently called testdata. The db must be created before the app is run but the app will create the tables.  
The name can be changed in user.txt  
The server required these to be installed: 
```
sudo apt-get install apache2  
sudo mod_wsgi-express install-module  
sudo apt-get install python-certbot-apache  
```
Every time the server is updated, 
```
sudo service apache2 restart
```
must be run.

This line:
```
sudo chmod -R 757 /var/www/CMPUT401-FenceFriends/fencing/static/
```
must also be run in order to change the permission of the static folder to allow for file uploads.

## Help

In the "fencing" folder, run:
```bash
python3 app.py --help
```

## Tips

[View tips](Documentation/tips.md)

# draw.io

This repository contains a modified copy of draw.io.

## URL

https://fencythat.cavalryfence.ca/

## Required for Building

### Apache Ant

Mac OS (assuming Homebrew is installed):
```bash
brew install ant
```

## Build

In the drawio/etc/build folder, run:
```bash
ant
```

## Run

1. In the drawio/war folder, run:
```bash
python3 -m http.server 8000
```

2. While that is running, access drawio with:

http://0.0.0.0:8000/index.html?offline=1&https=0

## draw.io License

* Apache License 2.0
* https://github.com/jgraph/drawio/blob/master/LICENSE
  - Accessed December 9, 2017
* Local copy: https://github.com/gdbaker/CMPUT401-FenceFriends/blob/master/drawio/LICENSE
  - Path: drawio/LICENSE
