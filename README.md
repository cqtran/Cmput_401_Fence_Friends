# Cavalry Fence Builder

## URL

https://app.cavalryfence.ca/

Cavalry Fence Builder is a web app for fence installation companies. It allows a fence business to track projects and financial data, calculate quotes, generate material lists, and send quotes to clients and material lists to suppliers.

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
```bash
python3 testingapp.py
```

3. While that is running, in a new terminal tab/window in the "fencing" folder, run:
```bash
python3 -m unittest discover
```

## Help

In the "fencing" folder, run:
```bash
python3 app.py --help
```

# draw.io

This repository contains a modified copy of draw.io.

## URL

https://fencythat.cavalryfence.ca/

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