"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import json

from flask import Flask, render_template, request, redirect
from helpers import fetch_lang_list, translate
from TelegramBot.Utilities.database import connect_to_database

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# The path to the JSON files containing the texts shown in the site.
texts_path = 'static/texts/'
# Import all the translated texts.
text_EN = json.load(open(texts_path + 'text.json', 'r', encoding="utf-8"))
text_PT_BR = json.load(open(texts_path + 'text_pt_br.json', 'r', encoding="utf-8"))
translator_text = json.load(open(texts_path + 'text_translator.json', 'r', encoding="utf-8"))
translator_text_PT_BR = json.load(open(texts_path + 'text_translator_pt_br.json', 'r', encoding="utf-8"))
text_orders = json.load(open(texts_path + 'text_orders.json', 'r', encoding="utf-8"))


@app.route('/')
@app.route('/pt-br')
def index():
    if request.path == '/':
        text = text_EN
    else:
        # Had to write the whole html without using a template, because jinja messes up the accented chars.
        text = text_PT_BR

    # The ds header type is a resizeable header type, whereas ds header inner is the fixed one.
    return render_template("index.html", headerType="ds-header", text=text)


@app.route('/translator', methods=['GET', 'POST'])
@app.route('/pt-br/translator', methods=['GET', 'POST'])
def renderTranslator():
    langList = fetch_lang_list()

    if request.method == 'POST':
        data = request.json
        return translate(data)

    if request.path == '/translator':
        text = translator_text
    else:
        text = translator_text_PT_BR

    return render_template("translator.html", langList=langList, headerType="ds-header-inner", text=text)


@app.route('/orders')
def orders():
    db, connection = connect_to_database()
    orders = db.execute(
        "SELECT order_id, timestamp FROM orders").fetchall()

    # Creates an empty list of users and appends to it a user for every order.
    users = []
    for order in orders:

        user = {} # The user's empty data.

        # Gets the user's data from the database.
        query = db.execute(
            "SELECT name, phone, address FROM users WHERE order_id = ?", (order["order_id"],)).fetchall()[0]

        # Add the user's data to the user's dictionary.
        for key in query.keys():
            user[key] = query[key]

        # Gets the products related to that order.
        query = db.execute(
            "SELECT name, price, units, product_id FROM products WHERE order_id = ?", (order["order_id"],)).fetchall()

        # If there are no longer any products related to that order, delete both the order and the user data.
        if len(query) == 0:
            db.execute("DELETE FROM orders WHERE order_id = ?",
                       (order["order_id"],))
            connection.commit()
            db.execute("DELETE FROM users WHERE order_id = ?",
                       (order["order_id"],))
            connection.commit()
            continue # Goes to the next order.

        products = [] # The empty list of products.
        for product in query:
            product_data = {} # A dictionary to append to the list of products.
            for key in product.keys(): # Stores the product info into the dictionary.
                product_data[key] = product[key]
            products.append(product_data)

        user["products"] = products # Adds the list of products to the user's dictionary.

        users.append(user) # Adds the user to the list of users.

    db.close()
    connection.close()                                              # Maybe put this header type in the JSON file..
    return render_template("orders.html", users=users, text=text_orders, headerType="ds-header-inner")

@app.route('/orders/done', methods=['POST'])
def order_completed():
    # Removes the order from the database when dismissed.
    db, connection = connect_to_database()
    
    db.execute("DELETE FROM products WHERE product_id = ?",
               (request.form.get('completed_order_id'),))
    connection.commit()

    db.close()
    connection.close()

    return redirect('/orders')



@app.route('/fiapPython')
def fiapPython():
    return render_template("fiapPython.html")





if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
