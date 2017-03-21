from flask import Flask,request,redirect,url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def getHome():
    return '''<form action="/search" method="GET">
                <h1>This is the home page!</h1>
                <p><input name="keyword" value="value" type="string" placeholder="Enter your keyword here"></p>
                <p><button type="submit">search</button>
                    <a href={0}><button type="button">sign in</button></a></p>
                </form>'''.format(url_for('signIn'))

@app.route('/signin', methods=['GET'])
def signinForm():
    return '''<form action="/signin" method="post">
                  <p><input name="username"></p>
                  <p><input name="password" type="password"></p>
                  <p><button type="submit">Sign In</button></p>
                  </form>'''

@app.route('/signin', methods=['POST'])
def signIn():
    name, passwd = request.form['username'], request.form['password']
    if name == 'admin' and passwd == '123':
        return '<h3>Welcome!</h3>'
    else:
        return redirect(url_for('signFailure'))  # '/signfailure'

@app.route('/signfailure', methods=['GET'])
def signFailure():
    return '''<h3>wrong name or password!</h3>
                <a href={0}>click here to try again</a>
                '''.format(url_for('signIn'))

@app.route('/search', methods=['GET'])
def search():
    return '''<p>args is {0}</p>
                <p>values is {1}</p>
                '''.format(request.args, request.values)

if __name__ == '__main__':
    app.run()