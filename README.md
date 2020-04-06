# BINA-experiment page

Web Service for the BINA Collaboration written in Flask microframework.

## Apache configuration

Temporarily unavailable

## Starting dev. server

1. Prepare python  environment
	- Create and activate virtual env
	`virtualenv venv && source vanv/bin/activate`
	- Install required modules
	`pip3 install -r requirements.txt`
	- Set local variables
	`export FLASK_APP=run.py`
	- Customize config.py and run.py

2. Create database
	- `mkdir database`
	- `flask db init`
	- `flask db migrate`
	- `flask db upgrade`

3. Create homepage
	- `mkdir App/static/homepage`
	- link git repository

4. Run server
	`python run.py` or `flask run -h <host> -p <port>`


## App structure

![structure](App/static/img/PageStructure.png)

