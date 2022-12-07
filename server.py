from flask import Flask, render_template, redirect, flash, request, session
import jinja2, melons

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


# ______ ROUTES END _______

if __name__ == "__main__":
    app.env = "development"
    app.run(debug = True, port = 4910, host = 'localhost')