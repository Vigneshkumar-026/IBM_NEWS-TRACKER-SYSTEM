from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape

import ibm_db
try:
  conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=txj24809;PWD=0ND0R7GUAtK2zp6A",'','')
  print("Successfully connected with db2")
except:
  print("Sorry.. Unable to connect : ", ibm_db.conn_errormsg())

app = Flask(__name__)


# Home page open aagum
@app.route('/')
def home():
  return render_template('home.html')


  
# register oda submit action
@app.route('/register',methods = ['POST', 'GET'])
def register():
  if request.method == 'POST':

    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']

    sql = "SELECT * FROM user WHERE email =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('home.html', msg="You are already a member, please login using your details")
    else:
      insert_sql = "INSERT INTO user VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, fname)
      ibm_db.bind_param(prep_stmt, 2, lname)
      ibm_db.bind_param(prep_stmt, 3, email)
      ibm_db.bind_param(prep_stmt, 4, password)
      ibm_db.execute(prep_stmt)
      return render_template('home.html', msg="Student Data saved successfuly..")

  
 

@app.route("/login", methods=["POST"])
def login():
  print("--------------------------")
  print("Inside login entrance")
  email = request.form.get("email")
  password = request.form.get("password")
  sql = "SELECT * FROM user WHERE email = ?" 
  stmt = ibm_db.prepare(conn, sql)
  ibm_db.bind_param(stmt, 1, email)
  ibm_db.execute(stmt)
  account = ibm_db.fetch_assoc(stmt)
  if not account:
    return render_template('home.html', msg="You are not yet registered, please sign up using your details")
  else:
    print("+====================================+")
    print(account)
    print("+====================================+")
    print("Inside login")
    if(password == account['PASSWORD']):
      email = account['EMAIL']
      name = account['FNAME']
      print("Going to redirect to dashboard")
      return redirect(url_for('dashboard'))
    else:
     return render_template('home.html', msg="Please enter the correct password")
     
@app.route('/dashboard')
def dashboard():
  return render_template('dashboard1.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')

