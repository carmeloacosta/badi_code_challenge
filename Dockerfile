FROM frolvlad/alpine-python3

#
# COPY ALL FILES TO THE /app CONTAINER'S DESTINATION FOLDER
#
WORKDIR /app
COPY . .
COPY badi/ badi/
COPY requirements.txt requirements.txt
USER root

#
# INSTALL DEPENDENCIES
#
RUN python3 -m pip install -r requirements.txt

#
# INITIALIZE DATABASE
#
WORKDIR /app/badi
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate --run-syncdb

#
# LAUNCH THE DEMO API
#
EXPOSE 8000
CMD python3 manage.py runserver
