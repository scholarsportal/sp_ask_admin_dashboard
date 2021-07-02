
Sp Ask DashBoard
======================================================

  - Yet Another LibraryH3lp Dashboard
  - This is not intended to replace the LH3 Dashboard but to supplement is by adding other features or reports.


## Screenshots
<p float="left">
<img src="screenshots/homepage.png" width="100%"/>
</p>


## Installation
Clone this repository. This project requires **python3**. On your command line, navigate in the location of this local repository, type this:

	pip install -r requirements.txt

Another option for installation - If you have **poetry** already installed:

        poetry install 

## Configuration - Windows

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

replace lh3_service_* with your main **queues** or leave empty after the equal sign. After verify the configuration by:
        
        python manage.py check
        #or with poetry
        poetry run python manage.py check

## Usage
	python manage.py runserver
        
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
