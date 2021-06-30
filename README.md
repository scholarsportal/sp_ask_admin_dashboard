
Sp Ask DashBoard
======================================================

  - Yet Another LibraryH3lp Dashboard
  - This is not intended to replace the LH3 Dashboard but to supplement is by adding other features or reports.


## Screenshots
<p float="left">
<img src="screenshots/homepage.png" width="100%"/>
</p>


## Installation
Clone this repository. This project requires python3. On your command line, navigate in the location of this local repository, type this:

	pip install -r requirements.txt

## Configuration - Mac OSX and Linux

Create a file in ~/.lh3/config::

        [default]
        server = ca.libraryh3lp.com
        timezone = America/Toronto
        salt = "you should probably change this"

The `salt` is used when generating system-level utility accounts.
This is not something you do often.  If your `salt` is unique, your
passwords will be unique.

Create a file in ~/.lh3/credentials with your LH3 credentials (should be an admin user)::

        [default]
        username = <ADMIN_USER>
        password = <ADMIN_PASS>

## Configuration - Windows

In the current directory, rename **env-exemple** to **.env** (there is a dot before the filename). Add your LibraryH3lp username and password

        salt=asjdflkajs
        scheme=https
        server=ca.libraryh3lp.com
        timezone=America/Toronto
        version=v2
        username=
        password=


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
