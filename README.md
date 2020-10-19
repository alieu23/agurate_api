# agurate_api
Agurate data model in flask and sqlalchemy with postegresql
# clone the project: 
git clone https://github.com/alieu23/agurate_api
# install packages
pip install -r requirements.txt
# setup the flask app
set FLASK_APP=app.py (for windows)
export FLASK_APP=app.py (for mac)
# set up the database
flask db init
flask db migrate
flask db upgrade
# run the flask app
flask run
Done!
