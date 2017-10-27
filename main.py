from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'as8d7f98a!@qw546era#$#@$'
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  

    def __init__(self, title, body, owner_id, pub_date=None):
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
    allowed_routes = ['login', 'signup', 'blog', 'index', 'static']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/login', methods=['POST','GET'])
def login():
    username_error = ""
    password_error = ""

    if request.method == 'POST':
        password = request.form['password']
        username = request.form['username']
        user = User.query.filter_by(username=username).first()

        if user and check_pw_hash(password, user.pw_hash):
            session['username'] = username
            return redirect('/newblogpost')
        if not user:
            return render_template('login.html', username_error=" Ye Username does not exist")

        else:
            return render_template('login.html', password_error="Ye username or Ye password is incorrect") 

        return render_template('login.html')

    @app.route("/signup", methods=['POST', 'GET'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            verify = request.form['verify']
            exist = User.query.filter_by(username=username).first()
            
            username_error = ""
            password_error = ""
            verify_error = ""
            
            if username == "":
                username_error = "PLease enter YE username"
            elif len(username) <= 3 or len(username) > 20:
                    username_error = "YE username must be between 3 and 20 characters long" 
            elif "" in username:
                    username_error = "Ye username cannot conatin spaces"
            if password == "":
                password_error = "Enter Ye Password"
            elif len(password) <= 3:
                password_error = "You shall not Pass with a password leff than 3 long"
            elif "" in password:
                password_error = "No spaces for you"
            if password != verify or verify =="":
                verify_error = "Nope Dont Match"
            if exist:
                username_error = "Whoops, Already taken" 
            if len(username) > 3 and len(password) > 3 and password == verify and not exitst:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newblogpost')
            else:
                return render_template('signup.html', 
            username=username,
            username_error=username_error,
            password_error=password_error,
            verify_error=verify_error
            )
            return render_template('signup.html')

        @app.route('/blog', methods=['POST', 'GET'])
        def blog():
            blog_id = request.args.get('id')
            user_id = request.args.get('userid')
            posts = Blog.query.order_by(Blog.pubdate.desc())

            if blog_id:
                post = Blog.query.filter_by(id-blog_id).first()
                return render_template("blogpost.html", title=post.title, body=post.body, user=post.owner.username, pub_date=post.pub_date, user_id=post.owner_id)
            if user_id:
                entries = Blog.query.filter_by(owner_id=user_id).all()
                return render_template('user.html', entries=entries)

            return render_template('blog.html', posts=posts)
        @app.route('/newblogpost')
        def post():
            return render_template('newblogpost.html', title="Ye NEw Post")
        
        @app.route('/newblogpost', methods=['POST', 'GET'])
        def newblogpost():
            title = request.form['title']
            body = request.form["body"]
            owner = User.query.filter_by(username=session['username']).first()
            
            title_error = ""
            body_error = ""

            if title == "":
                title_error = "Title needed"
            if body == "":
                body_error = "We Need something here" 

            if not title_error and not body_error:
                new_post = Blog(title, body, owner)
                db.session.add(new_post)
                db.session.commit()
                page_id = new_post.id
                return redirect("/blog?id={0}".format(page_id))
            else:
                return render_template("newblogpost.html",
            title = title,
            body = body,
            title_error = title_error,
            body_error = body_error
            )

        @app.route('/logout')
        def logout():
            del session['username']
            return redirect('/')

        if __name__ == '__main__':
            app.run()




    