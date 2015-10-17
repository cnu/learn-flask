__author__ = 'naren'
from flask import Flask
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from restaurant_db import Base, MenuItem

app = Flask(__name__)
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


@app.route('/')
def hello_world():
    menus = get_menus()
    output = ""
    output += "<html><body>"
    for menu in menus:
        output += menu.name + "</br>" + menu.price + "</br>" + menu.description + "</br>" + "</br>"
    output += "</body></html>"
    return output


def get_menus():
    session = DBSession()
    return session.query(MenuItem).all()


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
