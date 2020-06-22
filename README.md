# ubiwhere-exercise
This repository its associated with a Python &amp; Django exercise that have the purpose of develop an API REST to manage occurencies in urban environments. 

The project was created and developed on Visual Studio Code with **black** as formatter and **flake8** as linter.

The urls and views were tested with unit tests. To see the test files, go to **occurrences/tests/** and they can be ran by the following command: 
```
python .\manage.py test
```

This API REST have the following modules with specific endpoints:
-  **authentication**
```
POST api/register/ - Regist new users
POST api/login/ - Login
```
-  **users**
```
GET api/users/ - Get all users
GET api/users/<user_id> - Get specific user
DELETE api/users-delete/<user_id> - Delete specific user
```
-  **occurrencies**
```
POST api/occurrencies/ - Create new occurrences
GET api/occurrencies/ - Get user's occurrences
PUT api/occurrencies/<occurrence_id> - Update specific occurrence
DELETE api/occurrencies/<occurrence_id> - Delete specific occurrence
GET api/occurrencies-list/ - Get all occurrences
PATCH api/occurrencies-patch/<occurrence_id> - Update occurrence's state
```

For API REST Documentation, it was used Swagger. With the project running go to:
```
<ip_address:5000>/swagger/
```
Note: To test from Swagger, on login, copy the token to the 'Authorize' button with 'JWT ' on the begginning.

**Instructions to run this project**

As two different environments (development and production) are required, it was created a docker container for each environment. So, depending on which environment do you want, it can be ran ```script_run_exercise_<env_type>.sh``` or, if you want to run the project locally (using development variables), you need to, first, activate virtual environment, run requirements.txt and then run ```python .\manage.py runserver 127.0.0.1:<port>``` (if you're running it in windows, install psycopg2 by pip). In case of run the project in containers, the script will use environment variables and do 'docker-compose up' of the file that contains db, web and nginx services. The port of Nginx its **5000** by default.

The pre-requirements are:
- Docker installed
- Postman installed

To run the script, p.e Git Bash, it can be used the following command:
```
cd <path_to_project_directory>
./script_run_exercise_prod.sh
```

Having the containers running, or the project running on development, its possible to go to Postman to test the endpoints ourselves. So, using the public link below, generated via Embed, it will rendered a Collection named 'Ubiwhere API REST' with three folders, where are all the endpoints, organized by modules.
```
https://app.getpostman.com/run-collection/54597fa59c2b1eca57a6#?env%5Bdev-ubiwhere-env%5D=W3sia2V5IjoidXJsIiwidmFsdWUiOiJodHRwOi8vMTI3LjAuMC4xOjUwMDAiLCJlbmFibGVkIjp0cnVlfSx7ImtleSI6InRva2VuIiwidmFsdWUiOiJleUowZVhBaU9pSktWMVFpTENKaGJHY2lPaUpJVXpJMU5pSjkuZXlKMWMyVnlYMmxrSWpveUxDSjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2laWGh3SWpveE5Ua3lOemcxTWpJeUxDSmxiV0ZwYkNJNkltRmtiV2x1UUdWNFlXMXdiR1V1WTI5dEluMC44cm1CTXRTUHFCN1JIdlc4cEJFUERIV3pBOXNVdGtYUl9SVzF6a1p1UEIwIiwiZW5hYmxlZCI6dHJ1ZX1d
```
There is a environment associated 'dev-ubiwhere-env' where the url and token are defined. By default, the url is **127.0.0.1:5000** but, if the docker-machine ip its different, you need to change the ip manually (the port is always 5000 on the containers). The change of ip is needed for development purposes as well. In settings.py, the Database HOST is appointed to **127.0.0.1**, so, in case of need, change on both sides.

When creating the project container, a superuser is created by default. The credentials are:

**username:** admin

**password:** ubiwherepwd

Note: Running the project locally, implies the creation of a superuser on command line ```python manage.py createsuperuser```

I hope that everyhting its ok and functional.
Have a good weekend!

With the best regards,
Luís Santos
