wdev:
	pip install -r requirements.txt
	
kill_port:
	@echo 'Help to resolve this error:--- Error: That port is already in use.'
	sudo fuser -k 8000/tcp

admin:
	@echo 'will create a new tab on the browser and go to the django admin url'
	chromium http://127.0.0.1:8000/admin/login/?next=/admin/

open:
	@echo 'will open this Git repo URL on your default browser'
	open https://github.com/guinslym/sp_ask_admin_dashboard

git_alias:
	#git config --global alias.st status
	@echo "This will change your git alias. it's better for you to run it yourself"
	@echo "git config --global alias.st status"

dumpdata:
	python manage.py dumpdata --indent 4 > fixtures/data.json
	python manage.py dumpdata emplois --indent 4 > fixtures/db.emplois.json
	@echo 'dumping the Database for backup...we never knows '

efficient:
	@echo 'Runing pytest-watch ptw -v -c --ext=.py'
	ptw -v -c

tfrontend:
	@echo 'Runing pytest-watch ptw -v -c --ext=.py'
	py.test -v  applications/startupconfort/tests/test_frontend.py

test:
	@echo 'Runing py.test -v'
	py.test applications/

test_debug:
	@echo 'Runing py.test -x --pdb '
	pytest -x --pdb

test_failed:
	@echo 'only run the tests that failed the last time it was executed'
	@ehco 'exhaustive, informative traceback formatting'
	py.test --lf --tb=long -v

test_failed_first:
	@echo "all tests will be executed, but re-ordered based on whether they've failed in the previous run or not. Failures first, successful tests after."
	@echo "Traceback: only one line per failure"
	py.test --ff --tb=line  -v

poetry-runserver:
	@echo 'Runing poetry run python manage.py runserver '
	poetry run python manage.py runserver 

poetry-migrate:
	@echo 'Runing poetry run python manage.py migrate '
	poetry run python manage.py migrate 

docker-run:
	@echo 'Running docker to run the image'
	docker-compose up --build --force-recreate -d	

ansible-run:
	@echo 'Running ansible without password'
	ansible-playbook -i inventory -v -b -c paramiko --ask-pass ubuntu-playbook.yml
