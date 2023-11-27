import numpy as np
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import pickle
import bcrypt
import os

app = Flask(__name__)

rf = pickle.load(open('Saved Model/final_rf_model.pkl', 'rb')) # Load pickle object

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pcostest_database'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = '*^%SecretKey%^**'

mysql = MySQL(app)
  


@app.route('/')
def home():
    return render_template("home.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['reg_name']
        email = request.form['reg_email']
        password = request.form['reg_password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pcostest (name, email, password)  VALUES (%s, %s, %s)",(name, email, hash_password,))
        mysql.connection.commit()
        session['name'] = name
        session['email'] = email
        return redirect(url_for("login")) #method name instead of page name



@app.route('/login', methods=["GET","POST"])
def login():
    #img1 = os.path.join(app.config['UPLOAD_FOLDER'], 'brain.png')

    if request.method == "POST":
        email = request.form['log_email']
        password1 = request.form['log_password'].encode('utf-8')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        result = cur.execute("SELECT * FROM pcostest WHERE email=%s",(email,))

        if result>0:
            
            data = cur.fetchone()

            if bcrypt.hashpw(password1,data['password'].encode('utf-8')) == data['password'].encode('utf-8'):
                session['login'] = True
                session['name'] = data['name']
                return redirect(url_for('pcosTest'))
            else:
                 return "email or password doesn't match"
            
        else:
             return "email or name is incorrect"

    
    else:
        return render_template("login.html")



    
@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")




####### PCOS Test ######

@app.route('/pcosTest')
def pcosTest():
    return render_template('pcostest.html')



@app.route('/predict',methods=['POST'])
def predict():
    if request.method=='POST':
       intput_features = [float(x) for x in request.form.values()]
       final_features = [np.array(intput_features)]
       prediction = rf.predict(final_features)
      
       if prediction == 1:
           output = "The patient is PCOS Positive"
       if prediction == 0:
           output="The patient is PCOS Negative"
       

    return render_template('predict.html', outcome = output)


if __name__ == "__main__":
    app.run(debug=True)