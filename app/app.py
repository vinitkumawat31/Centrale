from flask import Flask, render_template,request, redirect
from flask_mysqldb import MySQL
import yaml
app = Flask(__name__)

# configure database
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/',methods=['GET','POST'])



def index():
	if request.method== 'POST':		#get form data
		userDetails = request.form
		name = userDetails['name']
		email = userDetails['email']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO users(name,email) VALUES(%s,%s)",(name,email))
		mysql.connection.commit()
		cur.close()
		return redirect('/users')
	return render_template('index.html')


@app.route('/users')

def users():
	
	cur = mysql.connection.cursor()
	resultValue = cur.execute("SELECT * FROM users")
	if resultValue > 0:
		userDetails = cur.fetchall()
		return render_template('users.html',userDetails = userDetails)


@app.route('/profile/<username>')		
def profile(username):
		cur = mysql.connection.cursor()
		resultValue = cur.execute("SELECT * FROM users")
		names = cur.execute("SELECT name FROM users ")

		#for name in names:
		#	if user == username:
		#		x=1
		#		break

		#if x==1 :
		return render_template('profile.html', username=username)
		#else :
		 #return redirect('/users')


if __name__ == '__main__':
	app.run(debug=True)