from flask import Flask,render_template,url_for ,request,flash,redirect,session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

#dbyaml=yaml.load(open('db.yml')) 
app = Flask(__name__)
app.secret_key = 'secret_key'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='mysqlroot'
app.config['MYSQL_DB']='book_shop'
db = MySQL(app)
@app.route("/")
def home():

    return render_template('index.html')
@app.route('/new_user')
def new_user():
    return render_template('ureg.html')

@app.route('/reg', methods = ['GET', 'POST'])
def reg():
   if request.method == "POST":
       details=request.form
       uname=details['uname']
       contact=details['contact']
       email=details['email']
       address=details['address']
       state=details['state']
       city=details['city']
       pin=details['pin']
       pswd=details['pswd']
       gen=details['gen']
       cur=db.connection.cursor()
       cur.execute("INSERT INTO ureg (uname,contact,email,address,state,city,pin,pswd,gen) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (uname,contact,email,address,state,city,pin,pswd,gen))
       db.connection.commit()
       cur.close()
       msg='HURRAY YOUR REGISTRATION DONE!!'
       #return url_for('/result')
   return render_template('res.html',msg=msg)
   #return redirect(url_for('sign_in'))

@app.route('/login')
def user_login():
    return render_template('user_login.html')
@app.route('/check', methods=['GET', 'POST'])
def check():
# Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'pswd' in request.form:

        email = request.form['email']
        pswd = request.form['pswd']
        # Check if account exists using MySQL
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.execute('SELECT * FROM ureg WHERE email = %s AND pswd = %s', (eamil, pswd))
        cursor.execute('SELECT * FROM ureg WHERE email = %s AND pswd = %s ', (email,pswd))
        # Fetch one record and return result
        account = cursor.fetchone()

                # If account exists in accounts table in out database
        if account:
            
        #if (un == account['un'])and(ps == account['ps']):
            #session['loggedin'] = True

            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            #session['id'] = account['uid']
            session['email'] = account['email']
            session['pswd'] = account['pswd']
            cur=db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT title,author,price,lang,condn,b_img,description from sell_book')
            books=cur.fetchall()

            # Redirect to home page
            return render_template('user_dashboard.html',uname=account['uname'],books=books)
            #return redirect(url_for('home'))
        #elif (un != account['un'])and(ps != account['ps']):
        else:
            #flash('Account doesnt exist or username/password incorrect')
            msg = 'Incorrect username/password!'
            #return redirect(_url_for(hospital_login))
            return render_template('login.html', msg=msg)
'''@app.route('/sign_in')
def sign_in():
  if 'loggedin' in session:
    cur=db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * title,author,price,lang,condn,b_img,description from sell_book')
    books=cur.fetchall()



    return render_template('user_dashboard.html' ,books=books)'''
@app.route('/sell_book')
def sell_book():
    return render_template('sell_book.html')

@app.route('/add_book', methods = ['GET', 'POST'])
def add_book():
   if request.method == "POST":
       details=request.form
       sid=details['sid']
       title=details['title']
       author=details['author']
       price=details['price']
       category=details['category']
       lang=details['lang']
       condn=details['condn']
       b_img=details['b_img']
       description=details['description']
       
       cur=db.connection.cursor()
       cur.execute("INSERT INTO sell_book (sid,title,author,price,category,lang,condn,b_img,description) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (sid,title,author,price,category,lang,condn,b_img,description))
       db.connection.commit()
       cur.close()
       #msg='BOOK ADDED!!'
       #return url_for('/result')
   #return render_template('book_added_prompt.html',msg=msg)
   return render_template('sell_book.html')

'''@app.route('/my_ac')
def my_ac():
    return render_template('my_ac.html')'''
@app.route('/show_ac_info')
def show_ac_info():
  if 'loggedin' in session:


    cur=db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * from ureg WHERE email=%s ',(session['email'],))
    data=cur.fetchone()
    
    return render_template("my_ac.html",data=data)
@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect(url_for('home'))


  




