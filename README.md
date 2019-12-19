# BINA-experiment page

## Apache configuration

TODO!

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

3. Run server
	`python run.py` or `flask run -h <host> -p <port>`



