from flask import *
from flask_sqlalchemy import *
from flask_login import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db = SQLAlchemy(app)




class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(80))
    name = db.Column(db.String(30))




class Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    vote = db.Column(db.Integer())

class CurrentVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100))
    option1 = db.Column(db.String(100))
    option2 = db.Column(db.String(100))
    option3 = db.Column(db.String(100))
    option4 = db.Column(db.String(100))
    lam = db.Column(db.Integer())
    mu= db.Column(db.Integer())
    n = db.Column(db.Integer())
    isActive = db.Column(db.Boolean())
    option1Total = db.Column(db.Integer())
    option2Total = db.Column(db.Integer())
    option3Total = db.Column(db.Integer())
    option4Total = db.Column(db.Integer())




app.config['SECRET_KEY'] = 'alksdifa;lksdif;alksdifa;lksdifa;lksdfj'
login_manager = LoginManager(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(uid):
    user = User.query.filter_by(id=uid).first()
    return user



@app.route('/', methods=['GET', 'POST'])
def home():
    loggedin = current_user.is_authenticated
    if request.method == 'GET':
        return render_template('about.html',loggedin=loggedin)



#ported over needs to be compatiable with
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('Create.html')
    elif request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        if not User.query.filter_by(username=username).all():
            user = User(username=username, password=password, name=name)
            db.session.add(user)
            print("session add")
            db.session.commit()
            print("session commit")
            login_user(user)
            print("login")
            return redirect('/')
        else:
            return redirect('/create')



@app.route('/about', methods=['GET'])
def about():
    loggedin = current_user.is_authenticated
    user = current_user
    username = user.username
    if request.method == 'GET':
        return render_template('about.html',loggedin=loggedin)

@app.route('/currentVote', methods=['GET', 'POST'])
@login_required #uncomment to make login required

def currentVote():
    loggedin = current_user.is_authenticated
    user = current_user
    username = user.username
    if request.method == 'GET':
        return render_template('Current vote.html',loggedin=loggedin)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None and password == user.password:
            print("try to log in")
            login_user(user)
            print("logged in apparently")
            return redirect('/')
        else:
            return redirect('/login')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        loggedin = current_user.is_authenticated
        user = current_user
        username = user.username
        return render_template('profile.html', username=username, loggedin=loggedin)



@app.errorhandler(404)
@app.errorhandler(401)
def functionToRun(err):
    return render_template('errorpage.html', users=User.query.all(), err=err)

@app. route ('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/update',methods = ['GET','POST'])
@login_required
def update():

    if request.method == 'GET':
        loggedin = current_user.is_authenticated
        return render_template('update.html', users=User.query.all(),loggedin=loggedin)
    elif request.method == 'POST':
        password = request.form['password']
        newpassword = request.form['newpassword']
        user = current_user
        if user.password == password:
            #user = User.query.filter_by(password=password).all()
            user.password = newpassword
            db.session.commit()
            return redirect('/')
        else:
            return redirect('/update')



if __name__ == '__main__':
    app.run(debug=True)



