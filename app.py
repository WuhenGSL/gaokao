from flask import Flask, flash, redirect, request, url_for, render_template, session
from models import RegisterForm, db, LoginForm, User
from flask_sijax import Sijax

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost:3306/userdb'
app.config['SQLALCHEMY_BINDS'] = {
    'database': 'mysql+pymysql://root:12345678@localhost:3306/database'
}
app.config['SECRET_KEY'] = '12345678'
db.init_app(app)

path = "static/js/sijax"
app.config['SIJAX_STATIC_PATH'] = path
app.config['SIJAX_JSON_URI'] = path + 'json2.js'
Sijax(app)


@app.route('/')
def index():
    return 'hello!'


@app.route('/login/', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()

    if 'user_name' in session:
        check = User.query.filter_by(name=session['user_name']).first()
        if check.score == 0:
            return redirect(url_for('profile'))
        elif check.score != 0:
            return redirect(url_for('user_profile'))

    if request.method == 'POST':
        if request.form['action'] == 'login':
            if login_form.validate_on_submit():
                email = login_form.email.data
                password = login_form.password.data
                user = User.query.filter(User.email == email).first()

                if user and user.check_password(password):
                    session['user_name'] = user.name
                    flash('登录成功', 'success')
                    return redirect(url_for('index'))  # 重定向到根目录
                else:
                    flash('登录失败，请检查邮箱或密码', 'error')

        elif request.form['action'] == 'register':
            if register_form.validate_on_submit():
                name = register_form.name.data
                email = register_form.email.data
                password = register_form.password.data
                confirm_password = register_form.confirm_password.data

                if User.query.filter_by(email=email).all():
                    flash('该邮箱已被注册', 'error')
                elif password != confirm_password:
                    flash('确认密码与密码不一致', 'error')
                else:
                    new_user = User(name=name, email=email, password=password)
                    db.session.add(new_user)
                    db.session.commit()
                    flash('注册成功', 'success')

    return render_template('login.html', login_form=login_form, register_form=register_form)


@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    username = session['user_name']
    user = User.query.filter_by(name=username).first()

    if request.method == 'POST':
        score = int(request.form['score'])
        rank = int(request.form['rank'])
        selected_subjects = request.form.get('selectedSubjects').split(',')

        if user:
            user.score = score
            user.rank = rank
            user.subject1 = selected_subjects[0]
            user.subject2 = selected_subjects[1]
            user.subject3 = selected_subjects[2]

            try:
                db.session.commit()
                return redirect(url_for('user_profile'))
            except Exception as e:
                print(e)
    return render_template('profile.html')


@app.route('/user_profile/', methods=['GET', 'POST'])
def user_profile():
    username = session['user_name']
    user = User.query.filter_by(name=username).first()
    return render_template('user_profile.html', user=user)


@app.route('/logout/')
def logout():
    session.pop('user_name', True)
    flash('注销成功')
    return redirect('/')


if __name__ == '__main__':
    session.clear()
    app.run(port=8000, debug=True)
