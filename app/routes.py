from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, LiftForm, LiftClaimForm, LiftDeleteForm
from app.models import User, Lift, UserLift
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required                                                                        
def index():
    lifts = Lift.query.filter(Lift.seats > 0)                                                           
    return render_template('index.html', title='Home', lifts=lifts)


@app.route('/login', methods=['GET', 'POST'])                                           
def login():
    if current_user.is_authenticated:                                                   
        return redirect(url_for('index'))                                               
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)                
        user.set_password(form.password.data)
        db.session.add(user)                                                          
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    goalLift = []
    user = User.query.filter_by(username=username).first_or_404()
    offeredlifts_display = user.lifts.order_by(Lift.date.desc())                                                   
    lift = UserLift.query.filter_by(userId=current_user.id)
    liftIdList = []
    for userlift in lift:
        liftIdList.append(userlift.liftId)
    for x in liftIdList:                                                                                            
        goal = Lift.query.filter_by(id=x)
        goalLift.append(goal[0])

    return render_template('user.html', title=username, user=user, lifts = offeredlifts_display, morelifts = goalLift)              


@app.route('/createlift', methods=['GET', 'POST'])
@login_required
def create_lift():
    form = LiftForm()
    if form.validate_on_submit():                                                                                       
        lift = Lift(date=form.date.data,                                                                               
                    start_loc=form.start_loc.data, end_loc=form.end_loc.data, seats=form.seats.data, user_id_driving = current_user.id)        
        db.session.add(lift)                                                                                            
        db.session.commit()
        flash('Lift has been created')
        return redirect(url_for('index'))                                                                               
    return render_template('lift.html', title='Create Lift', form=form)


@app.route('/lift/<lift_id>', methods=['GET', 'POST'])
@login_required
def lift_details(lift_id):
    form = LiftClaimForm()
    lift = Lift.query.filter_by(id=lift_id).first()
    if not lift.user_id_driving == current_user.id :    
        if request.method == 'POST':
            lift.seats = lift.seats -1
            userlift = UserLift(liftId=lift.id, userId=current_user.id)
            db.session.add(userlift)
            db.session.commit()
            flash("SUCCESS! The lift is your's!")
            return redirect(url_for('index'))
    else:
        flash("You cannot claim your own offer.")
        return redirect(url_for('index'))
    return render_template('lift_details.html', title='Lift details', lift=lift, form=form)


@app.route('/user/<username>/lift/<lift_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_lift(lift_id, username):
    form = LiftDeleteForm()
    lift = Lift.query.filter_by(id=lift_id).first()
    if request.method == 'POST':
        db.session.delete(lift)
        db.session.commit()
        flash("Your offer has been deleted.")
        return redirect(url_for('user', username=current_user.username))
    return render_template('delete_lift.html', title='Delete lift', lift=lift, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
