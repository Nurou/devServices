# Local Installation Guide

The application runs on a Heroku server and is accessible at https://dev-services.herokuapp.com/.

This guide is for running the application locally and it's written for unix systems. 

Familiarity with the command-line interface is assumed.

## Pre-requisite Software

Your system needs to be running:

- Python 3, including *venv* and *pip*
- PSQL

## Sourcing The Project

1. Clone the project into a directory of your choosing

```
$ git clone https://github.com/Nurou/devServices.git
```

OR

Download the project as a .ZIP-file from https://github.com/nurou/devServices.

2. Create and Activate a Virtual Environment

```
$ python3 -m venv venv
$ source venv/bin/activate
```

3. Install the Project's Dependencies

```
$ pip install -r requirements.txt
```

4. Connect a Local Database

The application expects a local database URI to be exported for the application's use as specified in the [config file](https://github.com/Nurou/devServices/blob/master/application/config.py).

5. Run the application

```
$ python3 run.py
```

6. Access the app in your browser at: http://localhost:5000/ 

The application is now ready to use. See the [user guide](https://github.com/Nurou/devServices/blob/master/documentation/user-guide.md) for further documentation on how to use the application.

---

# Deployment to Heroku

The application, and any updates to it, can be deployed to a remote Heroku server. The following short guide runs through the necessary steps for this. The deployment can be configured on Herkou's side so that updates (pushed commits) trigger automatic deploys. This removes the need for manually deploying changes through the Heroku CLI.

**NB**

For the application to work as intended:

1. The `requirements.text` file that specifies the project's dependencies needs to be updated to reflect changes made to the project's dependencies.
2. Changes to the database structure, such as the addition of a foreign-key relation, must be reflected on the remote database hosted by Heroku.

To keep the requirements specification in sync, run:

```
$ pip freeze | grep -v pkg-resources > requirements.txt
```

Once you've installed the project locally as per instructions detailed above, do the following:

## Install the Heroku Command Line Interface (CLI)

Run the following command:

Linux:

```
$ sudo snap install heroku --classic
```

MacOS:

```
$ brew install heroku/brew/heroku
```

## Login to Heroku

If you don't have an account, you can create one at their website for free without the provision of credit-card information. Once that's done, run

```
$ heroku login
```

## Navigate to the Project's Directory

Run

```
$ cd ~/<path-to-project-directory>
```

## Create the Application

Run

```
$ heroku create <app-name>
```

## Add Changes to Version Control

Run the following:

```
$ git remote add heroku
$ git add .
$ git commit -m "init heroku"
$ git push heroku master
```
The Heroku CLI should spit out a link to the newly-created application, which, assuming all went well, will be accessible for use. 

## Configure a PSQL Database on Heroku

Heroku will still need a database to be configured on their side. This can be achieved with the following commands

```
$ heroku config:set HEROKU=1
$ heroku addons:add heroku-postgresql:hobby-dev
```
This creates a working database for the application. To access it, run:
```
$ heroku pg:psql
```
