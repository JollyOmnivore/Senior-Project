#Willow Progress:
#Done:
#   +Fix session issues using current_user in place of template shenanigans
#       Flask Login : current_user
#               <DEFAULT> login_user(UserSQLObject)
#                         current_user.is_authenticated
#                         current_user.username
#               <END>     logout_user()
#       Flask       : session[stringkey] : Tracks through session, can get in html/jinja
#               <DEFAULT> session['username'] = <string>
#               <DEFAULT> session['loggedin'] = <bool>
#                         session['string'] = <most data types>
#               <END>     session.pop('stringkey', None) #do this for all of them you create
#   +Clean up repeat code around server and set up for encryption implementation.
#   +Prepare to combine files by setting up encryption.py with the functions Joe made.
#       -These needed modifications to be standalone
#       -Will need future attention for security
#       -Implement JSON for big prime to help find root of slowdowns
#
#   To-Do:
#   Ad-infinium: Fix math errors/security flaws
#   1.Fix(?) Create account? Still getting warnings but it still runs so idk.
#   2.Fully implement Create Vote.
#       - Generate p q values and do math accordingly
#       - Fill database accordingly
#       - Disallow users from voting when no vote active
#       - Implement timer section of create vote
#       - Make sure users can access vote results after.
#   3.Fully implement voting
#       - Make sure all votes arive in time.
#       - Simulate tests (steal old Joe script?)
#       -
from flask import *
from flask_sqlalchemy import *
from flask_login import *
from encryption import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
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
    mu = db.Column(db.Integer())
    n = db.Column(db.Integer())
    isActive = db.Column(db.Boolean())
    option1Total = db.Column(db.Integer())
    option2Total = db.Column(db.Integer())
    option3Total = db.Column(db.Integer())
    option4Total = db.Column(db.Integer())


app.secret_key = 'alksdifa;lksdif;alksdifa;lksdifa;lksdfj'
login_manager = LoginManager(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(uid):
    user = User.query.filter_by(id=uid).first()
    return user


@app.route('/', methods=['GET', 'POST'])
@app.route('/about', methods=['GET', 'POST'])
def home():
    loggedin = current_user.is_authenticated
    print(loggedin)  # add if case is false then don't get username
    return render_template('about.html')


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
            session['username'] = user.username
            session['loggedin'] = True
            print("logged in apparently")
            return redirect('/')
        else:
            return redirect('/login')


#ported over by carter, needs to be made compadible (maybe?)
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
            session['username'] = user.username
            session['loggedin'] = True
            print("login")
            return redirect('/')
        else:
            return redirect('/create')


@app.route('/currentVote', methods=['GET', 'POST'])
@login_required  # uncomment to make login required
def currentVote():
    if request.method == 'GET':
        return render_template('Current vote.html')


@app.route('/createVote', methods=['GET', 'POST'])
@login_required
def createVote():
    if request.method == 'GET':
        if current_user.username == "Admin":
            return render_template('CreateVote.html')
        else:
            return redirect('/')
    elif request.method == 'POST':
        #add code to delete the last "CurrentVote"
        question = request.form['question']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        #add code to generate lam, mu , n
        print(question)
        print(option1)
        print(option2)
        print(option3)
        print(option4)
        return redirect('/currentVote')


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'GET':
        loggedin = current_user.is_authenticated
        return render_template('update.html', users=User.query.all(), loggedin=loggedin)
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


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        return render_template('profile.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.errorhandler(404)
@app.errorhandler(401)
def functionToRun(err):
    # I don't know why we have a user query here but whatever. users aren't refenced in navbar or errpg?
    return render_template('errorpage.html', users=User.query.all(), err=err)


if __name__ == '__main__':
    app.run(debug=True)
