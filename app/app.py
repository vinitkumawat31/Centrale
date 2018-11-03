from flask import Flask, render_template,request, redirect, session
from flask_mysqldb import MySQL
import yaml
import os
from flask_uploads import UploadSet , configure_uploads , IMAGES 

UPLOAD_FOLDER = 'static/uploadedimages'


app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_FOLDER
configure_uploads(app,photos)
app.secret_key = os.urandom(24)

# configure databasesi
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/',methods=['GET','POST'])

def index():
    if request.method== 'POST' and request.form['btn'] == 'search':
        s = request.form
        category = s['category']
        if category == 'All':
            return redirect('/')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from posts where category='" + category + "'")
        posts = cur.fetchall()
        return render_template('index.html', posts = posts, category = category)
    if request.method== 'POST' and request.form['btn'] == 'sign-up':     #get form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        username = userDetails['username']
        phone_number = userDetails['phone']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * from users where username='" + username + "'")
        data = cur.fetchone()
        if data is not None :
            return 'username already exists'
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,email,username,password,phone_number) VALUES(%s,%s,%s,%s,%s)",(name,email,username,password,phone_number))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM posts")
    if resultValue > 0:
        posts = cur.fetchall()
        return render_template('index.html', posts = posts, category = None)
    return render_template('index.html')


@app.route('/users')

def users():
    
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails = userDetails)


@app.route('/login',methods=['GET','POST'])       
def login():
    if 'user' in session : 
        return redirect('/profile')
    if request.method== 'POST':     #get form data
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from users where username='" + username + "' and password='" + password + "'")
        data = cur.fetchone()
        if data is None:
            return "Username or Password is wrong"
        else:
            session['user'] = username
            session.permanent = True
            return redirect('/')


    return render_template('profile.html')       
    
@app.route('/profile',methods=['GET','POST'])
def profile():
    
    if 'user' in session:
        username = session['user']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM notifications where username = '"+username+"' ORDER BY timestamp DESC LIMIT 3")
        notify = cur.fetchall()
        cur.close()
        cur = mysql.connection.cursor()
        cur1 = mysql.connection.cursor()
        
        resultValue = cur.execute("SELECT * FROM posts where username = '" + username +"'")
        resultValue1 = cur1.execute("SELECT * FROM sharing where username = '" + username +"'")
        if resultValue>0:
            Posts = cur.fetchall()
            if resultValue1>0:
                Cabs = cur1.fetchall()
                return render_template('profile.html',Posts = Posts, Cabs = Cabs,notify=notify)
            return render_template('profile.html',Posts = Posts, Cabs = None,notify=notify)
        else :
            if resultValue1>0:
                Cabs = cur1.fetchall()
                return render_template('profile.html',Posts = None, Cabs = Cabs,notify=notify)
            return render_template('profile.html', Posts = None, Cabs = None,notify=notify)
    return redirect('/login') 
    


@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/posts',methods=['GET','POST'])
def posts():

    return render_template('post_form.html')

@app.route('/post_form',methods=['GET','POST'])
def post_form():
    if 'user' in session :
        if request.method == 'POST' and 'image' in request.files:
             postDetails = request.form
             username = session['user']
             title = postDetails['title']
             description = postDetails['description']
             price = postDetails['price']
             category = postDetails['category']
             filename = photos.save(request.files['image'])
             image_path = 'uploadedimages/' + filename

             cur = mysql.connection.cursor()
             cur.execute("SELECT * from users where username='" + username + "'")
             row = cur.fetchone()
             user_id = row[0]
             cur.close()
             cur = mysql.connection.cursor()
             cur.execute("INSERT INTO posts(username,user_id,title,description,price,image_path,category) VALUES(%s,%s,%s,%s,%s,%s,%s)",(username,user_id,title,description,price,image_path,category))
             mysql.connection.commit()
             cur.close()
        
             #return file.filename
        return render_template('post_form.html')        
    else: 
        return redirect('/login')


@app.route('/delete_post/<post_id>',methods=['GET','POST'])

def delete_post(post_id):
    if 'user' in session:
        cur = mysql.connection.cursor()
        username = session['user']
        cur.execute("SELECT * FROM posts where id = '" + post_id +"'")
        post = cur.fetchone()
        if username == post[1]:
            cur.close()
            cur = mysql.connection.cursor()
            cur.execute("DELETE  FROM posts where id = '" + post_id +"'")
            mysql.connection.commit()
            cur.close()
            return redirect('/profile')
        else:
            return 'persmission denied'
    else:
        return redirect('/login')
    return redirect('/profile')

@app.route('/post_details/<post_id>',methods=['GET','POST'])

def post_details(post_id):
    if 'user' in session:
        cur = mysql.connection.cursor()
        username = session['user'] # user whose comment
        cur.execute("SELECT * FROM posts where id = '" + post_id +"'")
        post = cur.fetchone()
        post_user = post[1]   # user whose post 
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from users where username='" + post_user + "'")
        user_data = cur.fetchone()


        if request.method== 'POST' and request.form['btn'] == 'Add-Comment':
             commentDetails = request.form
             username = session['user']
             comment = commentDetails['comment']
             cur = mysql.connection.cursor()
             cur.execute("SELECT * from users where username='" + username + "'")
             row = cur.fetchone()
             user_id = row[0]
             cur.close()
             cur = mysql.connection.cursor()
             cur.execute("INSERT INTO comment_post(username,post_id,text,user_id) VALUES(%s,%s,%s,%s)",(username,post_id,comment,user_id))
             mysql.connection.commit()
             cur.close()

             #notify
             text = "Comment on Item " + post[3]+" by "+ username
             link = "/post_details/"+post_id
             cur = mysql.connection.cursor()
             cur.execute("INSERT INTO notifications(username,text,link) VALUES(%s,%s,%s)",(post_user,text,link))
             mysql.connection.commit()
             cur.close()

             return redirect('/post_details/'+ post_id)

        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM comment_post where post_id = '" + post_id +" '")
        if resultValue > 0:
             comments = cur.fetchall()
             return render_template('post_details.html', user = user_data,post = post, comments = comments)
        return render_template('post_details.html', user = user_data,post = post)

    else:
        return redirect('/login')
    return render_template('post_details.html')

@app.route('/sharing_index',methods=['GET','POST'])

def sharing_index():
    if request.method== 'POST' and request.form['btn'] == 'search':
        s = request.form
        date = s['date']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from sharing where date='" + date + "'")
        sharing = cur.fetchall()
        return render_template('sharing_index.html', sharing = sharing, date=date)
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM sharing")
    if resultValue > 0:
        sharing = cur.fetchall()
        return render_template('sharing_index.html', sharing = sharing)
    return render_template('sharing_index.html')
         
@app.route('/cab_details/<cab_id>',methods=['GET','POST'])

def cab_details(cab_id):
    if 'user' in session:
        cur = mysql.connection.cursor()
        username = session['user']
        cur.execute("SELECT * FROM sharing where id = '" + cab_id +"'")
        cab = cur.fetchone()
        cab_user = cab[1]
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from users where username='" + cab_user + "'")
        user_data = cur.fetchone()

        if request.method== 'POST' and request.form['btn'] == 'Add-Comment':
             commentDetails = request.form
             username = session['user']
             comment = commentDetails['comment']
             cur = mysql.connection.cursor()
             cur.execute("SELECT * from users where username='" + username + "'")
             row = cur.fetchone()
             user_id = row[0]
             cur.close()
             cur = mysql.connection.cursor()
             cur.execute("INSERT INTO comment_cab(username,cab_id,text,user_id) VALUES(%s,%s,%s,%s)",(username,cab_id,comment,user_id))
             mysql.connection.commit()
             cur.close()
             #notify
             text = "Comment on Cab Sharing from " + cab[6]+"to"+cab[7]+" on "+ str(cab[3]) +" by "+ username
             link = "/cab_details/"+cab_id
             cur = mysql.connection.cursor()
             cur.execute("INSERT INTO notifications(username,text,link) VALUES(%s,%s,%s)",(cab_user,text,link))
             mysql.connection.commit()
             cur.close()

             return redirect('/cab_details/'+ cab_id)
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM comment_cab where cab_id = '" + cab_id +" '")
        if resultValue > 0:
             comments = cur.fetchall()
             return render_template('cab_details.html', user = user_data,cab = cab, comments = comments)
        return render_template('cab_details.html', user = user_data,cab = cab)

    else:
        return redirect('/login')
    return render_template('post_details.html')

@app.route('/sharing_form',methods=['GET','POST'])

def sharing_form():
    if 'user' in session :
        if request.method == 'POST':

             postDetails = request.form
             username = session['user']
             date = postDetails['date']
             time = postDetails['time']
             seats = postDetails['seats']
             source = postDetails['source']
             destination = postDetails['destination']
             price = postDetails['price']
             cur = mysql.connection.cursor()
             cur.execute("SELECT * from users where username='" + username + "'")
             row = cur.fetchone()
             user_id = row[0]
             cur.close()
             cur = mysql.connection.cursor()
             cur.execute("INSERT INTO sharing(username,user_id,date,time,seats,source,destination,price) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(username,user_id,date,time,seats,source,destination,price))
             mysql.connection.commit()
             cur.close()
        
             #return file.filename
        return render_template('sharing_form.html')        
    else: 
        return redirect('/login')
        
@app.route('/delete_comment/<comment_id>',methods=['GET','POST'])
def delete_comment(comment_id):
    if 'user' in session:
        cur = mysql.connection.cursor()
        username = session['user']
        cur.execute("SELECT * FROM comment_post where id = '" + comment_id +"'")
        comment = cur.fetchone()
        cur.close()
        if username == comment[1]:
            post_id = comment[2]
            cur = mysql.connection.cursor()
            cur.execute("DELETE  FROM comment_post where id = '" + comment_id +"'")
            mysql.connection.commit()
            cur.close()
            return redirect('/')

        else : 
            return 'persmission denied'    
    else:
        return redirect('/login')  


@app.route('/delete_cab/<cab_id>',methods=['GET','POST'])

def delete_cab(cab_id):
    if 'user' in session:
        cur = mysql.connection.cursor()
        username = session['user']
        cur.execute("SELECT * FROM sharing where id = '" + cab_id +"'")
        cab = cur.fetchone()
        if username == cab[1]:
            cur.close()
            cur = mysql.connection.cursor()
            cur.execute("DELETE  FROM sharing where id = '" + cab_id +"'")
            mysql.connection.commit()
            cur.close()
            return redirect('/profile')
        else:
            return 'persmission denied'
    else:
        return redirect('/login')
    return redirect('/profile') 
@app.route('/delete_comment_cab/<comment_id>',methods=['GET','POST'])
def delete_comment_cab(comment_id):
    if 'user' in session:
        cur = mysql.connection.cursor()
        username = session['user']
        cur.execute("SELECT * FROM comment_cab where id = '" + comment_id +"'")
        comment = cur.fetchone()
        cur.close()
        if username == comment[1]:
            post_id = comment[2]
            cur = mysql.connection.cursor()
            cur.execute("DELETE  FROM comment_cab where id = '" + comment_id +"'")
            mysql.connection.commit()
            cur.close()
            return redirect('/sharing_index')

        else : 
            return 'persmission denied'    
    else:
        return redirect('/login')  
        
@app.route('/profile/control', methods=['GET','POST'])
def profile_control():
    if 'user' in session:
        username = session['user']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM notifications where username = '"+username+"' ORDER BY timestamp DESC LIMIT 3")
        notify = cur.fetchall()
        cur.execute("SELECT * FROM notifications where username = '"+username+"' ORDER BY timestamp ")
        all_notify = cur.fetchall()
        cur = mysql.connection.cursor()
        
        cur.execute("SELECT * FROM comment_post where username = '" + username +"'")
        comment_post = cur.fetchall()
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM comment_cab where username = '" + username +"'")
        comment_cab = cur.fetchall()
        cur.close()
        return render_template('profile_control.html', comment_cab = comment_cab, comment_post=comment_post,notify = notify,all_notify=all_notify)

    else :
        return redirect('/login')    

if __name__ == '__main__':
    app.run(debug=True)