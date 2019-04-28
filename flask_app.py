
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
    lowerPassword = db.Column(db.String(80))

class LowerUsers(db.Model):
    __tablename__="lowerUsers"

    id = db.Column(db.Integer, primary_key=True)
    userChatroomID=db.Column(db.Integer)
    username = db.Column(db.String(15), unique=False)
    password = db.Column(db.String(80))

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
    username= StringField('chatroom name',validators=[InputRequired(),Length(min=4,max=15)])
    name= StringField('name',validators=[InputRequired(),Length(min=4,max=15)])
    password= StringField('password',validators=[InputRequired(),Length(min=8,max=80)])
class MLoginForm(FlaskForm):
    username= StringField('chatroom name',validators=[InputRequired(),Length(min=4,max=15)])
    password= StringField('password',validators=[InputRequired(),Length(min=8,max=80)])
class SetLowerForm(FlaskForm):
    name= StringField('name',validators=[InputRequired(),Length(min=4,max=15)])
class ChatForm(FlaskForm):
    content= StringField('content',validators=[InputRequired(),Length(min=0,max=9000)])
class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Chatroom name', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    lowerPassword = PasswordField('password for sub users', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/', methods=['GET'])
def main():
    return render_template("index.html")

@app.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        lUser=LowerUsers.query.filter_by(userChatroomID=user.id,username=form.name.data).first()
        if user:
            if check_password_hash(lUser.password, form.password.data):
                return post(user.id,lUser.id)
        return '<h1>invalid username or password</h1>'
        #return '<h1>'+form.username.data+' '+ form.password.data+'</h1>'
    return render_template('login.html', form=form)

@app.route('/mLogin', methods=['GET','POST'])
def mLogin():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                return mPost(user.id)
        return '<h1>invalid username or password</h1>'
        #return '<h1>'+form.username.data+' '+ form.password.data+'</h1>'
    return render_template('masterLogin.html', form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        hashed_lowerPassword = generate_password_hash(form.lowerPassword.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password,lowerPassword=hashed_lowerPassword,booleanSuper=True)
        db.session.add(new_user)
        db.session.commit()
        user=User.query.filter_by(username=form.username.data).first()
        return setLUsers(user.id)
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('register.html', form=form)

@app.route('/setLUsers/<int:post_id>',methods=['GET','POST'])
def setLUsers(post_id):
    form=SetLowerForm()
    user=User.query.filter_by(id=post_id).first()
    if form.validate_on_submit():
        lowerUser = LowerUsers(userChatroomID=post_id,username=form.name.data,password=user.lowerPassword)
        db.session.add(lowerUser)
        db.session.commit()
        return render_template('registerLUsers.html',postId=post_id,form=form)
    return render_template('registerLUsers.html',postId=post_id,form=form)

@app.route('/mPost/<int:mPost_id>',methods=['GET','POST'])
def mPost(mPost_id):
    filtered_content=Content.query.filter_by(userChatroomID=mPost_id)
    return render_template('ITSide.html',postId=mPost_id,form=form,comments=filtered_content)
    # if form.validate_on_submit():
    #     # return '<h1>' + form.content.data+ '</h1>'
    #     chatroomFil = Content(userChatroomID=post_id,usersID=1,content=form.content.data)
    #     db.session.add(chatroomFil)
    #     db.session.commit()
    #     return render_template('chatroom.html',postId=post_id,form=form,comments=filtered_content)


@app.route('/post/<int:post_id>/<int:lUser_id>',methods=['GET','POST'])
def post(post_id,lUser_id):
    form=ChatForm()
    filtered_content=Content.query.filter_by(userChatroomID=post_id)
    if form.validate_on_submit():
        # return '<h1>' + form.content.data+ '</h1>'
        chatroomFil = Content(userChatroomID=post_id,usersID=lUser_id,content=form.content.data)
        db.session.add(chatroomFil)
        db.session.commit()
        return render_template('chatroom.html',postId=post_id,form=form,lUserId=lUser_id,comments=filtered_content)
    return render_template('chatroom.html',postId=post_id,form=form,lUserId=lUser_id,comments=filtered_content)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
