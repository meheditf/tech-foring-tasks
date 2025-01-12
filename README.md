# A Project Management Tool

This is a project management tool that allows teams to collaborate on projects assigned by `TechForing Limited`.

This project is running on django version 5.0.7 and python version 3.12.3

# Introduction

This tool needs an API to manage users, projects, tasks, and comments. The API will be consumed by their front-end web application and mobile application. 

# Project Setup

To use this project to your own machine follow this steps

### Clone repository from github

First of all, clone this repository using this command

```
git clone https://github.com/mehedishovon01/tech-foring-tasks.git
```

### Create a virtualenv

Make a virtual environment to your project directory. Let's do this,

If you have already an existing python virtualenv then run this

```
virtualenv venv
```    

Or if virtualenv is not install in you machine then run this

```
python -m venv venv
```    

Activate the virtual environment and verify it

```
. venv/bin/activate
```    

### Install the dependencies

Most of the projects have dependency name like requirements.txt file which specifies the requirements of that project,
so let’s install the requirements of it from the file.

```
pip install -r requirements.txt
```

### Make an .env

Copy .env from .env.example file for put the secret credentials

```
cp .env.example .env
```    

After that, put the database credentials and mail credentials `(Do not use the direct Mail Password)`

### Create database

Django by-default uses sqlite database. Just follow the below instrucitons.

```
python manage.py migrate
```

Migration is done. Now, run the project.

### Run this project

Let's run the development server:

```
python manage.py runserver
```

That’s it! Now you’re project is already run into a development server.

Just click this link, [http://localhost:8000/admin](http://localhost:8000/admin)

# API documentations

Open the API documentations(redoc)

Click this link, [http://localhost:8000/api/v1/schema/redoc](http://localhost:8000/api/v1/schema/redoc)

# API Endpoints

Open the swagger view for the API Endpoints

Click this link, [http://localhost:8000/api/v1/schema/swagger-ui/](http://localhost:8000/api/v1/schema/swagger-ui/)

`Thanks for reading!`
