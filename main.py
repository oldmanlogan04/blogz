
from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner
        
class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash('Yule log in')
            return render_template('newblogpost.html')
        else:
            if user and user.password != password or len(username) < 3 or len(username) > 20 or len(password) < 3 or len(password) > 20 or username == "" or password == "":
                flash('You shall not pass')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']           
        if username == "" or len(username) < 3 or len(username) > 20:
            flash('Ye need to be between 3-20')
            return redirect('/signup')
        if password == "" or len(password) < 3 or len(password) > 20:
            flash('Ye need to be between 3-20')
            return redirect('/signup')
        if verify == "" or len(verify) < 3 or len(verify) > 20:
            flash('Its still between 3-20')
            return redirect('/signup')
        if verify != password:
            flash('YE Must Match to Pass')
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            flash('Your In')
            return render_template('newblogpost.html')
        else:
            flash('Ye has already been named')
    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/', methods=['GET'])
def index():
    users = User.query.all()
    return render_template("index.html", users=users)
        

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    blog_id = request.args.get('blog_id')
    user_id = request.args.get('user_id')

        
    if blog_id != None:
        flash("You shall pass with that id", blog_id)
        blogposts= Blog.query.get(blog_id)
        flash(blogposts)
        return render_template('blogposts.html', blogposts=blogposts)

    if user_id != None:
        print("Han Solo user=", user_id)
        user_blogs = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('solouser.html', solouser=solouser)

    blogs = Blog.query.all()
    print("all ye blogs")
    return render_template("blog.html", blogs=blogs)
        

@app.route('/newblogpost', methods=['GET', 'POST'])
def newblogpost():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        if blog_title == '' or blog_body == '':
            flash('Need something here in the fields')
            return render_template('newblogpost.html')
        blog = Blog(blog_title, blog_body, owner)
        db.session.add(blog)
        db.session.commit()
        return redirect('/blog?id=' + str(blog.id))
    else:
        if request.method == 'GET':
            return render_template('newblogpost.html', title="Add Ye Blog")

        
@app.route('/blogposts', methods=['POST', 'GET'])
def blogposts():
   if request.method == 'POST':
       blogposts = request.form['blogposts']
       add_entry = Blog(blogposts)
       if request.method == 'GET':
           users = User.query.all()
       return render_template('index.html', title="YE Blogz", users=users)
       db.session.add(add_entry)
       db.session.commit()
       return redirect('/blog?id=' + str(blog.id))
   # else:
   #     if request.method == 'GET':
    #    return render_template('blogposts.html')    

@app.route('/solouser', methods=['GET'])
def solouser():
    username = request.form['username']
    db.session.add(add_entry)
    db.session.commit()
    return render_template('solouser.html')    


if __name__ == '__main__':
    app.secret_key = "!dontl!keblog$"
    app.run()   
    




    
