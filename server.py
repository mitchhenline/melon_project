from flask import Flask, render_template, redirect, flash, request, session
import jinja2, melons, customers
from forms import LoginForm

app = Flask(__name__)
app.jinja_env.undefined = jinja2.StrictUndefined
app.secret_key = 'dev'

# ______ ROUTES _______

@app.route('/')
def homepage():
    return render_template("base.html")


@app.route('/melons')
def all_melons():
    melon_list = melons.get_melon_list()
    return render_template("all_melons.html", melon_list = melon_list)

@app.route('/melon/<melon_id>')
def melon_details(melon_id):

    melon = melons.get_melon_id(melon_id)
    return render_template("melon_details.html", melon=melon)

@app.route('/add_to_cart/<melon_id>')
def add_to_cart(melon_id):

    if 'username' not in session:
        return redirect('/login')
    
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']

    cart[melon_id] = cart.get(melon_id, 0) + 1
    session.modified = True
    flash(f"Melon {melon_id} successfully added to cart.")
    print(cart)

    return redirect("/cart")

@app.route('/cart')
def show_cart():
    order_total = 0
    cart_melons = []

    if 'username' not in session:
        return redirect('/login')

    cart = session.get("cart", {})

    for melon_id, quantity in cart.items():
        melon = melons.get_melon_id(melon_id)

        total_cost = quantity * melon.price
        order_total +=total_cost

        melon.quantity = quantity
        melon.total_cost = total_cost

        cart_melons.append(melon)

    return render_template('cart.html', cart_melons=cart_melons, order_total=order_total)

@app.route('/empty_cart')
def empty_cart():
    session['cart'] = {}

    return redirect('/cart')

@app.route("/login", methods=["GET", "POST"])
def login():
    """log user into site"""
    form = LoginForm(request.form)
    # Form is submitted with valid data
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

    #Check to see if a registered user with this username exists
        user = customers.get_by_username(username)

        if not user or user['password'] != password:
            flash("Invalid username or password")
            return redirect('/login')

    # Store username in session to keep track of logged user
        session['username'] = user['username']
        flash('Logged in.')
        return redirect("/melons")

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """log user out"""

    del session["username"]
    flash("Logged out.")
    return redirect("/login")

# error handler page
@app.errorhandler(404)
def error_404(e):
    return render_template("404.html")

# ______ ROUTES END _______

if __name__ == "__main__":
    app.env = "development"
    app.run(debug = True, port = 4910, host = 'localhost')