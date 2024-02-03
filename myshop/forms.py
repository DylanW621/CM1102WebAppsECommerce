from flask_wtf import FlaskForm
from wtforms import PasswordField, validators, StringField


# user registration form
class UserReg(FlaskForm):
    name = StringField("Enter your name", [validators.DataRequired(), validators.length(min=1, max=50)])
    email = StringField("Enter your email", [validators.DataRequired(), validators.length(min=1, max=50)])
    password = PasswordField('Enter your password', [validators.DataRequired(), validators.EqualTo('conf', message='The passwords dont match')])
    conf = PasswordField('Re-enter your password', [validators.DataRequired()])

# login form
class UserLogin(FlaskForm):
    email = StringField("Enter email")
    password = PasswordField('Enter Password')

# checkout form
class CheckoutForm(FlaskForm):
    addFirst = StringField("Street address", [validators.DataRequired(), validators.length(max=100)],render_kw={"onfocus": "street()", "oninput":"street()"})
    addTown = StringField("Town/City", [validators.DataRequired(), validators.length(max=100)], render_kw={"onfocus": "town()", "oninput":"town()"})
    addPost = StringField("Postcode", [validators.DataRequired(), validators.length(max=15)], render_kw={"onfocus": "postcode()", "oninput":"postcode()"})
    
    cardN = StringField("Card number", [validators.DataRequired(), validators.length(max=19)], render_kw={"oninput": "cardNum()", "onfocus":"cardNum()"})
    cvv = StringField("CVV", [validators.DataRequired(), validators.length(max=3)], render_kw={"oninput": "cardcvv()", "onfocus":"cardcvv()"})
    expDate = StringField("Expiry date", [validators.DataRequired(), validators.length(max=5)], render_kw={"oninput": "cardexp()", "onfocus":"cardexp()"})
    cardhName = StringField("Cardholder name", [validators.DataRequired(), validators.length(min=1, max=50)], render_kw={"oninput": "cardH()", "onfocus":"cardH()"})

