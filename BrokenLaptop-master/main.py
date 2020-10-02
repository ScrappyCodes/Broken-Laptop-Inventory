from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
# install using,  pip3 install sqlalchemy flask-sqlalchemy 
from flask_sqlalchemy import SQLAlchemy
import os
# this is the database connection string or link 
# brokenlaptops.db is the name of database and it will be created inside 
# project directory. You can choose any other direcoty to keep it, 
# in that case the string will look different. 

#database = "sqlite:///brokenlaptops.db"

database = (
    #mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_connection_name>
    'mysql+pymysql://{name}:{password}@/{dbname}?unix_socket=/cloudsql/{connection}').format (
        name       = os.environ['DB_USER'], 
        password   = os.environ['DB_PASS'],
        dbname     = os.environ['DB_NAME'],
        connection = os.environ['DB_CONNECTION_NAME']
        )

app = Flask(__name__)

# important configuration parameter, don't miss it 
app.config["SQLALCHEMY_DATABASE_URI"] = database

# database instance. thid db will be used in this project 
db = SQLAlchemy(app)

##################################################
# use python shell to create the database (from inside the project directory) 
# >>> from app import db
# >>> db.create_all()
# >>> exit()
# if you do not do this step, the database file will not be created and you will receive an error message saying "table does not exist".
###################################################

@app.route('/')
def index():
    brokenlaptops = BrokenLaptop.query.all()
    if len(brokenlaptops) ==0:
        return "There is no broken laptop"
    else:
        return render_template("index.html",brokenlaptops=brokenlaptops, title="All Broken Laptops")
    """
    this checks all of broken laptop inventory. 
    if there isn't any laptop, it displays an 'empty laptop' message
    """

@app.route('/test')
def test():
    return 'App is running'

@app.route('/init_db')
def init_db():
    db.drop_all()
    db.create_all() 
    return 'DB initialized'

@app.route('/create', methods=['GET','POST'])
def create():
    if request.form:
        brand = request.form.get("brand")
        price = request.form.get("price")
        brokenlaptop = BrokenLaptop(brand=brand,price=price)
        db.session.add(brokenlaptop)
        db.session.commit()
        
    brokenlaptops = BrokenLaptop.query.all()
    return render_template('create.html', brokenlaptops = brokenlaptops, title="Create a broken Laptop") 
    # now adde two lines to retrive all the BrokenLaptops from the database and display 
    # as it is done in '/' index route 
    """
    recieves a brand and price to then store into the broken laptop inventory
    uses create template to do so
    """
    
@app.route('/delete/<laptop_id>') # add id
def delete(laptop_id):
    try:
        brokenlaptop = BrokenLaptop.query.get(laptop_id)
        db.session.delete(brokenlaptop)
        db.session.commit()
    # add a line of code to commit the delete operation 
        brokenlaptops = BrokenLaptop.query.all() 
        render_template('delete.html', brokenlaptops = brokenlaptops)
    # now adde two lines to retrive all the BrokenLaptops from the database and display 
    # as it is done in '/' index route 
        return redirect('/')
    except:
        return "There is no broken laptop at that index"
    
    """
    So this one try to delete as normal. it reads the index id and then remove the information.
    it redirects to '/'
    if there is an error such as deleting a non-exsistent index id
    it will return a 'no laptop' string
    """
    
@app.route('/update/<laptop_id>', methods=['GET','POST']) # add id 
def update(laptop_id):
    if request.form:
        newbrand = request.form.get("brand")
        newprice = request.form.get("price")

        brokenlaptop = BrokenLaptop.query.get(laptop_id)
        brokenlaptop.brand = newbrand
        brokenlaptop.price = newprice
        
        # in this block, a modified instance of BrokenLaptop is coming in along with id
        # add few lines of code so that the modification is saved in the database 
        # for example, Brand of a laptop should be updated from 'Dell' to 'Dell Latitude'
        # code snippet will be similar to create() method 
        db.session.commit()
        
        return redirect("/")
    
    brokenlaptop = BrokenLaptop.query.get(laptop_id)
    #brokenlaptops = BrokenLaptop.query.all()
    return render_template('update.html', brokenlaptop = brokenlaptop, title= "Update a Laptop")
    # now adde two lines to retrive all the BrokenLaptops from the database and display 
    # as it is done in '/' index route 

"""
it gets the index id and simply recreates the id line
from the new brand and price, it replaces the old brand and price
it redirects to "/"
"""
# this class creates a table in the database named broken_laptop with 
# entity fields id as integer, brand as text, and price as decimal number 
# create a module containing this class and import that class into this application and use it

class BrokenLaptop(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    brand = db.Column(db.String(40), nullable = False)
    price = db.Column(db.Float, nullable = True)
    

if __name__ == '__main__':
    app.run(debug=True)