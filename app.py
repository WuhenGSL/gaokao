from flask import Flask, flash, redirect, request, url_for, render_template, session, render_template_string, jsonify
from models import RegisterForm, db, LoginForm, User, Schools, UserSelection, AddSelectionForm, Tyca, Specialty
from models import Feature, Province, Display
from sqlalchemy.sql import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost:3306/userdb'
app.config['SQLALCHEMY_BINDS'] = {
    'database': 'mysql+pymysql://root:12345678@localhost:3306/database'
}
app.config['SECRET_KEY'] = '12345678'
db.init_app(app)

cnt = 0


@app.route('/')
def index():
    return render_template('index.html')


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


def get_list(rank, selection1, selection2, selection3, flag):
    minrank = float(rank) - float(rank) * 0.005 * 50  # 最小名次  minrank 冲 bound1 稳 bound2 保 bound2+10000
    bound1 = float(rank) + float(rank) * 0.01 * 9
    bound2 = float(rank) + float(rank) * 0.01 * 39
    # list=School.query.get(1)
    if flag == 1:
        lists = Schools.query.filter(Schools.forelowest_rank > minrank, Schools.forelowest_rank < bound1,
                                    or_(Schools.mustspe == selection1, Schools.mustspe == selection2,
                                        Schools.mustspe == selection3,
                                        Schools.mustspe == None))  # 冲  注意返回值的是query ","而不用and ,导入_and,_or后使用，None与Null

    elif flag == 2:
        lists = Schools.query.filter(Schools.forelowest_rank > bound1, Schools.forelowest_rank < bound2,
                                    or_(Schools.mustspe == selection1, Schools.mustspe == selection2,
                                        Schools.mustspe == selection3, Schools.mustspe == None))  # 稳

    elif flag == 3:
        lists = Schools.query.filter(Schools.forelowest_rank > bound2, Schools.forelowest_rank < bound2 + 10000,
                                    or_(Schools.mustspe == selection1, Schools.mustspe == selection2,
                                        Schools.mustspe == selection3, Schools.mustspe == None))  # 保

    return lists


def get_probability(rank, lists, flag):
    if flag == 1:
        for sc in lists:
            probability = int(50 + ((sc.forelowest_rank) - int(rank)) / (float(rank) * 0.005)) + 1
            sc.probability = probability

    elif flag == 2:
        for sc in lists:
            probability = int(50 + ((sc.forelowest_rank) - int(rank)) / (float(rank) * 0.01)) + 1
            sc.probability = probability

    elif flag == 3:
        for sc in lists:
            probability = int(50 + ((sc.forelowest_rank) - int(rank)) / (float(rank) * 0.01)) + 1
            if probability > 99:
                probability = 99
            sc.probability = probability


@app.route('/add_selection/', methods=['GET', 'POST'])
def add_selection():
    form = AddSelectionForm()

    page = request.args.get('page', 1, type=int)
    PER_PAGE = 10

    username = session['user_name']
    user = User.query.filter_by(name=username).first()
    list1 = get_list(user.rank, user.subject1, user.subject2, user.subject3, 1)
    list2 = get_list(user.rank, user.subject1, user.subject2, user.subject3, 2)
    list3 = get_list(user.rank, user.subject1, user.subject2, user.subject3, 3)
    get_probability(user.rank, list1, 1)
    get_probability(user.rank, list2, 2)
    get_probability(user.rank, list3, 3)
    schools1 = list1.paginate(page=page, per_page=PER_PAGE, error_out=False)
    schools2 = list2.paginate(page=page, per_page=PER_PAGE, error_out=False)
    schools3 = list3.paginate(page=page, per_page=PER_PAGE, error_out=False)

    if request.method == 'POST':
        if form.validate_on_submit():
            id = form.id.data
            school = Schools.query.filter_by(id=id).first()
            max_id = db.session.execute('SELECT MAX(id) FROM userselection').scalar()

            if max_id is None:
                max_id = 0

            new_info = UserSelection(id=max_id+1,
                                     school=school.school,
                                     specialty=school.specialty,
                                     lowest_rank=school.forelowest_rank,
                                     feature=school.feature,
                                     probability=school.probability,
                                     name=username)

            db.session.add(new_info)
            db.session.commit()

    return render_template('add_selection.html',
                           Schools1=schools1,
                           Schools2=schools2,
                           Schools3=schools3,
                           form=form)


@app.route('/selection/', methods=['GET', 'POST'])
def selection():
    username = session['user_name']
    user = UserSelection.query.filter_by(name=username).all()
    information = User.query.filter_by(name=username).first()
    total = UserSelection.query.count()

    form = AddSelectionForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            id = form.id.data
            to_delete = UserSelection.query.get_or_404(id)
            db.session.delete(to_delete)
            db.session.commit()
            db.session.execute(f'UPDATE userselection SET id = id - 1 WHERE id > {id}')
            db.session.commit()
            return render_template_string("""
                    <script>
                        window.location.href = "{{ url_for('selection') }}";
                    </script>
                """)

    return render_template('selection.html', Users=user, info=information, total=total, form=form)


@app.route('/specialty')
def find_specialty():
    types = Tyca.query.filter()
    lists = []
    for i in types:
        listt = [i.type]
        specialties = Specialty.query.filter(Specialty.type == i.type)
        for j in specialties:
            listt.append(j.specialty)
        lists.append(listt)
    return render_template('specialty.html', lists=lists, types=types)


@app.route('/school/', methods=['GET', 'POST'])
def find_school():
    features = Feature.query.filter()  # 所有特色query
    provinces = Province.query.filter()  # 所有省query
    schools = Display.query.filter()  # 所有大学query
    return render_template('school.html', provinces=provinces, features=features, schools=schools)


@app.route('/chart')
def chart():

    return render_template('chart.html')


if __name__ == '__main__':
    app.run(port=8000, debug=True)
