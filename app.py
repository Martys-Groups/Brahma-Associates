from flask import Flask, render_template,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
import json

with open("config.json", "r") as c:
    params = json.load(c)["params"]

localhost = params["local_server"]

app = Flask(__name__)
app.config['SECRET_KEY']="marty1234"
if localhost:
    app.config["SQLALCHEMY_DATABASE_URI"] =  params["local_uri"]
else:
    app.config["SQLALCHEMY_DATABASE_URI"] =  params["production_uri"]

db = SQLAlchemy()
db.init_app(app) 

class Customer(db.Model):
    Sno = db.Column(db.Integer,unique=True, primary_key=True)
    Name = db.Column(db.String)
    Father_Name = db.Column(db.String, nullable=False)
    Place = db.Column(db.String)
    Phone_No_1 = db.Column(db.Integer)
    Phone_No_2 = db.Column(db.Integer)
    Model_no = db.Column(db.String)
    capacity = db.Column(db.String)
    size = db.Column(db.String)
    Total_amt = db.Column(db.Integer)
    Paid_amt = db.Column(db.Integer)
    remaining_amt = db.Column(db.Integer)

with app.app_context():
    db.create_all()

@app.route("/")
def Customer_list():
    customers = Customer.query.all()
    return render_template("customer_list.html", customer_info = customers)


@app.route("/add_customer", methods = ["POST", "GET"])
def add_customer():
    if request.method == 'POST':
        c_name = request.form['c-name']
        f_name = request.form['F-name']
        c_place = request.form['c-place']
        phone_number_1 = request.form['phone-number-1']
        phone_number_2 = request.form['phone-number-2']
        model_no = request.form['model_no']
        capacity = request.form['capacity']
        size = request.form['size']
        # total_amt = request.form['total_amt']
        # paid_amt = request.form['paid_amt']
        # remaining_amt = int(total_amt) - int(paid_amt)

        customer = Customer(Name = c_name,
                            Father_Name = f_name,
                            Place = c_place,
                            Phone_No_1 = phone_number_1,
                            Phone_No_2 = phone_number_2,
                            Model_no = model_no,
                            # Total_amt = total_amt,
                            # Paid_amt = paid_amt,
                            # remaining_amt = remaining_amt,
                            capacity=capacity,
                            size=size)

        db.session.add(customer)
        db.session.commit()
    customer_info = Customer.query.all()
    # return render_template("Add_customer.html")
    return redirect("/dashboard")

@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
    if 'user' in session and session['user'] == params['Username']:
        customers = Customer.query.all()
        return render_template('dashboard.html',customer_info = customers)

    if request.method == 'POST':
        username = request.form['user_name']
        password = request.form['user_pass']
        if username == params["Username"] and password == params["user_pass"]:
            session['user'] = username
            customers = Customer.query.all()
            return render_template('dashboard.html',customer_info = customers)

    return render_template("login.html")

# @app.route("/customer_list")
# def Customer_list():
#     customers = Customer.query.all()
    
#     return render_template("customer_list.html", customer_info = customers)

@app.route("/delete/<int:sno>")
def delete(sno):
    customer = Customer.query.filter_by(Sno=sno).first()
    db.session.delete(customer)
    db.session.commit()
    return redirect("/dashboard") 


@app.route("/update/<int:sno>", methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        c_name = request.form['c-name']
        Total_amt = request.form['desc']
        old_paid_amt = request.form['old_Paid']
        paid_amt = request.form['paid']
        customer = Customer.query.filter_by(Sno=sno).first() 
        customer.Name = c_name
        customer.Total_amt = Total_amt
        customer.Paid_amt = old_paid_amt
        customer.Paid_amt = paid_amt
        db.session.add(customer)
        db.session.commit()
    
    customer = Customer.query.filter_by(Sno=sno).first() 
    return render_template('update.html', customer=customer)
    return redirect('/dashboard')
   



@app.errorhandler(500)
def error_500():
    return render_template("error_500.html")
@app.route("/show/<int:sno>")
def show_profile(sno):
    customer_profile = Customer.query.filter_by(Sno=sno).first()
    return render_template("c-profile.html", customer_profile = customer_profile)
if __name__ == "__main__":
    app.run(debug=True)
