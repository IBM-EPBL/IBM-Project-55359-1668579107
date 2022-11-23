from flask import *
from twilio.rest import Client
from werkzeug.utils import secure_filename
from flask_ngrok import run_with_ngrok
#import mysql.connector
from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import ibm_db
#from sendgridmail import sendmail
import os
#from dotenv import load_dotenv

#load_dotenv()

#conn = ibm_db.connect(os.getenv('DB_KEY'),'','')

app = Flask(__name__)

app.config['MAIL_USERNAME'] = 'priyamohan4102@gmail.com'
app.config['MAIL_PASSWORD'] = 'Priya@1234567890'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


app.app_context().push()
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = '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'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;PROTOCOL=TCPIP;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=tpp03734;PWD=kSgr4rTn5rWIthjQ",'','')



#import os
import csv

run_with_ngrok(app)
app.secret_key = "your secret key"
#myconn = mysql.connector.connect(
 #   host="localhost",
  #  user="root",
   # passwd="Root",
    #database="android")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        Username = request.form['Username']
        Password = request.form['Password']
        #cur = myconn.cursor()
       # cur.execute("""select * from admin1 where Username=%s and password=%s""", (Username, Password))
        #data = cur.fetchall()
        sql = "SELECT * FROM Admin WHERE Username =? and Password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, Username)
        ibm_db.bind_param(stmt, 2, Password)
        ibm_db.execute(stmt)
        data = ibm_db.fetch_assoc(stmt)

        if data:
            session['loggedin'] = True
            flash("Login Successfully")
            return render_template('info.html')

        else:
            flash("Incorrect Username or Password")
    return render_template("login.html")


@app.route("/")
#@app.route("/bloodbank")
def bloodbank():
    return render_template("bloodbank.html")

@app.route("/aboutus")
def about():
    return render_template("aboutus.html")


@app.route("/compat")
def compat():
    return render_template("compat.html")
@app.route("/facts")
def facts():
    return render_template("facts.html")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/eligible")
def eligible():
    return render_template("eligible.html")
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method=="POST":
        name = request.form['name']
        email = request.form['email']
        phno = request.form['phno']
        blood_group = request.form['blood_group']
        weight = request.form['weight']
        gender = request.form['gender']
        dob = request.form['dob']
        address = request.form['address']
        adharno = request.form['adharno']
        # mycur = myconn.cursor()

        # mycur.execute("select * from Donor where aadharno=(%s)" % (adharno))
        # data = mycur.fetchall()

        insert_sql = "INSERT INTO Donor1 VALUES (?,?,?,?,?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, name)
        ibm_db.bind_param(prep_stmt, 2, email)
        ibm_db.bind_param(prep_stmt, 3, phno)
        ibm_db.bind_param(prep_stmt, 4, blood_group)
        ibm_db.bind_param(prep_stmt, 5, weight)
        ibm_db.bind_param(prep_stmt, 6, gender)
        ibm_db.bind_param(prep_stmt, 7, dob)
        ibm_db.bind_param(prep_stmt, 8, address)
        ibm_db.bind_param(prep_stmt, 9, adharno)
        ibm_db.execute(prep_stmt)
        return redirect(url_for('view2'))


    else:
        return render_template("about.html")


@app.route("/view", methods=['GET', 'POST'])
def view():
    if not session.get('loggedin'):
        return render_template("login.html")
    data4 = []
    sql = "SELECT * FROM Donor1"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    dic2 = ibm_db.fetch_both(stmt)
    while dic2 != False:
        data4.append(dic2)
        dic2 = ibm_db.fetch_both(stmt)

    return render_template("view.html", data=data4)


@app.route("/delete", methods=['GET', 'POST'])
def delete():
    if not session.get('loggedin'):
        return render_template("login.html")
    if request.method == "POST":
        id = request.form['delete']
        sql = "Delete FROM Donor1 where aadharno=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, id)
    return redirect(url_for('view'))


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    if not session.get('loggedin'):
        return render_template("login.html")
    if request.method == "POST":
        id = request.form['edit']

        data5 = []

        sql = "SELECT * FROM Donor1 where aadharno=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, id)
        ibm_db.execute(stmt)
        dic2 = ibm_db.fetch_both(stmt)
        while dic2 != False:
            data5.append(dic2)
            dic2 = ibm_db.fetch_both(stmt)
        return render_template("edit.html", data=data5)

@app.route("/loginurl", methods=['GET', 'POST'])
def loginurl():
    if request.method == "POST":
        Username = request.form['Username']
        Password = request.form['Password']
        sql = "SELECT * FROM Userinfo WHERE Username =? and Password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, Username)
        ibm_db.bind_param(stmt, 2, Password)
        ibm_db.execute(stmt)
        data = ibm_db.fetch_assoc(stmt)
        if data:
            session['loggedin'] = True
            flash("Login Successfully")
            return render_template("select.html")
        else:
            print("check")
    return render_template("receiverlogin.html")


@app.route('/regurl',methods = ['POST', 'GET'])
def regurl():
    if request.method=="POST":
        username = request.form['Username']
        phone = request.form['Phone']
        email = request.form['email']
        password = request.form['Password']
        insert_sql = "INSERT INTO Userinfo VALUES (?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, username)
        ibm_db.bind_param(prep_stmt, 2, phone)
        ibm_db.bind_param(prep_stmt, 3, email)
        ibm_db.bind_param(prep_stmt, 4, password)
        ibm_db.execute(prep_stmt)
        flash("Registered Successfully")
        return render_template("receiverlogin.html")
    return render_template("receiver.html")

@app.route("/update", methods=['GET', 'POST'])
def update():
    if not session.get('loggedin'):
        return render_template("login.html")
    if request.method == "POST":
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phno = request.form['phno']
        blood_group = request.form['blood_group']
        weight = request.form['weight']
        gender = request.form['gender']
        dob = request.form['dob']
        address = request.form['address']
        adharno = request.form['adharno']
        data6 = []
        sql = "update donor1 set name=?,emailid=?,phoneno=?,bloodgroup=?,weight=?,gender=?,dob=?,address=?,aadharno=?"
        stmt = ibm_db.exec_immediate(conn, sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.bind_param(stmt, 2, email)
        ibm_db.bind_param(stmt, 3, phno)
        ibm_db.bind_param(stmt, 4, blood_group)
        ibm_db.bind_param(stmt, 5, weight)
        ibm_db.bind_param(stmt, 6, gender)
        ibm_db.bind_param(stmt, 7, dob)
        ibm_db.bind_param(stmt, 8, address)
        ibm_db.bind_param(stmt, 5, adharno)

        ibm_db.execute(stmt)
        dic2 = ibm_db.fetch_both(stmt)
        while dic2 != False:
            data6.append(dic2)
            dic2 = ibm_db.fetch_both(stmt)
        return redirect(url_for('view'))


@app.route("/view2", methods=['GET', 'POST'])
def view2():
    data2 = []
    sql2 = "SELECT * FROM Donor1"
    stmt = ibm_db.exec_immediate(conn, sql2)
    dic1 = ibm_db.fetch_both(stmt)
    while dic1 != False:
        data2.append(dic1)
        dic1 = ibm_db.fetch_both(stmt)
    if data2:
        return render_template("select.html", data=data2)


@app.route("/viewselected", methods=['GET', 'POST'])
def viewselected():
    blood_group = request.form['blood_group']
    data3 = []
    sql = "SELECT * FROM Donor1 where Bloodgroup=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, blood_group)
    ibm_db.execute(stmt)
    dic2 = ibm_db.fetch_both(stmt)
    while dic2 != False:
        data3.append(dic2)
        dic2 = ibm_db.fetch_both(stmt)
    if data3:
        return render_template("view2.html", data=data3)

@app.route("/viewall", methods=['GET', 'POST'])
def viewall():
    data1= []
    sql1 = "SELECT * FROM Donor1"
    stmt = ibm_db.exec_immediate(conn, sql1)
    dic = ibm_db.fetch_both(stmt)
    while dic !=False:
        data1.append(dic)
        dic=ibm_db.fetch_both(stmt)
    if data1:
      return render_template("view2.html", data=data1)

@app.route("/send", methods=['GET', 'POST'])
def send():
    if request.method == "POST":
        id = request.form['send']
        subject = "Plasma donor App plasma request"
        message = Mail(from_email='priyamohan4102@gmail.com', to_emails=id, subject=subject,
                       html_content='<h6>Hello {}, </h6><br/><strong> {} </strong><br/><p>Best Wishes,</p><p>Team Plasma</p>'.format(
                           "hello", 'Your request for plasma is received.'))


        API = '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'
        sg = SendGridAPIClient(API)
        from_email = "priyamohan4102@gmail.com"
        to_email = "priyakala4102@gmail.com"
        subject = "Request for Plasma"
        content = "request for plasma"
        mail = Mail(from_email, subject, to_email, content)
        response = sg.send(mail)
        print(response.status_code)
        print(response.body)
        print(response.headers)


        return redirect(url_for("view2"))


@app.route("/logout")
def logout():
    session['loggedin'] = False
    return render_template("index.html")



if __name__ == "__main__":
    app.run()
