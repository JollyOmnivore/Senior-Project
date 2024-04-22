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
#   0.5JSON is ready, just needs to be implemented.
#   1. Fully implement Create Vote.
#       - Generate p q values and do math accordingly
#       - Fill database accordingly
#       - Disallow users from voting when no vote active
#       - Implement timer section of create vote
#           + Time is already imported
#       - Make sure users can access vote results after.
#   2. Fully implement voting
#       - Make sure all votes arive in time.
#       - Simulate tests (steal old Joe script?)


from flask import *
from flask_sqlalchemy import *
from flask_login import *
from encryption import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db = SQLAlchemy(app)

currentCoprimeList = []


def clearCoprimeList():
    if currentCoprimeList:
        currentCoprimeList.clear()


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


def printVote(currentVote, valList):
    print(currentVote.question)
    print(currentVote.option1)
    print(currentVote.option2)
    print(currentVote.option3)
    print(currentVote.option4)
    print("n=", currentVote.n, "\n",
          "lam=", currentVote.lam, "\n",
          "mu=", currentVote.mu)
    print("isActive=", currentVote.isActive)
    print(currentVote.option1Total)
    print(currentVote.option2Total)
    print(currentVote.option3Total)
    print(currentVote.option4Total)
    print("coprime list len=", len(valList))
    #print("coprime list: ")
    #for val in valList:
    #    print(val)


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
        return render_template('create.html')
    elif request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        if not User.query.filter_by(username=username).all():
            user = User()
            user.username = username
            user.password = password
            user.name = name
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

        return render_template('currentVote.html')


@app.route('/createVote', methods=['GET', 'POST'])
@login_required
def createVote():
    if request.method == 'GET':
        if current_user.username == "Admin":
            # note to self: add a thing here to warn that creating a vote
            #will delete any vote in progress.
            return render_template('createVote.html')
        else:
            return redirect('/')
    elif request.method == 'POST':
        #add code to delete the last "CurrentVote"
        #for now we will always wipe the active vote, there will
        #only be one active vote at a time. for now, It's what we
        #can do for the meeting tommorow.

        #prepare by initiallizing all vote values
        #if CurrentVote exsists, clear table and coprime list
        deleteVote = CurrentVote.query.filter_by(id=1).first()
        if deleteVote:
            db.session.delete(deleteVote)
            db.session.commit()
            clearCoprimeList()

        #create vote and populate values
        tempVote = CurrentVote()
        tempVote.question = request.form['question']
        tempVote.option1 = request.form['option1']
        tempVote.option2 = request.form['option2']
        tempVote.option3 = request.form['option3']
        tempVote.option4 = request.form['option4']
        tempVote.n, tempVote.lam, tempVote.mu, currentCoprimeList = createVals()
        tempVote.isActive = True
        tempVote.option1Total = 0
        tempVote.option2Total = 0
        tempVote.option3Total = 0
        tempVote.option4Total = 0

        #commit to db
        db.session.add(tempVote)
        db.session.commit()

        # debug!!! Make sure the vote creates correct!
        debugVote = CurrentVote.query.filter_by(id=1).first()
        printVote(debugVote, currentCoprimeList)

        return redirect('/currentVote')


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'GET':
        return render_template('update.html')
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
    return render_template('errorPage.html', err=err)


if __name__ == '__main__':
    random.seed(time.time_ns())
    testingIndex = int(random.randint(0, len(primesListBig)))
    print("debugValue: ", testingIndex)
    app.run(debug=True)
