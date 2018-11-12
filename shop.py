from flask import Flask, render_template, abort, request, redirect, session
from werkzeug.utils import secure_filename
import sqlite3, sys, pdms, os, ssl

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
print(UPLOAD_FOLDER)
print(__file__)
UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'static', 'uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
print(UPLOAD_FOLDER)

app = Flask(__name__, static_url_path='')
app.secret_key = 'xScorpio2232'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    uid = session.get('user_id')
    with pdms.connect_db() as conn:
        data = pdms.get_user(conn, uid)
        if uid:
            global idx, name
            idx = data[0]
            name = data[1]
        else:
            idx = '[]'
            name = '[]'
    return render_template('index.html', user=uid, id=idx, name=name, title="#LetsGoLiquid")

@app.errorhandler(500)
def internal_error(e):
    uid = session.get('user_id')
    with pdms.connect_db() as conn:
        data = pdms.get_user(conn, uid)
        if uid:
            global idx, name
            idx = data[0]
            name = data[1]
        else:
            idx = '[]'
            name = '[]'
    return render_template('500.html', user=uid, id=idx, name=name, title="#LetsGoLiquid"), 500
    
@app.errorhandler(404)
def page_not_found(e):
    uid = session.get('user_id')
    with pdms.connect_db() as conn:
        data = pdms.get_user(conn, uid)
        if uid:
            global idx, name
            idx = data[0]
            name = data[1]
        else:
            idx = '[]'
            name = '[]'
    return render_template('404.html', user=uid, id=idx, name=name, title="#LetsGoLiquid"), 404

@app.route("/shop")
def shop():
    uid = session.get('user_id')
    with pdms.connect_db() as conn:
        data = pdms.get_user(conn, uid)
        if uid:
            global idx, name
            idx = data[0]
            name = data[1]
        else:
            idx = '[]'
            name = '[]'
        pds = pdms.get_products(conn)
        return render_template("shop.html", products=pds, user=uid, id=idx, name=name, title="#LetsGoLiquid")

@app.route("/shop/add-product", methods = ['GET', 'POST'])
def add_product():
    uid = session.get('user_id')
    with pdms.connect_db() as conn:
        data = pdms.get_user(conn, uid)
        if uid:
            global idx, name
            idx = data[0]
            name = data[1]
        else:
            idx = '[]'
            name = '[]'
        name = 'name_of_product'
        price = 'price_of_product'
        qty = 'quantity_of_product'
        errors = {}
        if request.method == 'POST':
            name = request.form.get('name')
            if not name:
                errors['name'] = 'empty name'
            price = request.form.get('price')
            print(price)
            if not price or not price.isdigit():
                errors['price'] = 'invalid format'
            qty = request.form.get('qty')
            if not qty or not qty.isdigit():
                errors['qty'] = 'invalid format'
            filename = None
            if 'picture' in request.files:
                pic = request.files['picture']
                if pic and allowed_file(pic.filename):
                    filename = secure_filename(pic.filename)
                    pic.save(os.path.join(UPLOAD_FOLDER, filename))
            if len(errors) == 0:
                pdms.add_product(conn, name, price, qty)
                return redirect('/shop')
        return render_template('add-product.html', name=name, id=idx, price=price, qty=qty, user=uid, title="#LetsGoLiquid")

@app.route("/shop/product/<id>")
def pro(id):
    uid = session.get('user_id')
    with pdms.connect_db() as conn:
        data = pdms.get_user(conn, uid)
        if uid:
            global idx, name
            idx = data[0]
            name = data[1]
        else:
            idx = '[]'
            name = '[]'
        p = pdms.get_product(conn, id)
        if not p:
            abort(404)
        return render_template("product.html", product=p, user=uid, id=idx, name=name, title="#LetsGoLiquid")

@app.route('/shop/product/<id>/edit', methods = ['GET', 'POST'])
def edit_p(id):
    uid = session.get('user_id')
    with pdms.connect_db() as conn:
        data = pdms.get_user(conn, uid)
        if uid:
            global idx, name
            idx = data[0]
            name = data[1]
        else:
            idx = '[]'
            name = '[]'
        prod = pdms.get_product(conn, id)
        if not prod:
            abort(404)
        name = prod[1]
        price = prod[2]
        qty = prod[3]
        errors = {}
        if request.method == 'POST':
            name = request.form.get('name')
            if not name:
                errors['name'] = 'empty name'
            price = request.form.get('price')
            # print("PRICE", price, type(price))
            if not price or not price.isdigit():
                errors['price'] = 'invalid format'
            qty = request.form.get('qty')
            if not price or not qty.isdigit():
                errors['qty'] = 'invalid format'
            fname = None
            fpath = None
            if 'picture' in request.files:
                file = request.files['picture']
                print(file, file.filename, request.files)
                if file and file.filename:
                    fpath = os.path.join(UPLOAD_FOLDER, file.filename)
                    fname = os.path.basename(fpath)
                    print("WILL IS AN IDIOT", fname)
                    file.save(fpath)
            if len(errors) == 0:
                pdms.update_product(conn, id, name, price, qty, fname)
                return redirect('/shop/product/' + id)
        return render_template('product-edit.html', product=prod,
                                name=name, id=idx, price=price, qty=qty, errors=errors, user=uid, title="#LetsGoLiquid")

@app.route('/shop/product/<id>/delete', methods = ['POST'])
def delete_p(id):
    with pdms.connect_db() as conn:
        prod = pdms.get_product(conn, id)
        if not prod:
            abort(404)
        pdms.remove_product(conn, id)
        return redirect('/shop')


@app.route("/login", methods = ['GET', 'POST'])
def login():
    uid = session.get('user_id')
    if request.method == 'POST':
        with pdms.connect_db() as conn:
            data = pdms.get_user(conn, uid)
            if uid:
                global idx, name
                idx = data[0]
                name = data[1]
            else:
                idx = '[]'
                name = '[]'
            email = request.form['email']
            password = request.form['password']
            usr = pdms.user_login(conn, email, password)
            if usr:
                session['user_id'] = usr[0]
                return redirect('/')
    return render_template('login.html', user=uid, id=idx, name=name, title="#LetsGoLiquid")

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    uid = session.get('user_id')
    with pdms.connect_db() as conn:
        data = pdms.get_user(conn, uid)
        if uid:
            global idx, name
            idx = data[0]
            name = data[1]
        else:
            idx = '[]'
            name = '[]'
        name = 'name_of_user'
        email = 'email_of_user'
        password = 'password_of_user'
        conf_password = 'confirm_password'
        errors = {}
        if request.method == 'POST':
            name = request.form.get('name')
            if not name:
                errors['name'] = 'Empty name'
            email = request.form.get('email')
            if not email:
                errors['email'] = 'Empty Email'
            password = request.form.get('password')
            if not password:
                errors['password'] = 'Empty Password'
            if len(password) < 8:
                errors['password'] = 'Password too short (minimum = 8)'
            conf_password = request.form.get('conf_password')
            if password != conf_password:
                errors['conf_password'] = 'Passwords not matching'
            if len(errors) == 0:
                pdms.add_user(conn, name, email, password)
                return redirect('/login')
        return render_template('signup.html', name=name, id=idx, email=email, password=password, errors = errors, user=uid, title="#LetsGoLiquid")

@app.route("/user/<id>")
def usr(id):
    uid = session.get('user_id')
    with pdms.connect_db() as conn:
        data = pdms.get_user(conn, uid)
        if uid:
            global idx, name
            idx = data[0]
            name = data[1]
        else:
            idx = '[]'
            name = '[]'
        u = pdms.get_user(conn, id)
        if not u:
            abort(404)
        return render_template("user.html", user=u, name=name, id=idx, title="#LetsGoLiquid")

@app.route('/user/<id>/edit', methods = ['GET', 'POST'])
def edit_u(id):
    uid = session.get('user_id')
    with pdms.connect_db() as conn:
        data = pdms.get_user(conn, uid)
        if uid:
            global idx, name
            idx = data[0]
            name = data[1]
        else:
            idx = '[]'
            name = '[]'
        usr = pdms.get_user(conn, id)
        if not usr:
            abort(404)
        name = usr[1]
        email = usr[2]
        password = usr[3]
        errors = {}
        if request.method == 'POST':
            name = request.form.get('name')
            if not name:
                errors['name'] = 'empty name'
            email = request.form.get('email')
            if not email:
                errors['email'] = 'empty email'
            password = request.form.get('password')
            if not password:
                errors['password'] = 'empty password'
            if len(password) < 8:
                errors['password'] = 'Password too short (minimum = 8)'
            conf_password = request.form.get('conf_password')
            if password != conf_password:
                errors['conf_password'] = 'Passwords not matching'
            if len(errors) == 0:
                pdms.update_user(conn, id, name, email, password)
                return redirect('/')
        return render_template('user-edit.html', user=usr, id=idx,
                                name=name, email=email, password=password, errors=errors, title="#LetsGoLiquid")


@app.route('/user/<id>/delete', methods = ['POST'])
def delete_u(id):
    with pdms.connect_db() as conn:
        usr = pdms.get_user(conn, id)
        if not usr:
            abort(404)
        pdms.remove_user(conn, id)
        return redirect('/logout')

@app.route('/logout', methods = ['GET'])
def logout():
    session['user_id'] = None
    return redirect('/')

@app.route('/privacy')
def privacy():
    uid = session.get('user_id')
    with pdms.connect_db() as conn:
        data = pdms.get_user(conn, uid)
        if uid:
            global idx, name
            idx = data[0]
            name = data[1]
        else:
            idx = '[]'
            name = '[]'
    return render_template('privacy.html', user=uid, id=idx, name=name, title="#LetsGoLiquid")

@app.route('/terms')
def terms():
    uid = session.get('user_id')
    with pdms.connect_db() as conn:
        data = pdms.get_user(conn, uid)
        if uid:
            global idx, name
            idx = data[0]
            name = data[1]
        else:
            idx = '[]'
            name = '[]'
    return render_template('terms.html', user=uid, id=idx, name=name, title="#LetsGoLiquid")
    
@app.route('/releasenotes')
def rnotes():
    uid = session.get('user_id')
    with pdms.connect_db() as conn:
        data = pdms.get_user(conn, uid)
        if uid:
            global idx, name
            idx = data[0]
            name = data[1]
        else:
            idx = '[]'
            name = '[]'
    return render_template('releasenotes.html', user=uid, id=idx, name=name, title="#LetsGoLiquid")
    
if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')