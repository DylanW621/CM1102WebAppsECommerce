from flask import Flask, render_template, request, redirect, url_for , session, flash
from flask_login import login_user, login_required, logout_user
from Run import app, db
from myshop import logM
from myshop.forms import UserReg,UserLogin,CheckoutForm #CreateReview
from myshop.classes import User, Products, Adverts, BasketContent, Reviews
import random
import copy


#PRODUCT CAT CODES
# OVUS - OVERSUIT/UNDERSUIT
# PRO - PROTECTION
# ACC - ACCESSORIES
# SRT - SRT EQUIPMENT


# <----------------------------- PRODUCT PAGES ----------------------------->
def sortProducts(itemCatToQuery, sort):
    #ascending order (price)
    if sort == "asc":
            return Products.query.order_by(Products.itemPrice.asc()).filter_by(itemCat=itemCatToQuery).all()
    
    #descending order (price)
    elif sort == "dsc":
        return Products.query.order_by(Products.itemPrice.desc()).filter_by(itemCat=itemCatToQuery).all()
    
    #environmental impact (asc)
    elif sort == "env":
        return Products.query.order_by(Products.itemCO2.asc()).filter_by(itemCat=itemCatToQuery).all()
    
    #name (asc)
    elif sort == "name":
        return Products.query.order_by(Products.itemName.asc()).filter_by(itemCat=itemCatToQuery).all()
    
    #no sort (none selected)
    else:
        return Products.query.filter_by(itemCat=itemCatToQuery).all()

#suit page
@app.route("/suit",methods=['GET', 'POST'])
def suitProd():
    if request.method == 'POST':
        productsList = sortProducts("OVUS", request.form.get('sortCat'))
    else:  
        productsList = Products.query.filter_by(itemCat="OVUS").all()
    
    return render_template('suit.html', pageHeader = "Oversuits and Undersuits",productsList=productsList, cat = request.form.get('sortCat'))

#srt page
@app.route("/SRT",methods=['GET', 'POST'])
def srtProd():
    if request.method == 'POST':
        productsList = sortProducts("SRT", request.form['sortCat'])
    else:  
        productsList = Products.query.filter_by(itemCat="SRT").all()

    return render_template('SRT.html', pageHeader = "SRT Equipment",productsList=productsList, cat = request.form.get('sortCat'))

#protection page
@app.route("/pro",methods=['GET', 'POST'])
def protecProd():
    if request.method == 'POST':
        productsList = sortProducts("PRO", request.form['sortCat'])
    else:  
        productsList = Products.query.filter_by(itemCat="PRO").all()

    return render_template('protection.html', pageHeader = "Protection",productsList=productsList, cat = request.form.get('sortCat'))


#accessories page
@app.route("/acc",methods=['GET', 'POST'])
def accProd():
    if request.method == 'POST':
        productsList = sortProducts("ACC", request.form['sortCat'])
    else:  
        productsList = Products.query.filter_by(itemCat="ACC").all()

    return render_template('acc.html', pageHeader = "Accessories",productsList=productsList, cat = request.form.get('sortCat'))

#When image clicked, goes to single product page
@app.route("/productID/<int:itemID>",methods=['GET', 'POST'])
def oneProduct(itemID):
    selectedPro = Products.query.get_or_404(itemID)
    reviews = Reviews.query.filter_by(itemID = itemID).all()

    # user submit review
    if request.method == 'POST':
        addedbyID = User.query.filter_by(email=session['loggedin']).first()
        Reviews.addReview(addedbyID.name, itemID, request.form['rating'], request.form['reviewWriting'])
        return redirect(url_for('oneProduct', itemID=itemID))

    return render_template('single.html',reviews=reviews,selectedPro=selectedPro, productINFO = selectedPro, pageHeader=selectedPro.itemName)



# <-------------------------------- HOME ------------------------------->
@app.route("/")
def home():
    newproductsFrontPage = Products.query.filter_by(newProductBool=True).all()
    # uses random import to randomly select an advert id
    randAd = Adverts.query.filter_by(AdvertID = random.randint(1,4)).all()
    return render_template('homepage.html', pageHeader = "New Products", newproductsFrontPage = newproductsFrontPage, randAd=randAd)


# <----------------------------- LOGIN/REG ----------------------------->
@app.route("/Registration", methods=['GET', 'POST'])
def register():
    form = UserReg()
    if form.validate_on_submit():
        
        # Passes the entered name, email and password into the static method 
        # in the 'Users' db
        User.registerUser(form.name.data, form.email.data, form.password.data)
        newUser = User.query.filter_by(email=form.email.data).first()
        login_user(newUser)

        # If email session null, (which is it before loggin in) then add one 
        if not 'loggedin' in session:
            session['loggedin'] = form.email.data

        return redirect(url_for('home'))
    
    return render_template('userRegPage.html', form=form, pagetitle="User Registration", pageHeader = "Create a Caving Emporium account")


@app.route("/login", methods=['GET', 'POST'])
def login():
    Ulogin = UserLogin()
    if Ulogin.validate_on_submit():
        # query's email address and checks pw hash
        UserVal = User.query.filter_by(email=Ulogin.email.data).first()
        if UserVal is None or not (UserVal.check_pass_hash(Ulogin.password.data)):
            flash('Email and/or password is incorrect!', 'danger')
            return redirect(url_for('login', **request.args))
        
        # If email session null, (which is it before loggin in) then add one 
        login_user(UserVal)
        if not 'loggedin' in session:
            session['loggedin'] = UserVal.email

        print(f"User {session['loggedin']} has logged in")
        return redirect(url_for('home'))

    return render_template('login.html', Ulogin=Ulogin, pageHeader="Login")


@app.route('/logout')
@login_required
def logout():
    #email session cleared
    session.clear()
    logout_user()
    flash("You have been successfully logged out!", 'success')
    return redirect(url_for('home'))


@logM.user_loader
def load_user(id):
    return User.query.get(int(id))


# <----------------------------- BASKET ----------------------------->

#function to calculate total price in basket
def getTotBasketPrice(itemsinBask):
    basketTotal = 0
    for prices in itemsinBask:
        basketTotal += prices.totPrice
    
    return basketTotal

#basket page
@app.route('/basket')
@login_required
def basket():
    itemsinBask = BasketContent.query.filter_by(addedbyEmail=session['loggedin']).all()
    return render_template('basket.html', pageHeader = "My basket", itemsinBask=itemsinBask, basketTotal=getTotBasketPrice(itemsinBask))
    
# add to basket
@app.route("/addbask/<int:itemID>")
def addToBasket(itemID):
    # user must be logged in to access 'add to basket'
    if not 'loggedin' in session:
        flash("You must be logged in before adding items to the basket!", 'danger')
        return redirect(request.referrer)

    # uses query to get product info so it can be added to basket table
    itemToAdd = Products.query.filter_by(itemID=itemID).first()
    BasketContent.addtobask(prodID=itemToAdd.itemID, prodName=itemToAdd.itemName,prodImg=itemToAdd.itemPic, addedbyEmail=session['loggedin'])
    flash('The item was added to the basket!', 'success')
    return redirect(request.referrer)

# route to add or remove items to/from basket
@app.route('/addremBasket/<int:prodID>/<choice>')
def addRemInBask(prodID, choice):
    if choice == "add":
        BasketContent.addtoBasketINBASK(prodID=prodID, addedbyEmail=session['loggedin'])
    else:
        BasketContent.remfromBask(prodID=prodID, addedbyEmail=session['loggedin'])

    return redirect(request.referrer)



# <----------------------------- Checkout ----------------------------->
@app.route("/checkout",methods=['GET', 'POST'])
def checkout():
    itemsinBask = BasketContent.query.filter_by(addedbyEmail=session['loggedin']).all()
    form = CheckoutForm()
    # on submit go to order completed page
    if form.validate_on_submit():
        return redirect(url_for('orderComp'))
    
    return render_template('checkout.html', pageHeader= "Checkout",checkoutPrice = getTotBasketPrice(itemsinBask), form=form)


@app.route('/ordercomplete')
def orderComp():
    userq = User.query.filter_by(email=session['loggedin']).first()
    basketCont = BasketContent.query.filter_by(addedbyEmail=session['loggedin']).all()

    # clears user's items from basket table
    for item in basketCont:
        db.session.delete(item)

    db.session.commit()
    
    # makes copy of basket to display to the user
    baskCopy = copy.copy(basketCont)

    # order number displayed uses the order num session
    # it increments for every user order
    if 'orderNum' not in session:
        session['orderNum'] = 1
    else:
        session['orderNum'] += 1

    return render_template('orderDone.html', name=userq.name, pageHeader=f"Order #{session['orderNum']}", orderedItems=baskCopy)

# <----------------------------- MISC ----------------------------->
@app.route("/about")
def abProd():
    return render_template('about.html', pageHeader = "About us")


# if the user tries to access a page they're unauthorized to, it will execute this
@logM.unauthorized_handler
def unauthorized():
    flash("You must be logged in to do that!", 'danger')
    return redirect(request.referrer)

