## This is my test page on Stone Campus!
>This is only a simple sample page, obviously not what I've been doing for three months' worth of time.
>I've been working on a li'l project testing the functionality of Flask and Jinja2 and I hope you like it!

``` python
@app.route('/')
def index():
    uid = session.get('user_id')
    with pdms.connect_db() as conn:
        data = pdms.get_user(conn, uid)
        if uid:
            name = data[1]
        else:
            name = '[]'
    return render_template('index.html', user=uid, name=name)
```

``` python
def user_login(conn, email, password):
    c = conn.cursor()
    sql = '''
        SELECT id, name, password, email FROM users
        WHERE email = ? AND password = ?
    '''
    c.execute(sql, (email, password))
    user = c.fetchone()
    return user
```

### Abstract
* Shop
    * Add product
    * Edit product
    * Delete product
* User
    * Sign Up
    * Edit User
    * Delete User
    * Login

### Developers
It's obvious that I did most of the works in this project, but I also want to credit my teachers at [Stone Campus](https://www.stonecampus.net) that always answer my questions patiently and my parents who give me lots of time and mental support while I'm working on this.

### Time
This project will last for the entire year (until June 2019). I've been updating this regularly around once per week or ten days. Each time there will be more functions or decorations added. There might be bugs sometimes but I will try to fix them asap.

### Host
This project *will* be hosted on [Python Anywhere](https://www.pythonanywhere.com). It is a service that enables you to host web applications made with python and there are many more add-ons like HTTPS support and everybody can view it online (not locally hosted).

So far, I also use Cloud 9 as the IDE for this project. Please go to [This site](http://shop-xscorp-xscorpio2232.c9users.io:8080/). This is a emulated version of what the site on PythonAnywhere will look like, but issues has been going on. Anyways, **please don't put strange things there.**

### Reasons
The main reason why I like to do this is because I really like to develop web applications. It is also a good way to burn your excess time if you have nothing else to do. Besides, I really like Team Liquid in Clash Royale! [#LetsGoLiquid](https://www.teamliquidpro.com)

### Stuffs
>Check it out here! [Shop_xScorp](http://shop-xscorp-xscorpio2232.c9users.io:8080)

