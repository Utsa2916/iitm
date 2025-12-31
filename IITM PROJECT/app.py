from flask import Flask
from application.database import db

app=None #initialise app as a variable with none

def create_app():
    app=Flask(__name__) #flask object is created
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///inventory.sqlite3' #db connection
    db.init_app(app)
    #this is the context of my application and when db will be created, the context will stay same
    app.app_context().push() #tells whatever youve written in this code, use this as a server code
    return app

app=create_app()

from application.controllers import *

if __name__=='__main__': #run this app only when invoked
    with app.app_context():
        db.create_all()
        admin=User.query.filter_by(username="admin1").first()
        if admin is None:
            admin=User(username="admin1", email="admin@example.com", password="1234", type="admin")
            db.session.add(admin)
            db.session.commit()
    app.run() 
    
    
#after running the code, in the browser, do ...5000/index for the project to run
