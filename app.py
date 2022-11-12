from database import *
import flask
from flask import render_template, request, make_response, redirect
from methods import *

app = flask.Flask(__name__)

@app.route('/', methods=['GET','POST'])
def login_tem():
    if request.method == 'POST':
        net_id = request.form['netId']
        password = request.form['password']
        exist = login(net_id, password)

        if exist:
            view = render_template('login.html', errorMsg = "")
            response = make_response(view)
            response.set_cookie('info', f"{net_id}, {password}", expireDate(1))
            return market_buy()
        else:
            return render_template('login.html', errorMsg=f"The user ,{net_id.capitalize()}, does not exist!!")
    
    return render_template("login.html", errorMsg = "")


@app.route('/register', methods=['GET','POST'])
def register_tem():  
    if request.method == 'POST':
        netId = request.form['net_id']
        password = request.form['password']
        first_name = request.form['first_name']
        confPassword = request.form['conf_password']
        error = ""

        if confPassword != password:
            error = "The password must match!!"
        elif first_name.isalpha():
            error = "All the characters must be an alphabet!!"
        elif netId[0].isdigit():
            error = "The netId must start with alphabet. ie (ab1234)!!"

        is_registered = register(first_name, netId, password)

        if is_registered:
            # return redirect('./')
            return login_tem()
        else:
            return render_template('register.html', errorMsg=error)
    
    return render_template("register.html", errorMsg="")

@app.route('/my_posts', methods=['GET', 'POST'])
def myPosts():
    info = request.cookies.get('info', None)
    info = info.split(',')
    username = info[0] # netId
    password = info[1]

    if login(username, password):
        posts = my_posts(username, password)
        return render_template("posts/my_posts.html", posts=posts)
    else:
        return login_tem()

#  =================================================================
INIT()

@app.route('/market/buy')
def market_buy():
    buy_posts = getBuyPosts()
    info = request.cookies.get('info', None)
    username = info[0]
    password = info[1]
    if login(username, password):
        return render_template("posts/browse_buy.html", buy_posts=buy_posts)
    else:
        return login_tem()

@app.route('/market/sell')
def market_sell():
    sell_posts = getSellPosts()
    info = request.cookies.get('info', None)
    username = info[0]
    password = info[1]
    if login(username, password):
        return render_template("posts/browse_buy.html", sell_posts=sell_posts)
    else:
        return login_tem()

@app.route('/create', methods=['GET'])
def create_post():
    info = request.cookies.get('info', None)
    username = info[0]
    password = info[1]
    if login(username, password):
        return render_template("posts/create_post.html")
    else:
        return login_tem()

@app.route('/create/sell', methods=['GET'])
def create_sell():
    info = request.cookies.get('info', None)
    username = info[0]
    password = info[1]
    if login(username, password):
        return render_template("posts/create_sell.html")
    else:
        return login_tem()


@app.route('/create/sell', methods=['GET', 'POST'])
def create_sell_action():
    if request.method == "POST":
        info = request.cookies.get('info', None)
        username = info[0]
        password = info[1]
        if login(username, password):
            user_id = "1234"
            amount = request.form.get("amount")
            rate = request.form.get("rate")
            create_sell_post(user_id, amount, rate)
            return render_template("posts/create_sell.html")
        else:
            return login_tem()

    return create_sell()

@app.route('/create/buy', methods=['GET'])
def create_buy():
    return render_template("posts/create_buy.html")


@app.route('/create/buy', methods=['GET', 'POST'])
def create_buy_action():
    if request.method == "POST":
        user_id = "1234" #todo
        amount = request.form.get("amount")
        rate = request.form.get("rate")
        create_buy_post(user_id, amount, rate)
        return render_template("posts/create_buy.html")
    return render_template("posts/create_sell.html")

app.run(debug=True)

