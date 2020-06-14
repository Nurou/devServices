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

