# Question, Answer, Comment API
The Question, Answer, Comment API allows users to List, Create, Retrieve, Update and Delete the Questions,
can Answer on particular Question, can Comment on particular Answer, and also upvote/downvote on particular Answer and like/dislike on particular Comment.

# Tech Stack
This application is purely build with the Django Framework of Python.\
Requirements:
- Python 3
- python-pip
- [virtualenv](https://virtualenv.pypa.io/en/latest/)
- Django 3.2
- [Django Rest Framework 3.12](https://www.django-rest-framework.org/)
- [python-decouple](https://pypi.org/project/python-decouple/)
- sqlite3

# Installation
First, clone this respository with the following link:
```bash
https://github.com/Parth-Shah-99/Polling-Project-API.git
```
Next, navigate in the following folder:
```bash
cd Polling-Project-API
```
Create a virtualenv for the following project and activate it:
```bash
virtualenv venv
source venv/bin/activate
```
Next, install the requirements from requirements.txt file:
```bash
pip install -r requirements.txt
```

- Before running migrations, edit the settings.py file:
1. Generate new SECRET_KEY (help: you can generate it from [Djecrety](https://djecrety.ir/))<br /> ( SECRET_KEY = "<generated_key>" )
2. Set DEBUG = True

Next, run migrations:
```bash
python manage.py makemigrations polls_api
python manage.py migrate
```
Next, create a default superuser (enter username and password for admin):
```bash
python manage.py createsuperuser
```
Run the server:
```bash
python manage.py runserver
```
Finally, you are ready to use the API.

For API Documentation, navigate to [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

For Admin Panel, navigate to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and enter username and password you have used earlier.

# License [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
Please see the [LICENSE](https://github.com/Parth-Shah-99/Polling-Project-API/blob/master/LICENSE) file for details.
