# -*- coding: utf-8 -*-

from flask import Flask,request,redirect,url_for,session,render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

from datetime import datetime
import random, os

#import jinja2, os
# jinja_environment = jinja2.Environment(autoescape=True,
#      loader=jinja2.FileSystemLoader('/Users/huangyulong/PycharmProjects/my-webapp/www/'))


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SECRET_KEY'] = ''.join(random.sample(app.secret_key, 10)) #for WTForm
bootstrap = Bootstrap(app)
moment = Moment(app)

def getDatabase(app, path=None, type='SQLite', autocommit=True):
    if type != 'SQLite':
        raise TypeError('database type not availble')

    try:
        if os.path.exists(path):
            if not os.path.isabs(path):
                os.path.abspath(path)
            if os.path.isfile(path):
                basedir, name = os.path.split(path)
            elif os.path.isdir(path):
                basedir, name = path, 'db.sqlite'
        else:
            raise ValueError('illegal path, using default path instead')
    except Exception as e:
        basedir = os.path.dirname(__file__)
        name = 'db.sqlite'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, name)
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = autocommit
    db = SQLAlchemy(app)
    return db

db = getDatabase(app)

class SignForm(FlaskForm):
    name = StringField('Please input your name here', validators=[DataRequired()])
    passwd = PasswordField('Please input your password here', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

@app.route('/', methods=['GET'])
def index():

    return render_template('index.html', name=session.get('name'), signin_page=url_for('signIn'),
                           signout_page=url_for('signOut'),current_time=datetime.utcnow())

@app.route('/signin', methods=['GET', 'POST'])
def signIn():
    form = SignForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))

    return render_template('signin.html', form=form, signin_page=url_for('signIn'),
                           signout_page=url_for('signOut'), name=session.get('name'), current_time=datetime.utcnow())

@app.route('/signfailure', methods=['GET'])
def signFailure():
    if session['login_counter'] < 5:
        return '''<h3>wrong name or password!</h3>
                <p>you have {0} chances</p>
                <a href={1}>click here to try again</a>
                '''.format(5-session['login_counter'], url_for('signIn'))
    else:
        session['status'] = 'login_fail'
        return '''<h1>No longer available</h1>'''

@app.route('/signout', methods=['GET'])
def signOut():
    #ret = '''<h3>{0} sign out session is {1}</h3>'''.format(session['username'], session)
    session.pop('name', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    pass

@app.route('/search', methods=['GET'])
def search():
    return '''<p>args is {0}</p>
                <p>values is {1}</p>
                '''.format(request.args, request.values)

@app.route('/<string:user>', methods=['GET'])
def welcome(user):
    return 'welcome {0}'.format(user) #request_data['get']['user']

if __name__ == '__main__':
    app.run(debug=True)