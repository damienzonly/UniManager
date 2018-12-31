rm -rf venv
rm -rf *.sqlite3
rm -rf app/migrations
pip3 install virtualenv
virtualenv venv
. venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py migrate --run-syncdb
clear
echo -e "####################################################################"
echo -e "Creating superuser for /admin interface..."
echo -e "Type a password for the admin page:"
python3 manage.py createsuperuser --username "admin" --email ""
echo
echo
echo -e "Done! Now you can signup to http://localhost:8000/accounts/signup"
echo -e "####################################################################"

python3 manage.py runserver --insecure
