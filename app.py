from flask import Flask,render_template, session,url_for,redirect,request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_required,login_user,logout_user,current_user



app = Flask(__name__)
app.config['SECRET_KEY']='thisisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db=SQLAlchemy(app)



login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def get(id):
    return User.query.get(id)


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(200),nullable=False,unique=True)
    email=db.Column(db.String(200),nullable=False)
    phone=db.Column(db.Integer,nullable=False)
    password=db.Column(db.String(200),nullable=False)
    
@app.route('/home',methods=['GET'])
@login_required
def home():
    return render_template('home.html')

@app.route('/participants')
def participants():
    return render_template('participants.html')

@app.route('/',methods=['GET'])
@app.route('/login',methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/register',methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/',methods=['POST'])
@app.route('/login',methods=['POST'])
def login_post():
    username=request.form['username']
    password=request.form['password']
    user= User.query.filter_by(username=username,password=password).first()
    login_user(user)
    return redirect('/home')
    
    

@app.route('/register',methods=['POST'])
def register_post():
    username=request.form['username']
    email=request.form['email']
    phone=request.form['phone']
    password=request.form['password']
    user = User(username=username,email=email,phone=phone,password=password)
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(username=username).first()
    flash("Account Created Successfully","success")
    return redirect('/')
    

@app.route('/logout',methods=['GET'])
def logout():
    if "user" in session:
        user = session['user']
    logout_user()
    flash("You have been logged out.", category ='success')
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
