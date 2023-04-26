import datetime
from builtins import setattr, hasattr, getattr

from flask import Flask, render_template, redirect, abort, request
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from wtforms import SelectField

from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.user_form import RegisterForm, LoginForm
from forms.job_forms import JobForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
t = 0


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template('index.html', jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        for key, value in form.data.items():
            if key not in ('submit', 'password', 'password_again'):
                setattr(user, key, value)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        for field in form:
            if hasattr(job, field.name):
                setattr(job, field.name, field.data)
        job.team_leader = current_user.id
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    if not form.start_date.data:
        form.start_date.data = datetime.datetime.now()
    if not form.finished_date.data:
        form.finished_date.data = datetime.datetime.now()
    return render_template('work.html', title='Добавление новости',
                           form=form)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id)
    if current_user.id == 1:
        job = job.first
    else:
        job = job.filter(Jobs.team_leader_user == current_user).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id)
    if current_user.id == 1:
        job = job.first()
    else:
        job = job.filter(Jobs.team_leader_user == current_user).first()
    if not job:
        abort(404)
    form = JobForm()
    if request.method == "GET":
        for field in form:
            if hasattr(job, field.name):
                field.data = getattr(job, field.name)
    if form.validate_on_submit():
        for field in form:
            if hasattr(job, field.name):
                setattr(job, field.name, field.data)
        db_sess.commit()
        return redirect('/')
    return render_template('work.html',
                           title='Edit job',
                           form=form
                           )


@app.route('/statik', methods=['GET', 'POST'])
def statik():
    db_sess = db_session.create_session()
    language = SelectField('ГОД', choices=[('cpp', '2022'), ('py', '2021'), ('text', '2020')])
    return render_template('statik.html')


@app.route('/winrate')
def image1():
    return '''<img src="/static/img/DOTA2.jpg" alt="здесь должна была быть картинка, но не нашлась">'''


@app.route('/players')
def image2():
    return '''<img src="/static/img/DOTA3.jpg" alt="здесь должна была быть картинка, но не нашлась">'''


@app.route('/items')
def image3():
    return '''<img src="/static/img/DOTA4.jpg" alt="здесь должна была быть картинка, но не нашлась">'''


@app.route('/map')
def map():
    db_sess = db_session.create_session()
    return render_template('mapik.html')


@app.route('/2021')
def map1():
    return f'''<img src="/static/img/GAY1.jpg" alt="здесь должна была быть картинка, но не нашлась">
Здесь русские выиграли
'''


@app.route('/2022')
def map2():
    return f'''<img src="/static/img/GAY2.jpg" alt="здесь должна была быть картинка, но не нашлась">
Здесь русские заняли последние места
'''


@app.route('/2020')
def map3():
    return f'''<img src="/static/img/GAY3.jpg" alt="здесь должна была быть картинка, но не нашлась">
а это москва
'''


def main():
    db_session.global_init("db/db.db")
    app.run(host='0.0.0.0', port=8080, debug=True)


if __name__ == '__main__':
    main()
