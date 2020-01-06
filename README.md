# Test exercise for Badi by Carmelo Acosta 

    The following exercise exposes the requested API in localhost:8000. It is implemented using Python3 and Django 2.

# Run from docker

From the root directory (where is located Dockerfile file) run

    docker build . -t badi_challenge

Then launch the container:

    docker run -it --rm badi_challenge

# Install dependencies

It is possible to simply install dependencies and run from outside docker. Simply run the following commands from 
the root directory (where is located requirements.txt file) to install dependencies:

    python3 -m pip install -r requirements.txt
    cd badi
    python3 manage.py makemigrations
    python3 manage.py migrate --run-syncdb
    
And then run the HTTP server, exposing the API, running the following command

    python3 manage.py runserver

# Run all tests

First, install dependencies (see prior section)
Then, from the root directory (where is located manage.py file) run

    python manage.py test

# Run a single test

From the root directory (where is located manage.py file) run

    python manage.py test badi.tests.<test_file_name>.<test_class_name>.<test_name>

Example:

    python manage.py test badi.tests.tests_sunlight_hours.SunlightHoursTestCase.test__get_apartment_dawn__ok
