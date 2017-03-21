from flask import Flask,request,redirect,url_for,session

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/', methods=['GET', 'POST'])
def index():
    ret = '''<form action="/search" method="GET">
                <h1>This is the home page!</h1>
                <p><input name="keyword" value="value" type="string" placeholder="Enter your keyword here"></p>
                <p><button type="submit">search</button>
                    <a href={0}><button type="button">sign in</button></a></p>
                </form>'''.format(url_for('signIn'))
    if session.get('status') == 'login_success':
        ret += '''<a href={0}><p><button type='button'>sign out</button></a>'''.format(url_for('signOut'))

    return ret

@app.route('/signin', methods=['GET', 'POST'])
def signIn():
    if request.method == 'GET':
        if session.get('status') == 'login_success':
            ret = '<h1>you have already login</h1>'

        else:
            ret = '''<form action="/signin" method="post">
                      <p><input name="username"></p>
                      <p><input name="password" type="password"></p>
                      <p><button type="submit">Sign In</button></p>
                      </form>'''
        return ret

    if request.method == 'POST':
        name, passwd = request.form['username'], request.form['password']
        if not 'username' in session:
            session['username'] = name
            session['login_counter'] = 0

        if name == 'admin' and passwd == '123':
            session['username'] = name
            session['status'] = 'login_success'
            session['login_counter'] = 0
            ret = '<h3>Welcome! Admin</h3>'
        else:
            session['login_counter'] += 1
            ret = redirect(url_for('signFailure'))  # '/signfailure'

        return ret

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
    ret = '''<h3>{0} sign out session is {1}</h3>'''.format(session['username'], session)
    session.pop('username', None)
    session.pop('status', None)
    return ret

@app.route('/search', methods=['GET'])
def search():
    return '''<p>args is {0}</p>
                <p>values is {1}</p>
                '''.format(request.args, request.values)

if __name__ == '__main__':
    app.run(debug=True)