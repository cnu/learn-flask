__author__ = 'naren'
from flask import Flask, render_template
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from restaurant_db import Base, MenuItem, Restaurant

app = Flask(__name__)
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    menus = get_menus(restaurant_id)
    restaurants = get_restaurant(restaurant_id)
    return render_template('menu.html', restaurant=restaurants, items=menus)


# Task 1: Create route for newMenuItem function here


@app.route('/restaurants/<int:restaurant_id>/new')
def new_menu_item(restaurant_id):
    output = ""
    output += "<html><body>"
    output += "<h1>Create New Menu</h1>"

    return output


# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit')
def edit_menu_item(restaurant_id, menu_id):
    output = ""
    output += "<html><body>"
    output += "<h1>Create New Menu</h1>"
    return "page to edit a menu item. Task 2 complete!"


# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete')
def del_menu_item(restaurant_id, menu_id):
    output = ""
    output += "<html><body>"
    output += "<h1>Create New Menu</h1>"
    return "page to delete a menu item. Task 3 complete!"


def get_menus(res_id):
    session = DBSession()
    menus = session.query(MenuItem).filter_by(restaurant_id=res_id).all()
    session.close()
    return menus


def create_menu(res_id, name, desc, course, price):
    session = DBSession()
    new_menu = MenuItem(name=name, description=desc, course=course, price=price)
    session.add(new_menu)



def get_restaurant(res_id):
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=res_id).one()
    session.close()
    return restaurant


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
