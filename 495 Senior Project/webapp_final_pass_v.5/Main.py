#Willow Progress:
#Done:
#   +Fix session issues using current_user in place of template shenanigans
#       Flask Login : current_user       : Persistent thru disconects, can get in html/jinja
#               <DEFAULT> login_user(UserSQLObject)
#                         current_user.is_authenticated
#                         current_user.username
#               <END>     logout_user()
#       Flask       : session[stringkey] : Not persistent thru disc, can get in html/jinja
#               <DEFAULT> session['username'] = <string>
#               <DEFAULT> session['loggedin'] = <bool>
#                         session['string'] = <most data types>
#               <using>   session['name'] = user.name
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
#   1. Live user vote updating on /currentVote while vote active
#   2. Admin view vote history
#   3. Users view vote history
import random

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


def refreshCoprimeList(n, p, q):
    global currentCoprimeList
    currentCoprimeList = randNumList(n, p, q)


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
    #added p and q to regen coprimes when coprime list shits the bed
    p = db.Column(db.Integer())
    q = db.Column(db.Integer())
    isActive = db.Column(db.Boolean())
    option1Total = db.Column(db.Integer())
    option2Total = db.Column(db.Integer())
    option3Total = db.Column(db.Integer())
    option4Total = db.Column(db.Integer())


class PastVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100))
    option1 = db.Column(db.String(100))
    option2 = db.Column(db.String(100))
    option3 = db.Column(db.String(100))
    option4 = db.Column(db.String(100))

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
          "p=", currentVote.p, "\n",
          "q=", currentVote.q, "\n",
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
    print("coprime list len:", len(currentCoprimeList))
    #session refresher: include here if someone logged in is comming back
    #since they always go home first, we can run this when they get to home and
    #recache their session data so if they go to current vote they'll have ['name']
    if current_user.is_authenticated:
        tempUser = User.query.filter_by(username=current_user.username).first()
        session['name'] = tempUser.name
    #repopulate coprimes if active vote
    active = CurrentVote.query.filter_by(id=1).first()
    if active:
        if active.isActive:
            refreshCoprimeList(active.n, active.p, active.q)
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
            session['name'] = user.name
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
            session['name'] = user.name
            print("login")
            return redirect('/')
        else:
            return redirect('/create')


@app.route('/currentVote', methods=['GET', 'POST'])
@login_required
def currentVote():
    print("coprime list len:", len(currentCoprimeList))
    #GET CASES:
    # 1. User who hasn't voted/active vote open
    #   + Send to vote
    # 2. User who has voted/active vote open
    #   + Send to votes chart, display contents of votes table (live/till close)
    # 3. User who has voted/active vote closed + User sent from prev +
    #   + Send to graph page. (MAKE SURE ACTIVE VOTE CLOSED BEFORE DECRYPT)

    #Just in case, secret edge case if no vote exsists to display. Should never
    #be the case though....
    if request.method == 'GET':
        latestVote = CurrentVote.query.filter_by(id=1).first()
        if not latestVote:
            print("err, no vote? Something's wrong...")
            return redirect('/')

        #Now Actual Get cases
        else:
            #If vote is active, query votes to see if current_user has voted
            if latestVote.isActive:
                # if user vote not found, send to vote page
                if not Votes.query.filter_by(name=session['name']).first():
                    return render_template('vote.html', op1=latestVote.option1,
                                           op2=latestVote.option2,
                                           op3=latestVote.option3,
                                           op4=latestVote.option4,
                                           quest=latestVote.question)
                #else user voted, send to votechart with all votes data
                else:
                    voteData = Votes.query.all()
                    return render_template('voteChart.html', voteData=voteData)

            #If vote is not active, send user to graph page with data
            else:
                #will leave this for now as graphing it will require a graphing tool and
                # sending said graph through template/alternative. Problem for later.
                return render_template('voteResults.html', opt1=latestVote.option1Total,
                                       opt2=latestVote.option2Total,
                                       opt3=latestVote.option3Total,
                                       opt4=latestVote.option4Total)
    #Post request handling
    elif request.method == 'POST':
        #for now we will encrypt the vote here. it's not secure, but for now we just need it to work
        #we should try and move encryption to JS on the clientside so we can just send the vote
        voteVal = request.form['chosenValue']
        print("recieved vote:", voteVal)
        #debug: check coprime list to see if any values exist. (wtf)
        #encrypt vote
        latestVote = CurrentVote.query.filter_by(id=1).first()
        if len(currentCoprimeList) <= 0:
            refreshCoprimeList(latestVote.n, latestVote.p, latestVote.q)
        encVote = encryptVote(random.choice(currentCoprimeList), int(voteVal), latestVote.n)
        print("name:", session['name'])
        print("encrypted vote:", encVote)
        #create and populate vote object
        newvote = Votes()
        newvote.name = session['name']
        newvote.vote = encVote
        #save to table
        db.session.add(newvote)
        #stress tester
        for i in range(0, 5):
            samples = [1, 100, 10000, 1000000]  #10^6 currently breaks the big decrypt.
            tempyVote = Votes()
            tempyVote.name = str(i) + "Joe"
            tempyVote.vote = encryptVote(random.choice(currentCoprimeList), random.choice(samples), latestVote.n)
            print("name:", tempyVote.name)
            print("encrypted vote:", tempyVote.vote)
            db.session.add(tempyVote)
        #end stress tester
        db.session.commit()
        return redirect('/currentVote')


@app.route('/createVote', methods=['GET', 'POST'])
@login_required
def createVote():
    global currentCoprimeList
    print("coprime list len:", len(currentCoprimeList))
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
        tempVote.n, tempVote.p, tempVote.q, tempVote.lam, tempVote.mu, currentCoprimeList = createVals()
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
        if current_user.username != "Admin" or session['name'] != "Admin":
            all_votes = PastVote.query.all()
            for vote in all_votes:
                print("Question:", vote.question)
            return render_template('profile.html', votes=all_votes)
        return render_template('profile.html')


@app.route('/endVote')
@login_required
def endVote():
    #make sure its "Admin"
    #if not, redir to home
    if current_user.username != "Admin" or session['name'] != "Admin":
        return redirect('/')
    #else check current vote
    else:
        latestVote = CurrentVote.query.filter_by(id=1).first()
        #check if already set to False, redir if so
        if not latestVote.isActive:
            return redirect('/')
        #if true, vote MUST BE ACTIVE AND ADMIN USER.
        #ending the vote:
        else:
            # set CurrentVote.isActive = False
            latestVote.isActive = False
            tallyProduct = 1
            checksum = 0
            # calculate the tally
            # itterate through and actually calculate tally, then store in val
            # delete all votes from table
            allVotes = Votes.query.all()
            for vote in allVotes:
                #print("Tally Prod:", tallyProduct, " * ", vote.vote)
                tallyProduct = tallyProduct * vote.vote
                print("New Tally:", tallyProduct)
                singleDec = decryptTotal(vote.vote, latestVote.lam, latestVote.n, latestVote.mu)
                print("checkval:", singleDec)
                checksum += decryptTotal(vote.vote, latestVote.lam, latestVote.n, latestVote.mu)
                print("checksum:", checksum)
                db.session.delete(vote)
            #calc and print tally
            voteTally = decryptTotal(tallyProduct,
                                     latestVote.lam,
                                     latestVote.n,
                                     latestVote.mu)
            print("tally:", tallyProduct)
            print("decrypt:", checksum)

            saveVote = PastVote()
            saveVote.question = latestVote.question
            saveVote.option1 = latestVote.option1
            saveVote.option2 = latestVote.option2
            saveVote.option3 = latestVote.option3
            saveVote.option4 = latestVote.option4

            splInt = str(checksum)
            a = splInt[0:1]
            b = splInt[2:3]
            c = splInt[4:5]
            d = splInt[6:]
            saveVote.option1Total = a
            saveVote.option2Total = b
            saveVote.option3Total = c
            saveVote.option4Total = d
            db.session.add(saveVote)
            db.session.commit()
            #return template with data to render
            # currently: send the tally through the template, stacked decrypt val/checksum
            # later    : use acutal data and display visuals instead of just tally
            return render_template('voteResults.html', tally=checksum)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('name', None)
    return redirect('/')


@app.errorhandler(404)
@app.errorhandler(401)
def functionToRun(err):
    return render_template('errorPage.html', err=err)


if __name__ == '__main__':
    random.seed(time.time_ns())
    testingIndex = int(random.randint(0, len(primesListBig)))
    print("debugValue: ", testingIndex)
    app.run()
