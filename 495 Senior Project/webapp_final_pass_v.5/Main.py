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

# Muskat Notes:
# +make sure no vote birthdays (check r and vote)
# +needs product on buletin
# +mod out products for the product
# +MAKE SURE TALLY SHOWS FOR USERS (with product)
# +Log the encrypted data for the user (FOR THE CURRENT VOTE)

from flask import *
from flask_sqlalchemy import *
from flask_login import *
from encryption import *
from sqlalchemy import desc
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    lastVote = db.Column(db.Integer)


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
    numVoters = db.Column(db.Integer)
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
    abstainTotal = db.Column(db.Integer())
    tally = db.Column(db.String(240))


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
    print(currentVote.tally)
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
    active = CurrentVote.query.order_by(desc(CurrentVote.id)).first()
    #active = CurrentVote.query.first()
    if active:
        if active.isActive and len(currentCoprimeList) < 1:
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
            user.lastVote = 0
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
        latestVote = CurrentVote.query.order_by(desc(CurrentVote.id)).first()
        if not latestVote:
            print("err, no vote? Something's wrong...")
            return redirect('/')

        #Now Actual Get cases
        else:
            #CASE 1:If vote is active, query votes to see if current_user has voted
            voteData = Votes.query.all()
            if latestVote.isActive:
                # if user vote not found, send to vote page
                if not Votes.query.filter_by(name=session['name']).first():
                    return render_template('vote.html', op1=latestVote.option1,
                                           op2=latestVote.option2,
                                           op3=latestVote.option3,
                                           op4=latestVote.option4,
                                           quest=latestVote.question)
                #CASE 2:else user voted, send to votechart with all votes data
                else:
                    return render_template('voteChart.html', voteData=voteData)

            #CASE 3:If vote is not active, send user to graph page with data
            else:
                #will leave this for now as graphing it will require a graphing tool and
                # sending said graph through template/alternative. Problem for later.
                return render_template('voteResults.html', latestVote=latestVote, voteData=voteData)
    #Post request handling
    elif request.method == 'POST':
        #Two cases:

        #regular:
        # Expected vals:
        # 'chosenValue'

        #matchstick:
        # Expected vals:
        # 'chosenValue'
        # 'encryptVal'


        #for now we will encrypt the vote here. it's not secure, but for now we just need it to work
        #we should try and move encryption to JS on the clientside so we can just send the vote
        voteVal = request.form['chosenValue']

        #check to make sure val picked, if not return
        if voteVal == '':
            return redirect("/currentVote")

        print("recieved vote:", voteVal)

        #query table for latest vote
        latestVote = CurrentVote.query.order_by(desc(CurrentVote.id)).first()

        #repopulate values using coprime list calculation.
        # note: This could be optimized by using the (mentioned below) system of threads or some
        # kind of beautiful server global var. Flask is a gift and a curse.
        if len(currentCoprimeList) <= 0:
            refreshCoprimeList(latestVote.n, latestVote.p, latestVote.q)

        # encrypt vote
        #note: This is where the fabled R check would happen if it were possible.
        # Implementation of this would require either A) some clever flask thread/worker
        # handling, B) creation of new sql tables on the fly (illegal, class 2 felony)/storage
        # of lists in an array IN sql (varsize limit overflow errors),
        # or C) a system of sockets and broadcasting using JS. This is what killed
        # my CS412 Blackjack project. Threads are a nightmare and the only other feasible way
        # to do this would be to seed all possible R choices before the vote using a static val,
        # which would once again fall to either a global dynamic server variable (that like
        # currentCoprimeList, would be lost upon thread crash/reset, which happens inevitably
        # and requires the above if statement to refill the current coprime list, which we must
        # do every time. This is the case for both local and hosted. Please for the love of god,
        # if you wish to venture into this cave, COME PREPARED. This is a dark road to walk down.

        #if this a matchstick, its already encrypted and ready, it just needs to be submitted
        #retrieve matchstick value 'encryptVal'
        newvote = Votes()
        newvote.name = session['name']
        encVote = request.form['encryptVal']
        #if value present, send vote as is with name, else encrypt
        if encVote:
            print("Matchstick Submit")
            newvote.vote = int(encVote)
        else:
            print("Regular Submit")
            encVote = encryptVote(random.choice(currentCoprimeList), int(voteVal), latestVote.n)

        print("name:", session['name'])
        print("vote:", voteVal)
        print("encrypted vote:", encVote)
        #create and populate vote object

        newvote.vote = encVote

        #VOTE CHECKS!

        #Collision Check
        # query active votes table for all
        allVotes = Votes.query.all()

        # Itterate by vote, check to make sure vote val doesnt match.
        #note: see note above as to why the R version doesn't exsist.
        for vote in allVotes:
            # if vote present, send back to the vote page
            if vote.vote == newvote.vote:
                # itterates through and checks, sending user back to page if fail
                # redir back to page should send user to vote.html based on lack of vote.
                # add error message at later time
                return redirect('/currentVote')
        # Else, vote valid

        # Pass Check: save vote to table
        #note: Yeah, I'm doing this before I check max voters. Yeah, im a bad influence >:)
        # Because im doing this, im also incrementing voteInc AFTER I add, for sake of o^3
        # This could be done better by appending the vote into allVotes directly, and the
        # closest thing I've found in terms of help is a stack overflow from 7 years ago
        # with exactly 0 replies. This is gross but THE way to do it. Love that :)
        db.session.add(newvote)
        db.session.commit()

        #refresh allVotes to include new vote before (possibly) running endvote
        allVotes = Votes.query.all()

        #Max Votes Check

        #if the set number of voters = counted voters, safely end vote
        # + set vote active to 0
        # + calculate vote tally
        # + populate values in latestVote
        # + print debug for votes
        # + return template 'voteResults' with latestVote
        #note: This can and SHOULD be done more safely when live updating is added. This
        # will probably require sockets and some handling on the html side as well.

        # vote vals at time of run
        # numVoters/lam/mu/n/p/q = static val (set at create)
        # isActive = 1
        # opt1-4 = 0
        # tally = 0

        #active query vars
        # latestVote = most recent vote, always active here
        # allVotes = all active votes (name, vote)
        if latestVote.numVoters == len(allVotes):
            # set active vote 0
            latestVote.isActive = 0

            # calculate vote tally
            #stolen from endVote, with adjustments made.
            checksum = 0
            tallyProduct = 1
            for vote in allVotes:
                tallyProduct = tallyProduct * vote.vote
                singleDec = decryptTotal(vote.vote, latestVote.lam, latestVote.n, latestVote.mu)
                checksum += singleDec
                db.session.delete(vote)
            #calc and print tally
            voteTally = decryptTotal(tallyProduct,
                                     latestVote.lam,
                                     latestVote.n,
                                     latestVote.mu)
            print("tally:", tallyProduct)
            print("decrypt:", voteTally)
            print("checkval", checksum)

            #populate values in latestVote
            a, b, c, d, abstains = tallyUp(voteTally, latestVote.numVoters)
            latestVote.option1Total = a
            latestVote.option2Total = b
            latestVote.option3Total = c
            latestVote.option4Total = d
            latestVote.tally = str(tallyProduct % (latestVote.n ** 2))
            latestVote.abstainTotal = abstains
            db.session.commit()
            # More debugging:
            print("Option 1:", latestVote.option1Total)
            print("Option 2:", latestVote.option2Total)
            print("Option 3:", latestVote.option3Total)
            print("Option 4:", latestVote.option4Total)
            print("Abstains:", latestVote.abstainTotal)

            #return render template with voteResults with data, exiting function.
            # following this,
            return render_template('voteResults.html', latestVote=latestVote)

        #Stress Tester
        # This will create a handful of votes based on the static number of voters
        # and is untested with the live web version in python anywhere. Either adapt
        # to work on webserver or just use locally.
        #note: currentCoprimeList will be populated here if needed
        #'''
        for i in range(0, latestVote.numVoters - 1):
            samples = [0, 1, 100, 10000, 1000000] # add 0 to options to sim abstain
            tempyVote = Votes()
            tempyVote.name = str(i + 1) + "Joe"
            tempyVote.vote = encryptVote(random.choice(currentCoprimeList), random.choice(samples), latestVote.n)
            print("name:", tempyVote.name)
            print("encrypted vote:", tempyVote.vote)
            db.session.add(tempyVote)
        #'''
        #end stress tester
        #Save last vote to user for profile page.
        currUser = User.query.filter_by(username=current_user.username).first()
        currUser.lastVote = encVote
        db.session.commit()
        return redirect('/currentVote')

@app.route('/matchstick', methods=['GET', 'POST'])
@login_required
def matchstick():
    #Input: Post req from form, not a submit tho!
    #output: send back to form with prepopulated values
    # hopefully, the hardest part should be getting the form to cooperate here.

    #If GET (IDK how but just in case)
    if request.method == 'GET':
        #send back to currentVote (if this ever activates someone is being a goblin)
        return redirect("/currentVote")

    #else run the encryption math.
    #prep encrypt vars

    #query table for latest vote
    latestVote = CurrentVote.query.order_by(desc(CurrentVote.id)).first()

    if len(currentCoprimeList) <= 0:
        refreshCoprimeList(latestVote.n, latestVote.p, latestVote.q)

    #grab form value like normal.
    voteVal = request.form['chosenValue']
    optionText = request.form['optionText']



    #if no val present, ie hit matchstick with no val, redirect back to page
    if voteVal == '':
        return redirect("/currentVote")


    print("!MATCHSTICK!")
    print("###DEBUG###")
    print("Len coprime list:", len(currentCoprimeList))
    print("recieved vote:", voteVal)
    print("optionText:", optionText)

    #no need for a new vote object since were just responding with a return to the
    #page with an int instead of a whole vote
    matchVote = encryptVote(random.choice(currentCoprimeList), int(voteVal), latestVote.n)
    print("match vote:", matchVote)

    #return to vote page with match vote.
    return render_template('vote.html', op1=latestVote.option1,
                           op2=latestVote.option2,
                           op3=latestVote.option3,
                           op4=latestVote.option4,
                           quest=latestVote.question,
                           match=matchVote,
                           optionText=optionText,
                           chosenValue=voteVal)

@app.route('/decrypt', methods=['GET', 'POST'])
@login_required
def decryptor():
    # If GET (IDK how but just in case)
    if request.method == 'GET':
        # send back to currentVote (if this ever activates someone is being a goblin)
        return redirect("/currentVote")





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
        #Clear any values exsistent in coprime list, theyre about to be made irrelevant
        clearCoprimeList()

        #create vote and populate values
        tempVote = CurrentVote()
        tempVote.question = request.form['question']
        tempVote.option1 = request.form['option1']
        tempVote.option2 = request.form['option2']
        tempVote.option3 = request.form['option3']
        tempVote.option4 = request.form['option4']
        tempVote.numVoters = request.form['num_voters']
        tempVote.n, tempVote.p, tempVote.q, tempVote.lam, tempVote.mu, currentCoprimeList = createVals()
        tempVote.isActive = True
        tempVote.option1Total = 0
        tempVote.option2Total = 0
        tempVote.option3Total = 0
        tempVote.option4Total = 0
        tempVote.abstainTotal = 0
        tempVote.voteInc = 0
        tempVote.tally = 0

        #commit to db
        db.session.add(tempVote)
        db.session.commit()

        # debug!!! Make sure the vote creates correct!
        debugVote = CurrentVote.query.order_by(desc(CurrentVote.id)).first()
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
            user = User.query.filter_by(password=password).all()
            user.password = newpassword
            db.session.commit()
            return redirect('/')
        else:
            return redirect('/update')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        #query for current user to load lastVote
        currUser = User.query.filter_by(username=current_user.username).first()
        if current_user.username == "Admin" and session['name'] == "Admin":
            # query all pastvotes in CurrentVote
            all_votes = CurrentVote.query.all()
            debug = 0
            for vote in all_votes:
                print(debug, ":", vote.question)
                debug += 1

            return render_template('profile.html', lastVote=currUser.lastVote, votes=all_votes)
        return render_template('profile.html', lastVote=currUser.lastVote)


@app.route('/endVote')
@login_required
def endVote():
    #make sure its "Admin"
    #if not, redir to home
    if current_user.username != "Admin" or session['name'] != "Admin":
        return redirect('/currentVote')
    #else check current vote
    else:
        latestVote = CurrentVote.query.order_by(desc(CurrentVote.id)).first()
        #check if already set to False, redir if so
        if not latestVote.isActive:
            return redirect('/currentVote')
        #if true, vote MUST BE ACTIVE AND ADMIN USER.
        #ending the vote:
        else:
            # set CurrentVote.isActive = False
            latestVote.isActive = False
            # this val is probably unneccesary, could
            # just init latestVote.tally = 1 in create maybe?
            tallyProduct = 1
            checksum = 0
            # calculate the tally
            # itterate through and actually calculate tally, then store in val
            # delete all votes from table
            allVotes = Votes.query.all()
            for vote in allVotes:
                tallyProduct = tallyProduct * vote.vote
                singleDec = decryptTotal(vote.vote, latestVote.lam, latestVote.n, latestVote.mu)
                checksum += singleDec
                db.session.delete(vote)
            # calc and print tally
            voteTally = decryptTotal(tallyProduct,
                                     latestVote.lam,
                                     latestVote.n,
                                     latestVote.mu)
            print("tally:", tallyProduct)
            print("decrypt:", voteTally)
            print("checkval", checksum)

            # populate values in latestVote
            a, b, c, d, abstains = tallyUp(voteTally, latestVote.numVoters)
            latestVote.option1Total = a
            latestVote.option2Total = b
            latestVote.option3Total = c
            latestVote.option4Total = d
            latestVote.tally = str(tallyProduct % (latestVote.n ** 2))
            latestVote.abstainTotal = abstains
            db.session.commit()
            #More debugging:
            print("Option 1:", latestVote.option1Total)
            print("Option 2:", latestVote.option2Total)
            print("Option 3:", latestVote.option3Total)
            print("Option 4:", latestVote.option4Total)
            print("Abstains:", latestVote.abstainTotal)

            #return template with data to render
            # currently: send the tally through the template, stacked decrypt val/checksum
            # later    : use acutal data and display visuals instead of just tally
            return render_template('voteResults.html', latestVote=latestVote)


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
    app.run()

