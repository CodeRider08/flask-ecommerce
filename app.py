



# from flask import Flask, render_template, redirect, request, session
# import sqlite3
# import os

# app = Flask(__name__)

# app.secret_key = "mysecretkey"

# UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'image')

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # define admin username for admin-only access
# ADMIN_USERNAME = "admin"


# # DATABASE TABLES
# def create_table():

#     conn = sqlite3.connect("database.db")

#     cur = conn.cursor()

#     # USERS TABLE
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS users (

#             id INTEGER PRIMARY KEY AUTOINCREMENT,

#             username TEXT,

#             password TEXT
#         )
#     """)

#     # PRODUCTS TABLE
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS products (

#             id INTEGER PRIMARY KEY AUTOINCREMENT,

#             name TEXT,

#             price INTEGER,

#             image TEXT,
                
#             category TEXT,
#                 rating INTEGER
#         )
#     """)

#     #order table
#     cur.execute(""" 
#                 CREATE TABLE IF NOT EXISTS orders(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username TEXT,
#                 product_name TEXT,
#                 price INTEGER
#                 status TEXT

#                 )
#                 """)
    
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS reviews (

#         id INTEGER PRIMARY KEY AUTOINCREMENT,

#         product_id INTEGER,

#         username TEXT,

#         comment TEXT
#     )
# """)

#     conn.commit()

#     conn.close()


# create_table()


# cart = []
# wishlist = []


# HOME PAGE
# @app.route('/')
# def home():

#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     cur.execute("SELECT * FROM products")

#     products = cur.fetchall()

#     conn.close()

#     return render_template(
#         'index.html',
#         products=products,
#         username=session.get('username')
#     )
# @app.route('/category/<name>')
# def category(name):

#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     cur.execute(
#         "SELECT * FROM products WHERE category=?",
#         (name,)
#     )

#     products = cur.fetchall()

#     conn.close()

#     return render_template(
#         'index.html',
#         products=products,
#         username=session.get('username')
#     )

# # ADD TO CART
# @app.route('/add/<int:id>')
# def add_cart(id):

#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     cur.execute(
#         "SELECT * FROM products WHERE id=?",
#         (id,)
#     )

#     product = cur.fetchone()

#     conn.close()

#     if product:
#         found = False
#         for item in cart:
#             if item['id'] == product['id']:
#                 item['quantity'] +=1
#                 found = True

#                 if not found:

#                     cart.append({
#                         "id": product['id'],
#                         'name': product['name'],
#                         'price': product['price'],
#                         'image': product['image'],
#                         'quantity': 1
#                     })

#     return redirect('/cart')


# # PRODUCT DETAILS
# @app.route('/product/<int:id>', methods=['GET', 'POST'])
# def product_detail(id):
    
#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     if request.method == 'POST':

#         comment = request.method.form['comment']
#         username = session.get('username')

#         cur.execute(
#             "INSERT INTO reviews (product_id, username, comment) VALUES(?,?,?)",
#             (id, username, comment)
#         )
#         conn.commit()

#     cur.execute(
#         "SELECT * FROM products WHERE id=?",
#         (id,)
#     )

#     product = cur.fetchone()

#     cur.execute(
#         "SELECT * FROM reviews WHERE product_id=?",
#              (id,)  
#                )
    
#     reviews = cur.fetchall()

#     conn.close()

#     return render_template(
#         'product.html',
#         product=product,
#         reviews=reviews,
#         username=session.get('username')
#     )

# @app.route('/wishlist/<int:id>')
# def add_wishlist(id):

#     conn = sqlite3.connect("database.db")
#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     cur.execute(
#         "SELECT * FROM products WHERE id=?",
#         (id,)
#     )

#     product = cur.fetchone()

#     conn.close()

#     if product:
#         wishlist.append(product)

#     return redirect('/')


# # SEARCH
# @app.route('/search')
# def search():

#     query = request.args.get('query')

#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     cur.execute(
#         "SELECT * FROM products WHERE name LIKE ?",
#         ('%' + query + '%',)
#     )

#     products = cur.fetchall()

#     conn.close()

#     return render_template(
#         'index.html',
#         products=products,
#         username=session.get('username')
#     )


# # REGISTER
# @app.route('/register', methods=['GET', 'POST'])
# def register():

#     if request.method == 'POST':

#         username = request.form['username']

#         password = request.form['password']

#         conn = sqlite3.connect("database.db")

#         cur = conn.cursor()

#         cur.execute(
#             "INSERT INTO users (username, password) VALUES (?, ?)",
#             (username, password)
#         )

#         conn.commit()

#         conn.close()

#         return redirect('/login')

#     return render_template('register.html')


# # LOGIN
# @app.route('/login', methods=['GET', 'POST'])
# def login():

#     if request.method == 'POST':

#         username = request.form['username']

#         password = request.form['password']

#         conn = sqlite3.connect("database.db")

#         cur = conn.cursor()

#         cur.execute(
#             "SELECT * FROM users WHERE username=? AND password=?",
#             (username, password)
#         )

#         user = cur.fetchone()

#         conn.close()

#         if user:

#             session['username'] = username

#             return redirect('/')

#         else:

#             return "Invalid Username or Password"

#     return render_template('login.html')


# # LOGOUT
# @app.route('/logout')
# def logout():

#     session.pop('username', None)

#     return redirect('/')

# @app.route('/profile')
# def profile():

#     username = session.get('username')

#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     cur.execute(
#         "SELECT COUNT(*) as total_orders FROM orders WHERE username=?",
#         (username,)
#     )

#     orders = cur.fetchone()

#     cur.execute(
#         "SELECT COUNT(*) as total_wishlist FROM wishlist WHERE username=?",
#         (username,)
#     )

#     wishlist = cur.fetchone()

#     conn.close()

#     return render_template(
#         'profile.html',
#         username=username,
#         orders=orders,
#         wishlist=wishlist
#     )

# # ADMIN PANEL
# @app.route('/admin', methods=['GET', 'POST'])
# def admin():

#     if session.get('username') != ADMIN_USERNAME:
#         return redirect('/login')
    
     
#     conn = sqlite3.connect("database.db")
#     conn.row_factory = sqlite3.Row
#     cur = conn.cursor()

#     if request.method == 'POST':

#         name = request.form['name']

#         price = request.form['price']
#         category = request.form['category']
#         rating = request.form['rating']

#         image = request.files['image']

#         filename = image.filename

#         image.save(
#             os.path.join(
#                 app.config['UPLOAD_FOLDER'],
#                 filename
#             )
#         )

#         cur.execute(
#             "INSERT INTO products (name, price, image, category, rating) VALUES (?, ?, ?)",
#             (name, price, filename, category, rating)
#         )

#         conn.commit()

#         cur.execute("SELECT * FROM products")

#         products = cur.fetchall()

#         conn.close()
        
#         return render_template(
#             'admin.html',
#             products=products,
#         )

        
#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     cur.execute("""
#         SELECT product_name,
#                COUNT(*) as total_orders,
#                SUM(price) as total_sales
#         FROM orders
#         GROUP BY product_name
#     """)

#     report = cur.fetchall()

#     conn.close()

#     return render_template(
#         'sales_report.html',
#         report=report
#     )

# @app.route('/delete-product/<int:id>')
# def  delete_product(id):
#     conn = sqlite3.connect("database.db")
#     cur = conn.cursor()
#     cur.execute(
#         "DELETE FROM products WHERE id=?" ,
#         (id,)
#     )

#     conn.commit()
#     conn.close()
#     return redirect('/admin')

# @app.route('/admin-orders')
# def admin_orders():

#         if session.get('username') != ADMIN_USERNAME:

#           return redirect('/login')

#         conn = sqlite3.connect("database.db")

#         conn.row_factory = sqlite3.Row

#         cur = conn.cursor()

#         cur.execute(
#         "SELECT * FROM orders"
#     )

#         orders = cur.fetchall()

#         conn.close()

#         return render_template(
#         'admin_orders.html',
#         orders=orders
#     )
#     #update status

# @app.route('/update-status/<int:id>/<status>')
# def update_status(id, status):

#       conn = sqlite3.connect("database.db")

# cur = conn.cursor()

# cur.execute(
#         "UPDATE orders SET status=? WHERE id=?",
#         (status, idconn.commit()

#     conn.close()

#     return redirect('/admin-orders')

#     #dashboard data
#     cur.execute("SELECT COUNT(*) FROM products")
#     total_products = cur.fetchone()[0]

#     cur.execute("SELECT COUNT(*) FROM orders")
#     total_orders = cur.fetchone()[0]

#     cur.execute("SELECT SUM(price) FROM orders")
#     total_sales = cur.fetchone()[0] or 0

#     cur.execute("SELECT * FROM products")

#     products = cur.fetchall()

#     conn.close()

#     return render_template(
#         'admin.html',
#         products=products,
#         total_products=total_products,
#         total_orders=total_orders,
#         total_sales=total_sales,
#         username=session.get('username')
#     )

# @app.route('/edit-product/<int:id>', methods=['GET', 'POST'])
# def edit_product(id):

#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     if request.method == 'POST':

#         name = request.form['name']

#         price = request.form['price']

#         category = request.form['category']

#         rating = request.form['rating']

#         cur.execute(
#             """
#             UPDATE products
#             SET name=?, price=?, category=?, rating=?
#             WHERE id=?
#             """,
#             (name, price, category, rating, id)
#         )

#         conn.commit()

#         return redirect('/admin')

#     cur.execute(
#         "SELECT * FROM products WHERE id=?",
#         (id,)
#     )

#     product = cur.fetchone()

#     conn.close()

#     return render_template(
#         'edit_product.html',
       
#         product=product
#     )

# @app.route('/place-order')
# def place_order():

#     username = session.get('username')

#     conn = sqlite3.connect("database.db")

#     cur = conn.cursor()

#     for item in cart:

#         cur.execute(
#             "INSERT INTO orders (username, product_name, price, status) VALUES (?, ?, ?)",
#             (username, item['name'], item['price'], "Pading")
#         )

#     conn.commit()

#     conn.close()

#     cart.clear()

#     return redirect('/payment')


# @app.route('/payment', methods=['GET', 'POST'])
# def payment():

#     if request.method == 'POST':

#         return "Payment Successful!"

#     return render_template(
#         'payment.html',
#         username=session.get('username')
#     )

# @app.route('/my-orders')
# def my_orders():

#     username = session.get('username')

#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     cur.execute(
#         "SELECT * FROM orders WHERE username=?",
#         (username,)
#     )

#     orders = cur.fetchall()

#     conn.close()

#     return render_template(
#         'orders.html',
#         orders=orders,
#         username=username
#     )

# @app.route('/ship/<int:id>')
# def ship_order(id):

#     conn = sqlite3.connect("database.db")
#     cur = conn.cursor()

#     cur.execute(
#         "UPDATE orders SET status='Shipped' WHERE id=?",
#         (id,)
#     )

#     conn.commit()
#     conn.close()

#     return redirect('/admin')

# @app.route('/remove/<int:index>')
# def remove_item(index):

#     if index < len(cart):

#         cart.pop(index)

#     return redirect('/cart')

# @app.route('/increase/<int:index>')
# def increase_quantity(index):

#     if index < len(cart):
#         cart[index]['quantity'] += 1

#     return redirect('/cart')


# @app.route('/decrease/<int:index>')
# def decrease_quantity(index):

#     if index < len(cart) and cart[index]['quantity'] > 1:
#         cart[index]['quantity'] -= 1

#     return redirect('/cart')

# @app.route('/my-wishlist')
# def my_wishlist():

#     return render_template(
#         'wishlist.html',
#         wishlist=wishlist,
#         username=session.get('username')
#     )

# # CART PAGE
# @app.route('/cart')
# def show_cart():

#     total = 0

#     for item in cart:
#         total += item['price'] * item['quantity']

#     return render_template(
#         'cart.html',
#         cart=cart,
#         username=session.get('username')
#     )


# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, render_template, request, redirect, session
# import sqlite3
# import os

# app = Flask(__name__)

# app.secret_key = "secretkey"

# ADMIN_USERNAME = "admin"

# cart = []


# # ---------------- DATABASE ---------------- #

# def create_table():

#     conn = sqlite3.connect("database.db")

#     cur = conn.cursor()

#     # USERS TABLE
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS users (

#             id INTEGER PRIMARY KEY AUTOINCREMENT,

#             username TEXT,

#             password TEXT
#         )
#     """)

#     # PRODUCTS TABLE
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS products (

#             id INTEGER PRIMARY KEY AUTOINCREMENT,

#             name TEXT,

#             price INTEGER,

#             image TEXT,

#             category TEXT,

#             rating INTEGER
#         )
#     """)

#     # ORDERS TABLE
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS orders (

#             id INTEGER PRIMARY KEY AUTOINCREMENT,

#             username TEXT,

#             total INTEGER,

#             status TEXT
#         )
#     """)

#     # REVIEWS TABLE
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS reviews (

#             id INTEGER PRIMARY KEY AUTOINCREMENT,

#             product_id INTEGER,

#             username TEXT,

#             comment TEXT
#         )
#     """)

#     # WISHLIST TABLE
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS wishlist (

#             id INTEGER PRIMARY KEY AUTOINCREMENT,

#             username TEXT,

#             product_id INTEGER
#         )
#     """)

#     conn.commit()

#     conn.close()


# create_table()


# # ---------------- HOME ---------------- #

# @app.route('/')
# def home():

#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     cur.execute("SELECT * FROM products")

#     products = cur.fetchall()

#     conn.close()

#     return render_template(
#         'index.html',
#         products=products,
#         username=session.get('username')
#     )


# # ---------------- SEARCH ---------------- #

# @app.route('/search')
# def search():

#     query = request.args.get('query')

#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     cur.execute(
#         "SELECT * FROM products WHERE name LIKE ?",
#         ('%' + query + '%',)
#     )

#     products = cur.fetchall()

#     conn.close()

#     return render_template(
#         'index.html',
#         products=products,
#         username=session.get('username')
#     )


# # ---------------- CATEGORY ---------------- #

# @app.route('/category/<name>')
# def category(name):

#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     cur.execute(
#         "SELECT * FROM products WHERE category=?",
#         (name,)
#     )

#     products = cur.fetchall()

#     conn.close()

#     return render_template(
#         'index.html',
#         products=products,
#         username=session.get('username')
#     )


# # ---------------- REGISTER ---------------- #

# @app.route('/register', methods=['GET', 'POST'])
# def register():

#     if request.method == 'POST':

#         username = request.form['username']

#         password = request.form['password']

#         conn = sqlite3.connect("database.db")

#         cur = conn.cursor()

#         cur.execute(
#             "INSERT INTO users (username, password) VALUES (?, ?)",
#             (username, password)
#         )

#         conn.commit()

#         conn.close()

#         return redirect('/login')

#     return render_template('register.html')


# # ---------------- LOGIN ---------------- #

# @app.route('/login', methods=['GET', 'POST'])
# def login():

#     if request.method == 'POST':

#         username = request.form['username']

#         password = request.form['password']

#         conn = sqlite3.connect("database.db")

#         conn.row_factory = sqlite3.Row

#         cur = conn.cursor()

#         cur.execute(
#             "SELECT * FROM users WHERE username=? AND password=?",
#             (username, password)
#         )

#         user = cur.fetchone()

#         conn.close()

#         if user:

#             session['username'] = username
#             return redirect('/')

#     return render_template('login.html')




# # ---------------- LOGOUT ---------------- #

# @app.route('/logout')
# def logout():

#     session.clear()

#     return redirect('/')


# # ---------------- PROFILE ---------------- #

# @app.route('/profile')
# def profile():

#     username = session.get('username')

#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     cur.execute(
#         "SELECT COUNT(*) as total_orders FROM orders WHERE username=?",
#         (username,)
#     )

#     orders = cur.fetchone()

#     cur.execute(
#         "SELECT COUNT(*) as total_wishlist FROM wishlist WHERE username=?",
#         (username,)
#     )

#     wishlist = cur.fetchone()

#     conn.close()

#     return render_template(
#         'profile.html',
#         username=username,
#         orders=orders,
#         wishlist=wishlist
#     )


# # ---------------- PRODUCT DETAIL ---------------- #

# @app.route('/product/<int:id>', methods=['GET', 'POST'])
# def product_detail(id):

#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     if request.method == 'POST':

#         comment = request.form['comment']

#         username = session.get('username')

#         cur.execute(
#             "INSERT INTO reviews (product_id, username, comment) VALUES (?, ?, ?)",
#             (id, username, comment)
#         )

#         conn.commit()

#     cur.execute(
#         "SELECT * FROM products WHERE id=?",
#         (id,)
#     )

#     product = cur.fetchone()

#     cur.execute(
#         "SELECT * FROM reviews WHERE product_id=?",
#         (id,)
#     )

#     reviews = cur.fetchall()

#     conn.close()

#     return render_template(
#         'product.html',
#         product=product,
#         reviews=reviews,
#         username=session.get('username')
#     )


# # ---------------- ADD TO CART ---------------- #

# @app.route('/add/<int:id>')
# def add_cart(id):

#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     cur.execute(
#         "SELECT * FROM products WHERE id=?",
#         (id,)
#     )

#     product = cur.fetchone()

#     conn.close()

#     if product:

#         found = False

#         for item in cart:

#             if item['id'] == product['id']:

#                 item['quantity'] += 1

#                 found = True

#                 break

#         if not found:

#             cart.append({

#                 'id': product['id'],

#                 'name': product['name'],

#                 'price': product['price'],

#                 'image': product['image'],

#                 'quantity': 1
#             })

#     return redirect('/cart')


# # ---------------- CART ---------------- #

# @app.route('/cart')
# def show_cart():

#     return render_template(
#         'cart.html',
#         cart=cart
#     )


# # ---------------- REMOVE CART ---------------- #

# @app.route('/remove/<int:index>')
# def remove(index):

#     if index < len(cart):

#         cart.pop(index)

#     return redirect('/cart')


# # ---------------- PAYMENT ---------------- #

# @app.route('/payment')
# def payment():

#     total = 0

#     for item in cart:

#         total += item['price'] * item['quantity']

#     return render_template(
#         'payment.html',
#         total=total
#     )


# # ---------------- PLACE ORDER ---------------- #

# @app.route('/place-order')
# def place_order():

#     username = session.get('username')

#     total = 0

#     for item in cart:

#         total += item['price'] * item['quantity']

#     conn = sqlite3.connect("database.db")

#     cur = conn.cursor()

#     cur.execute(
#         "INSERT INTO orders (username, total, status) VALUES (?, ?, ?)",
#         (username, total, 'Pending')
#     )

#     conn.commit()

#     conn.close()

#     cart.clear()

#     return redirect('/my-orders')


# # ---------------- MY ORDERS ---------------- #

# @app.route('/my-orders')
# def my_orders():

#     username = session.get('username')

#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     cur.execute(
#         "SELECT * FROM orders WHERE username=?",
#         (username,)
#     )

#     orders = cur.fetchall()

#     conn.close()

#     return render_template(
#         'my_orders.html',
#         orders=orders
#     )


# # ---------------- WISHLIST ---------------- #

# @app.route('/wishlist/<int:id>')
# def wishlist(id):

#     username = session.get('username')

#     conn = sqlite3.connect("database.db")

#     cur = conn.cursor()

#     cur.execute(
#         "INSERT INTO wishlist (username, product_id) VALUES (?, ?)",
#         (username, id)
#     )

#     conn.commit()

#     conn.close()

#     return redirect('/')


# @app.route('/my-wishlist')
# def my_wishlist():

#     username = session.get('username')

#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     cur.execute("""
#         SELECT products.*
#         FROM wishlist
#         JOIN products
#         ON wishlist.product_id = products.id
#         WHERE wishlist.username=?
#     """, (username,))

#     products = cur.fetchall()

#     conn.close()

#     return render_template(
#         'wishlist.html',
#         products=products
#     )


# # ---------------- ADMIN PANEL ---------------- #

# @app.route('/admin', methods=['GET', 'POST'])
# def admin():

#     if session.get('username') != ADMIN_USERNAME:

#         return redirect('/login')

#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     if request.method == 'POST':

#         name = request.form['name']

#         price = request.form['price']

#         category = request.form['category']

#         rating = request.form['rating']

#         image = request.files['image']

#         filename = image.filename

#         image.save(
#             os.path.join(
#                 'static/images',
#                 filename
#             )
#         )

#         cur.execute(
#             """
#             INSERT INTO products
#             (name, price, image, category, rating)

#             VALUES (?, ?, ?, ?, ?)
#             """,
#             (name, price, filename, category, rating)
#         )

#         conn.commit()

#     cur.execute("SELECT * FROM products")

#     products = cur.fetchall()

#     conn.close()

#     return render_template(
#         'admin.html',
#         products=products
#     )


# # ---------------- DELETE PRODUCT ---------------- #

# @app.route('/delete-product/<int:id>')
# def delete_product(id):

#     if session.get('username') != ADMIN_USERNAME:

#         return redirect('/login')

#     conn = sqlite3.connect("database.db")

#     cur = conn.cursor()

#     cur.execute(
#         "DELETE FROM products WHERE id=?",
#         (id,)
#     )

#     conn.commit()

#     conn.close()

#     return redirect('/admin')


# # ---------------- EDIT PRODUCT ---------------- #

# @app.route('/edit-product/<int:id>', methods=['GET', 'POST'])
# def edit_product(id):

#     if session.get('username') != ADMIN_USERNAME:

#         return redirect('/login')

#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     if request.method == 'POST':

#         name = request.form['name']

#         price = request.form['price']

#         category = request.form['category']

#         rating = request.form['rating']

#         cur.execute(
#             """
#             UPDATE products
#             SET name=?, price=?, category=?, rating=?
#             WHERE id=?
#             """,
#             (name, price, category, rating, id)
#         )

#         conn.commit()

#         return redirect('/admin')

#     cur.execute(
#         "SELECT * FROM products WHERE id=?",
#         (id,)
#     )

#     product = cur.fetchone()

#     conn.close()

#     return render_template(
#         'edit_product.html',
#         product=product
#     )


# # ---------------- ADMIN ORDERS ---------------- #

# @app.route('/admin-orders')
# def admin_orders():

#     if session.get('username') != ADMIN_USERNAME:

#         return redirect('/login')

#     conn = sqlite3.connect("database.db")

#     conn.row_factory = sqlite3.Row

#     cur = conn.cursor()

#     cur.execute("SELECT * FROM orders")

#     orders = cur.fetchall()

#     conn.close()

#     return render_template(
#         'admin_orders.html',
#         orders=orders
#     )


# # ---------------- UPDATE STATUS ---------------- #

# @app.route('/update-status/<int:id>/<status>')
# def update_status(id, status):

#     if session.get('username') != ADMIN_USERNAME:

#         return redirect('/login')

#     conn = sqlite3.connect("database.db")

#     cur = conn.cursor()

#     cur.execute(
#         "UPDATE orders SET status=? WHERE id=?",
#         (status, id)
#     )

#     conn.commit()

#     conn.close()

#     return redirect('/admin-orders')


# # ---------------- RUN APP ---------------- #

# if __name__ == '__main__':

#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "muskan_secret"

# IMAGE FOLDER
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# DATABASE CREATE
def init_db():

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # PRODUCTS TABLE
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price INTEGER,
            category TEXT,
            image TEXT
        )
    ''')

    # USERS TABLE
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# HOME PAGE
@app.route('/')
def home():

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("SELECT * FROM products")

    products = cur.fetchall()

    conn.close()

    return render_template(
        'index.html',
        products=products
    )

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cur.fetchone()

        conn.close()

        if user:

            session['username'] = username

            return redirect('/')

    return render_template('login.html')

# LOGOUT
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

# ADMIN PANEL
@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if 'admin' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    # ADD PRODUCT
    if request.method == 'POST':

        name = request.form['name']
        price = request.form['price']
        category = request.form['category']

        image = request.files['image']

        image_filename = image.filename

        image.save(
            os.path.join(
                app.config['UPLOAD_FOLDER'],
                image_filename
            )
        )

        cur.execute(
            '''
            INSERT INTO products
            (name, price, category, image)
            VALUES (?, ?, ?, ?)
            ''',
            (name, price, category, image_filename)
        )

        conn.commit()

    # SHOW PRODUCTS
    cur.execute("SELECT * FROM products")

    products = cur.fetchall()

    conn.close()

    return render_template(
        'admin.html',
        products=products
    )

# DELETE PRODUCT
@app.route('/delete-product/<int:id>')
def delete_product(id):

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM products WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/admin')

# PRODUCT DETAILS PAGE
@app.route('/product/<int:id>')
def product(id):

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM products WHERE id=?",
        (id,)
    )

    product = cur.fetchone()

    conn.close()

    return render_template(
        'product.html',
        product=product
    )

if __name__ == '__main__':
    app.run(debug=True)

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)