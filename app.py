from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=['GET'])
def login():
    return render_template("login.html")

@app.route("/register", methods=['GET'])
def register():
    return render_template("register.html")

@app.route("/admin", methods=['GET'])
def admin():
    return render_template("admin.html")

@app.route("/kullanici_crud", methods=['GET'])
def kullanici_crud():
    return render_template("kullanici_crud.html")

@app.route("/kitap_crud", methods=['GET'])
def kitap_crud():
    return render_template("kitap_crud.html")

@app.route("/kategori_crud", methods=['GET'])
def kategori_crud():
    return render_template("kategori_crud.html")

@app.route("/yayinevi_crud", methods=['GET'])
def yayinevi_crud():
    return render_template("yayinevi_crud.html")

@app.route("/yazar_crud", methods=['GET'])
def yazar_crud():
    return render_template("yazar_crud.html")

@app.route("/yorum_crud", methods=['GET'])
def yorum_crud():
    return render_template("yorum_crud.html")




if __name__ == "__main__":
    app.run(debug = True)