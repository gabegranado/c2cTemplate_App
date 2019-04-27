
# A very simple Flask Hello World app for you to get started with...
from flask import Flask, render_template,request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
import MySQLdb
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from sqlalchemy import text
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user



app = Flask(__name__)
app.config['SECRET_KEY'] = 'devKey'
Bootstrap(app)


app.config["DEBUG"] = True
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="ggtx01",
    password="G^a70R0x",
    hostname="ggtx01.mysql.pythonanywhere-services.com",
    databasename="ggtx01$users",
)
# db = MySQLdb.connect(host='ggtx01.mysql.pythonanywhere-services.com',user='ggtx01',passwd='G^a70R0x',db='ggtx01$users',cursorclass=MySQLdb.cursors.DictCursor)
# curs = db.cursor()
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model):
    __tablename__= "users"

    id = db.Column(db.Integer, primary_key=True)
    booleanSuper=db.Column(db.Boolean)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

# class LowerUsers(db.Model):
#     __tablename__="lowerUsers"

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(15), unique=True)
#     time = db.Column(db.dateTime)
#     usersID = db.Column(db.Integer,primary_key=True)
#     content = db.Column(db.Text)

class Content(db.Model):
    __tablename__= "content"

    id = db.Column(db.Integer, primary_key=True)
    userChatroomID=db.Column(db.Integer)
    usersID = db.Column(db.Integer)
    content = db.Column(db.Text)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username= StringField('username',validators=[InputRequired(),Length(min=4,max=15)])
    password= StringField('password',validators=[InputRequired(),Length(min=8,max=80)])
class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Chatroom name', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/', methods=['GET'])
def main():
    return render_template("index.html")

@app.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                return post(3)
        return '<h1>invalid username or password</h1>'
        #return '<h1>'+form.username.data+' '+ form.password.data+'</h1>'
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password,booleanSuper=True)
        db.session.add(new_user)
        db.session.commit()

        return render_template('chatroom.html')
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('register.html', form=form)

@app.route('/post/<int:post_id>',methods=['GET','POST'])
def post(post_id):
    # post=User.query.filter_by(id=18)
    # # username=post.username
    # connection=mysql.connect('users.db')

    # stmt= 'SELECT * from content'
    # if request.method == "POST":
    #     true='true'
    #     # c = Content(content=request.form["contents"])
    #     # db.session.add(c)
    #     # db.session.commit()
    # test="testing"
    # result = db.session.execute(
    #         text("SELECT username FROM users WHERE id=:param"),
    #         {"param":1}
    #     )
    result = User.query.filter_by(id=post_id).first_or_404()
    return render_template('chatroom.html',result=result)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
