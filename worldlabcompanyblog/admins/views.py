from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_user, logout_user, login_required, current_user
from worldlabcompanyblog.admins.forms import AdminLoginForm
from worldlabcompanyblog.models import User
admins = Blueprint('admins', __name__)



@admins.route('/admin_login', methods=['GET', 'POST'])
def admin_login():

	if current_user.is_authenticated:
		logout_user()
	form = AdminLoginForm()
	if form.validate_on_submit():
		email = request.form['email']
		user = User.query.filter_by(email=email).first()
		if user and user.role=='admin' and user.check_password(form.password.data):
			login_user(user)
			flash('Logged in successfully.')
			return redirect("/admin")
		else:
			flash('Invalid Email Address or Password')
	return render_template('admin_login.html', form = form)


@admins.route("/admin_logout")
@login_required
def admin_logout():
	logout_user()
	flash('You logged out!')
	return redirect(url_for('admins.admin_login'))

