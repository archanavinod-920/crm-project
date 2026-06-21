from flask import Flask , render_template,request,redirect,session
import sqlite3
app = Flask(__name__)
cart = []
app.secret_key = "your_secret_key"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/categories')
def categories():
    return render_template('categories.html')





@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # ADMIN LOGIN
        if username == 'admin' and password == 'admin123':
            session['user'] = 'admin'
            return redirect('/admin_dashboard')

        # CUSTOMER LOGIN
        conn = sqlite3.connect('beautycrm.db')
        cursor = conn.cursor()
        print("Username:", username)
        print("Password:", password)

        cursor.execute(
            "SELECT * FROM customer_registration WHERE name=? AND password=?",
            (username, password)
        )

        customer = cursor.fetchone()
        conn.close()
        print("Username:", username)
        print("Password:", password)
        print("Customer:", customer)

       

        if customer:
            session['id'] = customer[0]
            return redirect('/customer_home')

        else:
            return "Invalid Login"

    return render_template('login.html')

    

@app.route('/profile')
def profile():

    print(session)

    if 'id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('beautycrm.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM customer_registration WHERE id=?",
        (session['id'],)
    )

    customer = cursor.fetchone()

    conn.close()

    return render_template('cust_prof.html', customer=customer)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():

    if 'id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('beautycrm.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        gender = request.form['gender']
        skin_type = request.form['skin_type']

        cursor.execute("""
        UPDATE customer_registration
        SET name=?,
            email=?,
            phone=?,
            address=?,
            gender=?,
            skin_type=?
        WHERE id=?
        """,
        (
            name,
            email,
            phone,
            address,
            gender,
            skin_type,
            session['id']
        ))

        conn.commit()
        conn.close()

        return redirect('/profile')

    cursor.execute(
        "SELECT * FROM customer_registration WHERE id=?",
        (session['id'],)
    )

    customer = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_prof.html',
        customer=customer
    )

@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('user') != 'admin':
        return redirect('/login')
    return render_template('admin dashboard.html')

@app.route('/addproduct')
def manageproducts():
    return render_template('addproduct.html')



@app.route('/customers')
def customer():

    conn = sqlite3.connect("beautycrm.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers")

    customers = cursor.fetchall()

    conn.close()

    return render_template(
        "cust_manage.html",
        customers=customers
    )


@app.route('/add', methods=['POST'])
def add_customer():

    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    gender = request.form['gender']
    skin = request.form['skin']
    address = request.form['address']

    conn = sqlite3.connect("beautycrm.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO customers
    (name,phone,email,gender,skin_type,address)
    VALUES(?,?,?,?,?,?)
    """,
    (name,phone,email,gender,skin,address))

    conn.commit()
    conn.close()

    return redirect('/customers')


@app.route('/delete/<int:id>')
def delete_customer(id):

    conn = sqlite3.connect("beautycrm.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM customers WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/customers')

# Edit Page
@app.route('/edit/<int:id>')
def edit_customer(id):

    conn = sqlite3.connect("beautycrm.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM customers WHERE id=?",
        (id,)
    )

    customer = cursor.fetchone()

    conn.close()

    return render_template(
        "edit_cust.html",
        customer=customer
    )

# Update Customer
@app.route('/update/<int:id>', methods=['POST'])
def update_customer(id):

    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    skin = request.form['skin']
    address = request.form['address']

    conn = sqlite3.connect("beautycrm.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE customers
    SET
    name=?,
    phone=?,
    email=?,
    skin_type=?,
    address=?
    WHERE id=?
    """,
    (
        name,
        phone,
        email,
        skin,
        address,
        id
    ))

    conn.commit()
    conn.close()

    return redirect('/customers')
   
@app.route('/history/<int:id>')
def history(id):

    conn = sqlite3.connect("beautycrm.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM customers WHERE id=?",
        (id,)
    )
    customer = cursor.fetchone()

    cursor.execute("""
    SELECT product_name, quantity, amount, purchase_date
    FROM purchase_history
    WHERE customer_id = ?
    """, (id,))

    history = cursor.fetchall()
    print("History:",history)

    conn.close()

    return render_template(
        "purchase_history.html",
        customer = customer,
        history = history
    )

@app.route('/search')
def search():

    keyword = request.args.get('search', '')

    conn = sqlite3.connect("beautycrm.db")
    cursor = conn.cursor()

    if keyword == "":
        cursor.execute("SELECT * FROM customers")
    else:
        cursor.execute("""
        SELECT * FROM customers
        WHERE name LIKE ?
        OR phone LIKE ?
        """, ('%' + keyword + '%',
              '%' + keyword + '%'))

    customers = cursor.fetchall()

    conn.close()

    return render_template(
        "cust_manage.html",
        customers=customers
    )


@app.route('/sales')
def sales():
    return render_template('sales.html')


@app.route('/invoice')
def invoice():
    return render_template('invoice.html')

#customer
@app.route('/customer_home')
def customer_home():
    if 'id' not in session:
        return redirect('/login')
    return render_template('customerprdt.html')

@app.route('/logout')
def logout():

    session.clear()   # removes all session data

    return redirect('/')

@app.route("/skincare")
def skincare():
    return render_template("skincare.html")


@app.route("/makeup")
def makeup():
    return render_template("makeup.html")


@app.route("/haircare")
def haircare():
    return render_template("haircare.html")


@app.route("/fragrance")
def fragrance():
    return render_template("fragrance.html")


# ADD TO CART (COMMON FOR ALL)
@app.route("/addprod", methods=["POST"])
def add():
    item = {
        "name": request.form.get("name"),
        "price": request.form.get("price"),
        "image": request.form.get("image")
    }

    cart.append(item)
    return render_template("cart.html", cart=cart)

@app.route("/cart")
def view_cart():
    total = sum(int(i["price"]) for i in cart)
    return render_template("cart.html", cart=cart, total=total)


@app.route("/remove", methods=["POST"])
def remove():
    index = int(request.form["index"])
    if 0 <= index < len(cart):
        cart.pop(index)

    total = sum(int(i["price"]) for i in cart)
    return render_template("cart.html", cart=cart, total=total)

@app.route('/prdthome')
def prdthome():
    return render_template('prdthome.html')

@app.route('/addproduct',methods=['GET','POST'])
def addproduct():
    if request.method=='POST':
        pid=request.form['pid']
        category=request.form['category']
        pname=request.form['pname']
        price=request.form['price']
        qty=request.form['qty']
        conn=sqlite3.connect("beautycrm.db")
        cur=conn.cursor()
        cur.execute("insert into products values(?,?,?,?,?)",(pid,category,pname,price,qty))
        conn.commit()
        conn.close()
    return render_template('addproduct.html')
    
@app.route('/viewproduct')
def viewprod():
    conn=sqlite3.connect("beautycrm.db")
    cur=conn.cursor()
    cur.execute("select * from products")
    products=cur.fetchall()
    conn.close()
    return render_template('viewproduct.html',products=products)

@app.route('/updateproduct',methods=['GET','POST'])
def updateproduct():
    if request.method=='POST':
        pid=request.form['pid']
        qty=int(request.form['qty'])
        conn=sqlite3.connect("beautycrm.db")
        cur=conn.cursor()
        cur.execute("update products set qty=? where id=?",(qty,pid))
        conn.commit()
        cur.execute("select * from products")
        products=cur.fetchall()
        conn.close()
        return render_template('viewproduct.html',products=products)
    return render_template('updateproduct.html')

@app.route('/deleteproduct',methods=['GET','POST'])
def deleteproduct():
    if request.method=='POST':
        pid=request.form['pid']
        conn=sqlite3.connect("beautycrm.db")
        cur=conn.cursor()
        cur.execute("delete from products  where id=?",(pid,))
        conn.commit()
        cur.execute("select * from products")
        products=cur.fetchall()
        conn.close()
        return render_template('viewproduct.html',products=products)
    return render_template('deleteproduct.html')

@app.route('/inventory')
def inventory():
    conn=sqlite3.connect("beautycrm.db")
    cur=conn.cursor()
    cur.execute("select * from products")
    products=cur.fetchall()
    conn.close()   
    return render_template('inventory.html',products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        dob = request.form['dob']
        gender = request.form['gender']
        skin_type = request.form['skin_type']
        category = request.form['category']
        address = request.form['address']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match"

        conn = sqlite3.connect("beautycrm.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO customers
        (name, phone, email, gender, skin_type, address)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (name, phone, email, gender, skin_type, address))

        cursor.execute("""
        INSERT INTO customer_registration
        (name, phone, email, dob, gender,
         skin_type, category, address, password)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (name, phone, email, dob, gender,
         skin_type, category, address, password))

        conn.commit()
        conn.close()

        return redirect('login')

    return render_template('cust_reg.html')

if __name__=='__main__':
    app.run(debug=True)