# ubiwhere-exercise
This repository its associated with a Python &amp; Django exercise that have the purpose of develop an API REST to manage occurencies in urban environments. 

The project was created and developed on Visual Studio Code with **black** as formatter and **flake8** as linter.

This API REST have the following modules with specific endpoints:
-  **authentication**
```
POST api/register - Regist new users
POST api/login - Login
```
-  **users**
```
GET api/users - Get all users
GET api/users/<user_id> - Get specific user
DELETE api/users-delete/<user_id> - Delete specific user
```
-  **occurrencies**
```
POST api/occurrencies - Create new occurrences
GET api/occurrencies - Get user's occurrences
PUT api/occurrencies/<occurrence_id> - Update specific occurrence
DELETE api/occurrencies/<occurrence_id> - Delete specific occurrence
GET api/occurrencies-list - Get all occurrences
PATCH api/occurrencies-patch/<occurrence_id> - Update occurrence's state
```

For API REST Documentation, it was used Swagger. With the project running go to:
```
<ip_address:port>/swagger/
```

**Instructions to run this project**

Since it was asked to create two differents environments (development and production) in docker containers, there is two script files for each environment. So, depending on which environment do you want, it can be ran ```script_run_exercise_<env_type>.sh```. The script will use environment variables, and docker-compose up of the file that contains both db and web services.

The pre-requirements are:
- ports 5432, 3000 and 5000 must be unused
- Docker installed
- Postman installed

To run the script, p.e Git Bash, it can be used the following command:
```
./<path_to_project_directory>/script_run_exercise_<env_type>.sh
```

Having both containers running, we can go to Postman to test the endpoints ourselves. So, using the public link below, generated via Embed, it will rendered a Collection named 'Ubiwhere API REST' with three folders, where are all the endpoints, organized by modules.
```
https://www.getpostman.com/collections/54597fa59c2b1eca57a6
```
There is a environment associated 'dev-ubiwhere-env' where the url and token are defined. By default, the url is **127.0.0.1** but, if the docker-machine ip its different, you need to change it manually. Yet, since the development and production ports are different, you need to change the port associated with the url environment variable (3000 or 5000).

When creating the project container, a superuser is created by default. The credentials are:

**username:** admin

**password:** ubiwherepwd

I hope that everyhting its ok and functional.
Have a good weekend!

With the best regards,
Luís Santos
