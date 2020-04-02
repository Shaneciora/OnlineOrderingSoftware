import sqlite3
import os
from flask import Flask, render_template, request


app = Flask(__name__)


def fileCheck(fn):
    try:
        open(fn, "r")
        return 1
    except IOError:
        #print ("File already exists")
        return 0

def setup(db_name):
    if(fileCheck(db_name + '.db') == 1):
        print("Database '" + db_name +".db' already exists")
        return 0
        
    conn = sqlite3.connect(db_name + '.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE orders (
            orderID int,
            productID int,
            quantity int,
            firstName text
        )
    ''')
    conn.commit()
    conn.close()
    print("Created " + db_name + ".db")

def createOrder(db_name, recordList):

    #Check if DB exists
    if(fileCheck(db_name + '.db') == 0):
        print("[Error]: Database '" + db_name +".db' doesn't exists")
        return 0
        
    
    conn = sqlite3.connect(db_name + '.db')
    c = conn.cursor()
    print("Connected to SQLite DB")
    
    sqlite_insert_query = '''INSERT INTO orders
    (orderID, productID, quantity, firstName)
    VALUES (?, ?, ?, ?);'''
    
    c.executemany(sqlite_insert_query, recordList)
    print("Added order to DB")
    conn.commit()
    conn.close()
    print("Closed conntection to SQLite DB")

def clearDB(db_name):
    #Check if DB exists
    if(fileCheck(db_name + '.db') == 0):
        print("[Error]: Database '" + db_name +".db' doesn't exists")
        return 0
    conn = sqlite3.connect(db_name + '.db')
    c = conn.cursor()
    print("Connected to SQLite DB")
    
    sqlite_delete_query = '''DELETE FROM orders'''
    c.execute(sqlite_delete_query)
    print("Cleared 'orders' table")
    conn.commit()
    c.close()
    print("Closed conntection to SQLite DB")
   
def createRecordList(name):
    a = [(1, 159, 1, name)]
    return a

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/submit_form", methods=['POST'])
def submitForm():
    name = request.form['textInput']
    createOrder("pizza", createRecordList(name))
    return "success"
    

if __name__ == "__main__":
    print("Setting up databases")
    
    db_name = "pizza"
    
    setup(db_name)
    
    recordsToInsert = [(1, 159, 1, 'Shane'),
                       (1, 192, 2, 'Shane'),
                       (2, 123, 1, 'Brooke')]
                       
    app.run(host="127.0.0.1", port=5000, debug=True)
    #createOrder(db_name, recordsToInsert)
    
    #Clear db data
    #clearDB(db_name)
