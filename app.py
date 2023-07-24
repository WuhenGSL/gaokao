from flask import Flask, flash, redirect, request, url_for, render_template,jsonify
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
def master():
    return 'hello!'


@app.route('/user', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()

    if request.method == 'POST':
        if request.form['action'] == 'login':
            if login_form.validate_on_submit():
                email = login_form.email.data
                password = login_form.password.data
                user = User.query.filter(User.email == email).first()

                if user and user.check_password(password):
                    flash('登录成功', 'success')
                    return redirect('/')  # 重定向到根目录
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






@app.route('/login1', methods=['GET', 'POST'])
def login1():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter(User.email == email).first()  # 使用filter方法而不是filter_by
        if user and user.check_password(password):
            flash('登录成功', 'success')
            return redirect(url_for('index'))
        else:
            flash('登录失败，请验证邮箱和密码', 'error')

    return render_template('login1.html', form=form)


@app.route('/register1', methods=['GET', 'POST'])
def register1():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if User.query.filter_by(email=email).all():
            flash('该邮箱已被注册', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('确认密码与密码不一致', 'error')
            return redirect(url_for('register'))

        try:
            new_user = User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('注册成功！请登录', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'注册失败: {e}', 'error')

    return render_template('register.html', form=form)



@app.route('/schools')
def show_schools():
    # 获取学校信息
    schools = school_db_manager.get_all_schools()
    return render_template('schools.html', schools=schools)


if __name__ == '__main__':

    app.run(port=8000, debug=True)
