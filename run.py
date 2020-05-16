# single responsibility: run app
# imports from other packages happen through the __init__.py file 
from application import app

if __name__ == '__main__':
  app.run()