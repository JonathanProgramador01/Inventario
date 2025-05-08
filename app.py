from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'bgnh65uyhjngdfg45y6ujmghde'  # Change this to a real secret key

@app.route('/')
def login():
    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Here you would typically save the user to a database
        flash("Registration successful!", "success")
        return redirect(url_for("login"))
    return render_template("register.html")









if __name__ == '__main__':
    app.run(debug=True, port=5001)