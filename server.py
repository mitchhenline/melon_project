from flask import Flask, render_template, redirect, request
import jinja2

app = Flask(__name__)
app.jinja_env.undefined = jinja2.StrictUndefined

# ______ ROUTES _______

@app.route('/')
def homepage():
    return render_template("base.html")


@app.route('/melons')
def melons():
    return render_template("melons.html")

@app.route('/melon/<melon_id>')
def melon_id(melon_id):
    return render_template("melon.html")

@app.route('/add_to_cart/<melon_id>')
def add_to_cart(melon_id):
    return f"{melon_id} added to cart"

@app.route('/cart')
def show_cart():
    return render_template('cart.html')


# ______ ROUTES END _______

if __name__ == "__main__":
    app.env = "development"
    app.run(debug = True, port = 4910, host = 'localhost')