
Sp Ask DashBoard
======================================================

  - Scholars Portal LibraryH3lp Dashboard
  - This is not intended to replace the LH3 Dashboard but to add other features.


## Screenshots
<p float="left">
<img src="screenshots/homepage.png" width="100%"/>
</p>


#### Table of contents
[Getting started with Markdown](#getting-started-with-markdown)
[Anchor links](#anchor-links)

## Configuration

In the current directory, rename **secrets-exemple** to **.secrets** (there is a dot before the filename). Add your LibraryH3lp **username** and **password**

        salt=asjdflkajs
        scheme=https
        server=ca.libraryh3lp.com
        timezone=America/Montreal
        version=v2
        lh3_service_web=scholars-portal
        lh3_service_language=clavardez
        lh3_service_sms=scholars-portal-txt
        username=
        password=

replace lh3_service_* with your main **queues** or leave empty after the equal sign. Then, you could verify the configuration by typing on your terminal:
        
        python manage.py check
        #or with poetry
        poetry run python manage.py check

## Installation
Clone this repository. This project requires **python3**. On your command line, navigate in the location of this local repository, type this:

	pip install -r requirements.txt

Another option for installation - If you have **poetry** already installed:

        poetry install 

## Configuration and installation using Docker

In the current directory, rename **secrets-exemple** to **.secrets** (there is a dot before the filename). Add your LibraryH3lp **username** and **password**

        salt=asjdflkajs
        scheme=https
        server=ca.libraryh3lp.com
        timezone=America/Montreal
        version=v2
        username=
        password=

Run Docker to access the web application

	docker-compose up

open your browser on http://127.0.0.1:8000/ or the ip address of your server 000.000.000.000:8000


## Anchor links
lorem   

## Usage

To run the web application type in your terminal:

	python manage.py runserver
        #or
        poetry run python manage.py runserver

        
open your browser on http://127.0.0.1:8000/

## Credit
[LibraryH3lp API](https://gitlab.com/libraryh3lp/libraryh3lp-sdk-python/) -MIT

## Contributors
 - Amy (LibraryH3lp)
 - Dan S (Laurentian U)
 - Aleksandra (Carleton)
 - Erik R (Western)
 - Bart K (Scholars-Portal)
 - Sabina P (Scholars-Portal)
