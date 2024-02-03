from myshop import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# table for products
class Products(db.Model):
    itemID = db.Column(db.Integer, primary_key = True)
    itemName = db.Column(db.String(100))
    itemPrice = db.Column(db.Integer)
    itemDesc = db.Column(db.String(500))
    itemDescList = db.Column(db.String(500))
    itemPic = db.Column(db.String(50))
    newProductBool = db.Column(db.Boolean)
    itemCat = db.Column(db.String(100))
    itemCO2 = db.Column(db.Integer)

    # adds items to product table
    @staticmethod
    def setItemID( itemName, itemPrice,itemDesc,itemDescList,itemPic,newProductBool,itemCat,itemCO2):
        newitem = Products(itemName = itemName,itemPrice=itemPrice, itemDesc = itemDesc,itemDescList=itemDescList, itemPic = itemPic, newProductBool = newProductBool,itemCat=itemCat,itemCO2=itemCO2)
        db.session.add(newitem)
        db.session.commit()

# table for adverts
class Adverts(db.Model):
    AdvertID = db.Column(db.Integer, primary_key = True)
    advertLink = db.Column(db.String(50))

    # adds adverts to advert table
    @staticmethod
    def setAdverts(AdvertID, advertLink):
        newAd = Adverts(AdvertID = AdvertID, advertLink = advertLink)
        db.session.add(newAd)
        db.session.commit()

# table for users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(100))

    def set_hash_pass(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_pass_hash(self, password):
        return check_password_hash(self.password_hash, password)
    
    # add new user
    @staticmethod
    def registerUser(name, email, password):
        print("New user added to DB")
        user = User(name=name, email=email)
        user.set_hash_pass(password)
        db.session.add(user)
        db.session.commit()
        return user

# Stores basket contents of logged in users
class BasketContent(db.Model):
    baskNum = db.Column(db.Integer, primary_key=True)
    prodID = db.Column(db.Integer)
    prodName = db.Column(db.String(50))
    prodImg = db.Column(db.String(50))
    addedbyEmail = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    totPrice = db.Column(db.Integer)

    # add item to basket
    @staticmethod
    def addtobask(prodID,prodName,prodImg,addedbyEmail):
        priceOfOne = Products.query.filter_by(itemID=prodID).first()
        alreadyInBask = BasketContent.query.filter_by(prodID=prodID, addedbyEmail=addedbyEmail).first()

        # if item not in basket, add quantity 1
        if not alreadyInBask:
            print(f"Item added: {prodName}")
            prodBask = BasketContent(prodID=prodID,prodName=prodName,prodImg=prodImg,addedbyEmail=addedbyEmail,quantity=1, totPrice=priceOfOne.itemPrice)
            db.session.add(prodBask)
            db.session.commit()
        
        # if item in basket, add 1 to the quantity
        else:
            print("Item already in basket:")
            print(f"product quantity +1 for {prodName}")
            alreadyInBask.quantity += 1
            alreadyInBask.totPrice += priceOfOne.itemPrice
            db.session.commit()

    # remove item from basket
    @staticmethod
    def remfromBask(prodID, addedbyEmail):
        alreadyInBask = BasketContent.query.filter_by(prodID=prodID, addedbyEmail=addedbyEmail).first()
        priceOfOne = Products.query.filter_by(itemID=prodID).first()

        # if item not in basket, do nothing
        if not alreadyInBask:
            return
        
        # if item in basket, minus 1 from quantity
        else:
            alreadyInBask.quantity -= 1
            alreadyInBask.totPrice -= priceOfOne.itemPrice
            if alreadyInBask.quantity == 0:
                db.session.delete(alreadyInBask)
        
        db.session.commit()
    
    # within basket add button
    @staticmethod
    def addtoBasketINBASK(prodID, addedbyEmail):
        priceOfOne = Products.query.filter_by(itemID=prodID).first()
        alreadyInBask = BasketContent.query.filter_by(prodID=prodID, addedbyEmail=addedbyEmail).first()
        alreadyInBask.quantity += 1
        alreadyInBask.totPrice += priceOfOne.itemPrice
        db.session.commit()

# stores reviews into table
class Reviews(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    itemID = db.Column(db.Integer)
    name = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    revWriting = db.Column(db.String(200))

    # adds review
    @staticmethod
    def addReview(name, itemID, rating, revWriting):
        addtoRev = Reviews(name=name,itemID=itemID, rating=rating,revWriting=revWriting)
        db.session.add(addtoRev)
        db.session.commit()
