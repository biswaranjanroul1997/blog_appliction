from flask.helpers import url_for
from codejana_flask import app,db,bcrypt,mail
from flask import render_template,redirect,flash
# from codejana_flask import forms
from codejana_flask.forms import RegistrationForm,LoginForm,ResetRequestForm,ResetPasswordForm,AccountUpdateForm
from codejana_flask.models import User
from flask_login import login_user,logout_user,current_user,login_required
from flask_mail import Message
import os


@app.route('/')
def homepage():
    return render_template('homepage.html',titel ="Home")

@app.route("/about")
@login_required
def about():
    return render_template('about.html',titel='About')    

def save_image(picture_file):
    picture_name = picture_file.filename
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_name)
    picture_file.save(picture_path)
    return picture_name


@app.route('/account',methods=['POST','GET'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        image_file = save_image(form.picture.data)
        current_user.image_file = image_file
        db.sesssion.commit()
        return redirect(url_for("account"))
    image_url =url_for('static',filename ='profile_pics/'+current_user.image_file)    
    return render_template('account.html', titel='Account',legend='Enter Your Accounts Details',form=form,image_url=image_url)    

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=encrypted_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created Successfully for {form.username.data}',category = 'success')
        return redirect(url_for('login'))

    return render_template('register.html',titel='Singup',form=form)   

@app.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form =LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if form.email.data == user.email and  form.password.data == user.password:
        if user and  bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            flash(f'Login Successfully for {form.email.data}',category = 'success')
            return redirect(url_for('account'))
        else:
            flash(f'Login  UnSuccessfully for {form.email.data}',category = 'danger')
              
     
    return render_template('login.html',titel='login',form = form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))  

def send_mail():
    token = user.get_token()
    msg = Message('Password Reset Request',recipients=[user.email],sender='noreply@codejan.com')
    msg.body=f'''To reset your password.Please follow the link below.
    
    {url_for('reset_token',token=token, _external =True)}

    if you didn't send a password reset request.Please follow the link below.
    
    '''
    mail.send(msg)  

@app.route('/reset_password',methods=['POST','GET'])
def reset_request():
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_mail(user)
        flash("Rest Request sent. Check your mail.", category= 'success')
        return redirect(url_for('login'))
    return render_template('reset_request.html',titel = 'Reset Request',form= form)

@app.route('/reset_password/<token>',methods= ['POST','GET'])
def reset_token(token):
    user = User.verify_token(token)
    if user is None:
        flash("That is Invalid token or expired, Please try again.",'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Password Chnage! Please login!','success')
        return redirect(url_for('login'))
    return render_template('change_password.html',titel='Change Password',form =form)    
            
