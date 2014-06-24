from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2


app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site""" 
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon)
 
@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""
    melons = {}
    order_total=0
    if 'cart' in session:
        for melon_id in session["cart"]:
            if melons.get(melon_id) == None:
                melons[melon_id] = {}
                melons[melon_id]['melon']=model.get_melon_by_id(melon_id)
                melons[melon_id]["qty"]=1
            else:
                melons[melon_id]['qty'] += 1
            melons[melon_id]['total']= melons[melon_id]["qty"]*melons[melon_id]['melon'].price
           
        for melon_id in melons:
            order_total=order_total+float(melons[melon_id]['total'])
        order_total="$%.2f" % order_total

        return render_template("cart.html",
                                melon_dict = melons,
                                order_total = order_total)
    else:
        return render_template("cart.html",
                                melon_dict = {},
                                order_total = 0)


@app.route("/removemelon", methods=["POST"])
def remove_melons():
    melon_id = request.form['name']
    flash("Removed selected melons")
    session['cart'].remove(int(melon_id))
    return redirect("/cart")

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.
    
    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """
    if 'cart' in session:
        session["cart"].append(id)
        flash("Successfully added to cart")
    else:
        session['cart']=[]
        session["cart"].append(id)
        flash("Successfully added to cart")
    return redirect("/cart")
    


@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""

    username = request.form['username']
    customer = model.get_customer_by_email(username)
    if customer:
        session['user'] = [customer.givenname, customer.surname]
        flash("Successfully logged in")
        return redirect("/melons")
    else:
        flash("Account not found.")
        return redirect("/login")

@app.route("/logout")
def process_logout():
    session.clear()
    flash("Successfully logged out")
    return redirect("/login")


@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    app.run(debug=True)
