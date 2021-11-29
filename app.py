from re import A
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import flask
import random
import psycopg2
import hashlib

app = Flask(__name__)

def get_sifre(username):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        postgres_read = "SELECT \"Kullanici_Sifresi\" FROM \"KULLANICI\" WHERE \"Kullanici_Adi\" = %s" 
        cursor.execute(postgres_read,(username,))
        sifre = cursor.fetchall()
        return sifre[0][0]

    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def insert_user(name, surname, username, password, email, address):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        postgres_get = "SELECT * FROM \"KULLANICI\" WHERE \"Kullanici_Adi\" = %s"
        cursor.execute(postgres_get,(username,))
        count = cursor.rowcount
        if(count>0):
            return 1
        postgres_insert = "INSERT INTO \"KULLANICI\" VALUES (%s,%s,%s,%s,%s,%s)" 
        cursor.execute(postgres_insert,(username,password,email,name,surname,address))
        postgres_insert = "INSERT INTO \"SEPET\" VALUES (%s,0,0)" 
        cursor.execute(postgres_insert,(username,))
        postgres_insert = "INSERT INTO \"FAVORILER\" VALUES (%s,0)" 
        cursor.execute(postgres_insert,(username,))
        connection.commit()
        print("Inserted user successfully")
        return 0
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def get_sepet_kitaplar(username):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        postgres_command = "SELECT \"KITAP\".\"Kitap_Id\", \"Kitap_Ismi\", \"Fiyat\", \"Fotograf_Adi\" FROM \"KITAP\",\"SICERIR\" WHERE \"Kullanici_Adi\" = %s AND \"KITAP\".\"Kitap_Id\" = \"SICERIR\".\"Kitap_Id\"" 
        cursor.execute(postgres_command,(username,))
        sepet_kitaplar = cursor.fetchall()
        postgres_command = "SELECT \"SKitap_Adet\" FROM \"SEPET\" where \"Kullanici_Adi\" = %s" 
        cursor.execute(postgres_command,(username,))
        count = cursor.fetchall()[0][0]
        print(count)
        sepet_bilgiler =[]
        sepet_bilgiler.append(sepet_kitaplar)
        sepet_bilgiler.append(count)
        print(sepet_bilgiler)
        return sepet_bilgiler
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def clear_sepet(username):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        postgres_command = "Delete from \"SICERIR\" where \"Kullanici_Adi\" = %s" 
        cursor.execute(postgres_command,(username,))
        postgres_command = "Update \"SEPET\" set \"SKitap_Adet\" = 0 where \"Kullanici_Adi\" = %s" 
        cursor.execute(postgres_command,(username,))
        connection.commit()
        print("Clear cart successfully")
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def get_favori_kitaplar(username):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        postgres_command = "SELECT \"KITAP\".\"Kitap_Id\", \"Kitap_Ismi\", \"Fiyat\", \"Fotograf_Adi\" FROM \"KITAP\",\"FICERIR\" WHERE \"Kullanici_Adi\" = %s AND \"KITAP\".\"Kitap_Id\" = \"FICERIR\".\"Kitap_Id\"" 
        cursor.execute(postgres_command,(username,))
        favori_kitaplar = cursor.fetchall()
        postgres_command = "SELECT \"FKitap_Adet\" FROM \"FAVORILER\" where \"Kullanici_Adi\" = %s" 
        cursor.execute(postgres_command,(username,))
        count = cursor.fetchall()[0][0]
        favori_bilgiler =[]
        favori_bilgiler.append(favori_kitaplar)
        favori_bilgiler.append(count)
        return favori_bilgiler
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def clear_favori(username):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        postgres_command = "Delete from \"FICERIR\" where \"Kullanici_Adi\" = %s" 
        cursor.execute(postgres_command,(username,))
        postgres_command = "Update \"FAVORILER\" set \"FKitap_Adet\" = 0 where \"Kullanici_Adi\" = %s" 
        cursor.execute(postgres_command,(username,))
        connection.commit()
        print("Clear favorites successfully")
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def add_favorites_to_cart(username):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        postgres_command = "INSERT INTO \"SICERIR\" (\"Kullanici_Adi\",\"Kitap_Id\") SELECT \"Kullanici_Adi\",\"Kitap_Id\" FROM \"FICERIR\"" 
        cursor.execute(postgres_command,(username,))
        count_fav = get_favori_kitaplar(username)[1]
        
        print(count_fav)
        postgres_command = """SELECT sum("Fiyat") FROM "FICERIR", "KITAP" WHERE "KITAP"."Kitap_Id" = "FICERIR"."Kitap_Id" and "Kullanici_Adi" = %s """
        cursor.execute(postgres_command,(username,))

        price_sum = cursor.fetchall()
        print(price_sum)
        postgres_command = "DELETE FROM \"FICERIR\"" 
        cursor.execute(postgres_command)
        postgres_command = "UPDATE \"FAVORILER\" set \"FKitap_Adet\" = 0 where \"Kullanici_Adi\" = %s" 
        cursor.execute(postgres_command,(username,))
        postgres_command = "UPDATE \"SEPET\" set \"SKitap_Adet\" = \"SKitap_Adet\" + %s where \"Kullanici_Adi\" = %s" 
        cursor.execute(postgres_command,(count_fav,username))

        

        postgres_command = """SELECT * FROM "SEPET" WHERE "Kullanici_Adi" = %s """
        cursor.execute(postgres_command,(username,))
        print(cursor.fetchall())
       
        postgres_command = "UPDATE \"SEPET\" set \"Sepet_Tutar\" = \"Sepet_Tutar\" + %s where \"Kullanici_Adi\" = %s" 
        cursor.execute(postgres_command,(price_sum[0][0],username))

        connection.commit()
        print("Add favorites to cart successfully")
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def add_favorite_to_cart(username, id):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        postgres_command = "INSERT INTO \"SICERIR\" (\"Kullanici_Adi\",\"Kitap_Id\") SELECT \"Kullanici_Adi\",\"Kitap_Id\" FROM \"FICERIR\" WHERE \"FICERIR\".\"Kullanici_Adi\" = %s and \"FICERIR\".\"Kitap_Id\" = %s" 
        cursor.execute(postgres_command,(username,id))

        postgres_command = """SELECT "Fiyat" FROM "FICERIR", "KITAP" WHERE "KITAP"."Kitap_Id" = %s and "KITAP"."Kitap_Id" = "FICERIR"."Kitap_Id" and "Kullanici_Adi" = %s """
        cursor.execute(postgres_command,(id,username))

        price_sum = cursor.fetchall()
        print(price_sum)
    
        postgres_command = "DELETE FROM \"FICERIR\" WHERE \"Kullanici_Adi\" = %s and \"Kitap_Id\" = %s" 
        cursor.execute(postgres_command, (username,id))

        postgres_command = "UPDATE \"FAVORILER\" set \"FKitap_Adet\" = \"FKitap_Adet\" - 1 where \"Kullanici_Adi\" = %s" 
        cursor.execute(postgres_command,(username,))
        postgres_command = "UPDATE \"SEPET\" set \"SKitap_Adet\" = \"SKitap_Adet\" + %s where \"Kullanici_Adi\" = %s" 
        cursor.execute(postgres_command,(1,username))

        postgres_command = "UPDATE \"SEPET\" set \"Sepet_Tutar\" = \"Sepet_Tutar\" + %s where \"Kullanici_Adi\" = %s" 
        cursor.execute(postgres_command,(price_sum[0][0],username))


        connection.commit()
        print("Add the favorite to cart successfully")
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def add_book_to_cart(username, id):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
       
        postgres_command = """SELECT "Fiyat" FROM "KITAP" WHERE "Kitap_Id" = %s """
        cursor.execute(postgres_command,(id,))
        
        price_sum = cursor.fetchall()
        print("Book price")
        print(price_sum)

        postgres_command = "UPDATE \"SEPET\" set \"SKitap_Adet\" = \"SKitap_Adet\" + %s where \"Kullanici_Adi\" = %s" 
        cursor.execute(postgres_command,(1,username,))

        postgres_command = "UPDATE \"SEPET\" set \"Sepet_Tutar\" = \"Sepet_Tutar\" + %s where \"Kullanici_Adi\" = %s" 
        cursor.execute(postgres_command,(price_sum[0][0],username,))

        postgres_command = "INSERT INTO \"SICERIR\" VALUES (%s,%s)"  
        cursor.execute(postgres_command,(username,id,))

        connection.commit()
        print("Add the book to cart successfully")
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def add_book_to_fav(username, id):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
       
        postgres_command = "UPDATE \"FAVORILER\" set \"FKitap_Adet\" = \"FKitap_Adet\" + %s where \"Kullanici_Adi\" = %s" 
        cursor.execute(postgres_command,(1,username,))

        postgres_command = "INSERT INTO \"FICERIR\" VALUES (%s,%s)"  
        cursor.execute(postgres_command,(username,id,))

        connection.commit()
        print("Add the book to fav successfully")
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")            

app = Flask(__name__)

@app.route("/")
def home():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        cursor.execute("""SELECT "Kitap_Id", COUNT ("Kitap_Id") AS id FROM "SATIN_ALIR" GROUP BY "Kitap_Id" ORDER BY id DESC LIMIT 5""")
        cokSatanlarIds = cursor.fetchall()

        cokSatanlar = []
        for id in cokSatanlarIds:
            cursor.execute("""SELECT "Kitap_Id", "Kitap_Ismi", "Fiyat", "Fotograf_Adi" FROM \"KITAP\" WHERE "Kitap_Id" = %s""", (id[0], ))
            cokSatanlar.append(cursor.fetchone())

        cursor.execute("""SELECT "Kitap_Id", "Kitap_Ismi", "Fiyat", "Fotograf_Adi" FROM \"KITAP\"""")
        randomKitaplar = random.sample(cursor.fetchall(), 5)
        connection.commit()
            
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data from KITAP table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return render_template("home.html", cokSatanlar = cokSatanlar, randomKitaplar = randomKitaplar)



@app.route("/login", methods=['GET'])
def login():
    return render_template("login.html")


@app.route("/register", methods=['GET'])
def register():
    return render_template("register.html")


@app.route("/admin", methods=['GET'])
def admin():
    return render_template("admin.html")

@app.route("/satin_al/<string:username>/<int:kitap_id>", methods=['GET'])
def satin_al(username, kitap_id):
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        cursor.execute("""SELECT "Kitap_Ismi", "Fiyat", "Kitap_Id" FROM "KITAP" WHERE "Kitap_Id" = %s""", (kitap_id, ))
        kitap = cursor.fetchall()
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data from KITAP table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")        
        return render_template("/satin_al.html", username = username, kitaplar = kitap, toplam = kitap[0][1])
        
@app.route("/handle_satin_al/<string:username>/<float:toplam>", methods=['GET'])
def handle_satin_al(username, toplam):
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()
        message = ""
        cursor.execute("""SELECT "Kullanici_Bakiyesi" FROM "KULLANICI" WHERE "Kullanici_Adi" = %s""", (username, ))
        kullaniciBakiyesi = float(cursor.fetchone()[0])

        if kullaniciBakiyesi < toplam:
            message = "Error"
        else:
            cursor.execute("""UPDATE "KULLANICI" SET "Kullanici_Bakiyesi" = %s WHERE "Kullanici_Adi" = %s""", (kullaniciBakiyesi - toplam, username))

        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data from KITAP table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed") 
        if message == "Error":
            return render_template("/satin_al.html", message = message)
        else:    
            return redirect(url_for("logged", username = username))

@app.route("/logged", methods=['GET'])
def logged():
    try:
        username = request.args['username']
        sepet_adet = get_sepet_kitaplar(username)[1]
        favori_adet = get_favori_kitaplar(username)[1]
        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        kitaplar = []
        cursor.execute("""SELECT "Kitap_Id" FROM "FICERIR" WHERE "Kullanici_Adi" = %s""", ("okarahan", ))
        kitapIds = cursor.fetchall()
        for kitapId in kitapIds:
            cursor.execute("""SELECT * FROM "KITAP" WHERE "Kitap_Id" = %s""", (kitapId, ))
            kitaplar.append(cursor.fetchone())

        cursor.execute("""SELECT "Kitap_Id" FROM "SICERIR" WHERE "Kullanici_Adi" = %s""", ("okarahan", ))
        kitapIds = cursor.fetchall()
        for kitapId in kitapIds:
            cursor.execute("""SELECT * FROM "KITAP" WHERE "Kitap_Id" = %s""", (kitapId, ))
            kitaplar.append(cursor.fetchone())

        cursor.execute("""SELECT "Kitap_Id" FROM "SATIN_ALIR" WHERE "Kullanici_Adi" = %s""", ("okarahan", ))
        kitapIds = cursor.fetchall()
        for kitapId in kitapIds:
            cursor.execute("""SELECT * FROM "KITAP" WHERE "Kitap_Id" = %s""", (kitapId, ))
            kitaplar.append(cursor.fetchone())

        kategoriler = []
        for kitap in kitaplar:
            cursor.execute("""SELECT "Kategori_Id" FROM "AITTIR" WHERE "Kitap_Id" = %s""", (kitap[0], ))
            kategoriId = cursor.fetchone()[0]
            if not kategoriId in kategoriler:
                kategoriler.append(kategoriId)

        if kategoriler:
            hangiKategoridenKacKitap = []
            x = 5 / len(kategoriler)
            for i in range(0, len(kategoriler) - 1):
                hangiKategoridenKacKitap.append(1)
            hangiKategoridenKacKitap.append(5 - len(hangiKategoridenKacKitap))
        
        oneriKitaplar = []
        for i in range(0, len(kategoriler)):
            cursor.execute("""SELECT "Kitap_Id" FROM "AITTIR" WHERE "Kategori_Id" = %s""", (kategoriler[i], ))
            oneriKitaplarIds = random.sample(cursor.fetchall(), hangiKategoridenKacKitap[i])
            for id in oneriKitaplarIds:
                cursor.execute("""SELECT "Kitap_Id", "Kitap_Ismi", "Fiyat", "Fotograf_Adi" FROM \"KITAP\" WHERE "Kitap_Id" = %s""", (id[0], ))
                oneriKitaplar.append(cursor.fetchone())

        cursor.execute("""SELECT "Kitap_Id", COUNT ("Kitap_Id") AS id FROM "SATIN_ALIR" GROUP BY "Kitap_Id" ORDER BY id DESC LIMIT 5""")
        cokSatanlarIds = cursor.fetchall()

        cokSatanlar = []
        for id in cokSatanlarIds:
            cursor.execute("""SELECT "Kitap_Id", "Kitap_Ismi", "Fiyat", "Fotograf_Adi" FROM \"KITAP\" WHERE "Kitap_Id" = %s""", (id[0], ))
            cokSatanlar.append(cursor.fetchone())

        cursor.execute("""SELECT "Kitap_Id", "Kitap_Ismi", "Fiyat", "Fotograf_Adi" FROM \"KITAP\"""")
        randomKitaplar = random.sample(cursor.fetchall(), 5)

        print(sepet_adet)
        print(favori_adet)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data from KULLANICI table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")        
        return render_template("logged.html",username=username, sepet_adet = sepet_adet, favori_adet = favori_adet, oneriKitaplar = oneriKitaplar, cokSatanlar = cokSatanlar, randomKitaplar = randomKitaplar)

@app.route("/sepet/<string:username>", methods=['GET'])
def sepet(username):
    sepet_bilgiler = get_sepet_kitaplar(username)
    favori_bilgiler = get_favori_kitaplar(username)

    return render_template("sepet.html", cards=sepet_bilgiler[0], username=username, cart_number = sepet_bilgiler[1], fav_number = favori_bilgiler[1])

@app.route("/sepet_temizle/<string:username>")
def sepet_temizle(username):
    message = ""
    if(get_sepet_kitaplar(username)[1] == 0):
        message = "error"
    clear_sepet(username)
    sepet_bilgiler = get_sepet_kitaplar(username)
    favori_bilgiler = get_favori_kitaplar(username)
    if(message == "error"):
        return render_template("sepet.html", cards=sepet_bilgiler[0], username=username, cart_number = sepet_bilgiler[1], fav_number = favori_bilgiler[1],message=message)
    return redirect(url_for("sepet", cards=sepet_bilgiler[0], username=username, cart_number = sepet_bilgiler[1], fav_number = favori_bilgiler[1], message=message))

@app.route("/favori/<string:username>", methods=['GET'])
def favori(username):
    sepet_bilgiler = get_sepet_kitaplar(username)
    favori_bilgiler = get_favori_kitaplar(username)
    return render_template("favoriler.html", cards=favori_bilgiler[0], username=username, cart_number = sepet_bilgiler[1], fav_number = favori_bilgiler[1])

@app.route("/favori_temizle/<string:username>")
def favori_temizle(username):
    message = "success"
    if(get_favori_kitaplar(username)[1] == 0):
        message = "error"
        
    clear_favori(username)
    sepet_bilgiler = get_sepet_kitaplar(username)
    favori_bilgiler = get_favori_kitaplar(username)
    if(message == "error"):
        return render_template("favoriler.html", cards=favori_bilgiler[0], username=username, cart_number = sepet_bilgiler[1], fav_number = favori_bilgiler[1],message=message)
    return redirect(url_for("favori", cards=favori_bilgiler[0], username=username, cart_number = sepet_bilgiler[1], fav_number = favori_bilgiler[1]))

@app.route("/butun_favori_sepete_ekle/<string:username>")
def butun_favori_sepet_ekle(username):
    print(username)
    add_favorites_to_cart(username)
    return redirect(url_for("favori", cards=get_favori_kitaplar(username), username=username, ))

@app.route("/favori_sepete_ekle/<string:username>/<string:id>")
def favori_sepet_ekle(username, id):
    print(username)
    add_favorite_to_cart(username, id)
    return redirect(url_for("favori", cards=get_favori_kitaplar(username), username=username, ))

@app.route("/kitap_sepete_ekle/<string:username>/<string:id>")
def kitap_sepet_ekle(username, id):
    add_book_to_cart(username, id)
    sepet_adet = get_sepet_kitaplar(username)[1]
    favori_adet = get_favori_kitaplar(username)[1]
    return redirect(url_for("logged",username=username,sepet_adet=sepet_adet,favori_adet=favori_adet))

@app.route("/kitap_fav_ekle/<string:username>/<string:id>")
def kitap_fav_ekle(username, id):
    add_book_to_fav(username, id)
    sepet_adet = get_sepet_kitaplar(username)[1]
    favori_adet = get_favori_kitaplar(username)[1]
    return redirect(url_for("logged",username=username,sepet_adet=sepet_adet,favori_adet=favori_adet))

@app.route("/login_check", methods=['POST'])
def login_check():
    username = request.form.get("kullanici_adi")
    password = request.form.get("sifre")
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    db_password = get_sifre(username)
    message = "Error"
    
    if hashed_password == db_password:
        return redirect(url_for("logged",username=username))
    else:
        return render_template("login.html",message = message)

@app.route("/register_process", methods=['POST'])
def register_process():
    name = request.form.get("isim")
    surname = request.form.get("soyisim")
    username = request.form.get("kullanici_adi")
    
    password = request.form.get("sifre")
    email = request.form.get("email")
    address = request.form.get("adres")
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    check = insert_user(name,surname,username,hashed_password,email,address)
    
    if(check == 0):
        return redirect(url_for("logged", username=username))
    else:
        return render_template("register.html",message="error")
    
@app.route("/search", methods=['GET', 'POST'])
def search():
    if flask.request.method == 'POST':
        kitaplar = []
        try:
            aranacak = request.form.get("search")
            connection = psycopg2.connect(user="postgres",
                                        password="bahadir",
                                        host="localhost",
                                        port="5432",
                                        database="takebook_db")
            cursor = connection.cursor()
            aranacak = aranacak.lower()
            postgres_read = "SELECT \"Kitap_Id\", \"Kitap_Ismi\", \"Fiyat\", \"Fotograf_Adi\" FROM \"KITAP\" WHERE LOWER(\"Kitap_Ismi\") LIKE %(par)s or CAST(\"Fiyat\" as text) LIKE %(par)s"
            cursor.execute(postgres_read, dict(par='%'+aranacak+'%'))
            kitaplar = cursor.fetchall()

            postgres_read = "SELECT * FROM \"YAYINEVI\" WHERE LOWER(\"Yayinevi_Ismi\") LIKE %(par)s"
            cursor.execute(postgres_read, dict(par='%'+aranacak+'%'))
            yayinevis = cursor.fetchall()
            for yayinevi in yayinevis:
                cursor.execute("""SELECT DISTINCT \"KITAP\".\"Kitap_Id\", \"Kitap_Ismi\", \"Fiyat\", \"Fotograf_Adi\" FROM "KITAP", "BASAR" WHERE "Yayinevi_Id" = %s  AND "KITAP"."Kitap_Id" = "BASAR".\"Kitap_Id\"""", (yayinevi[0], ))
                for kitap in cursor.fetchall():
                    kitaplar.append(kitap)

            postgres_read = "SELECT * FROM \"YAZAR\" WHERE LOWER(\"Yazar_Ismi\") LIKE %(par)s or LOWER(\"Yazar_Soyismi\") LIKE %(par)s"
            cursor.execute(postgres_read, dict(par='%'+aranacak+'%'))
            yazarlar = cursor.fetchall()
            for yazar in yazarlar:
                cursor.execute("""SELECT DISTINCT \"Kitap_Id\", \"Kitap_Ismi\", \"Fiyat\", \"Fotograf_Adi\" FROM "KITAP" WHERE "Yazar_Id" = %s""", (yazar[0], ))
                for kitap in cursor.fetchall():
                    kitaplar.append(kitap)
        except (Exception, psycopg2.Error) as error:
            print(error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
            return render_template("search.html", aranacak = aranacak, kitaplar = kitaplar)
    else:
        return render_template("search.html", aranacak = "", kitaplar = [])

@app.route("/search_user/<string:username>", methods=['GET', 'POST'])
def search_user(username):
    if flask.request.method == 'POST':
        kitaplar = []
        try:
            sepet_adet = get_sepet_kitaplar(username)[1]
            favori_adet = get_favori_kitaplar(username)[1]  
            aranacak = request.form.get("search")
            connection = psycopg2.connect(user="postgres",
                                        password="bahadir",
                                        host="localhost",
                                        port="5432",
                                        database="takebook_db")
            cursor = connection.cursor()
            aranacak = aranacak.lower()
            postgres_read = "SELECT \"Kitap_Id\", \"Kitap_Ismi\", \"Fiyat\", \"Fotograf_Adi\" FROM \"KITAP\" WHERE LOWER(\"Kitap_Ismi\") LIKE %(par)s or CAST(\"Fiyat\" as text) LIKE %(par)s"
            cursor.execute(postgres_read, dict(par='%'+aranacak+'%'))
            kitaplar = cursor.fetchall()

            postgres_read = "SELECT * FROM \"YAYINEVI\" WHERE LOWER(\"Yayinevi_Ismi\") LIKE %(par)s"
            cursor.execute(postgres_read, dict(par='%'+aranacak+'%'))
            yayinevis = cursor.fetchall()
            for yayinevi in yayinevis:
                cursor.execute("""SELECT DISTINCT \"KITAP\".\"Kitap_Id\", \"Kitap_Ismi\", \"Fiyat\", \"Fotograf_Adi\" FROM "KITAP", "BASAR" WHERE "Yayinevi_Id" = %s  AND "KITAP"."Kitap_Id" = "BASAR".\"Kitap_Id\"""", (yayinevi[0], ))
                for kitap in cursor.fetchall():
                    kitaplar.append(kitap)

            postgres_read = "SELECT * FROM \"YAZAR\" WHERE LOWER(\"Yazar_Ismi\") LIKE %(par)s or LOWER(\"Yazar_Soyismi\") LIKE %(par)s"
            cursor.execute(postgres_read, dict(par='%'+aranacak+'%'))
            yazarlar = cursor.fetchall()
            for yazar in yazarlar:
                cursor.execute("""SELECT DISTINCT \"Kitap_Id\", \"Kitap_Ismi\", \"Fiyat\", \"Fotograf_Adi\" FROM "KITAP" WHERE "Yazar_Id" = %s""", (yazar[0], ))
                for kitap in cursor.fetchall():
                    kitaplar.append(kitap)
        except (Exception, psycopg2.Error) as error:
            print(error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
            return render_template("search_user.html", username=username, aranacak = aranacak, kitaplar = kitaplar, sepet_adet=sepet_adet, favori_adet=favori_adet)
    else:
        return render_template("search_user.html", aranacak = "", kitaplar = [])


@app.route("/search_with_conditions/<string:aranacak>", methods=['GET', 'POST'])
def search_with_conditions(aranacak):
    kitaplar = []
    try:
        option = request.form.get("flexRadioDefaultOption")
        condition = request.form.get("flexRadioDefaultCondition")
        connection = psycopg2.connect(user="postgres",
                                    password="bahadir",
                                    host="localhost",
                                    port="5432",
                                    database="takebook_db")
        cursor = connection.cursor()
        aranacak = aranacak.lower()

        postgres_read = "SELECT \"Kitap_Id\", \"Kitap_Ismi\", \"Fiyat\", \"Fotograf_Adi\" FROM \"KITAP\" WHERE LOWER(\"Kitap_Ismi\") LIKE %(par)s or CAST(\"Fiyat\" as text) LIKE %(par)s"
        cursor.execute(postgres_read, dict(par='%'+aranacak+'%'))
        kitaplarForOptionKitap = cursor.fetchall()

        kitaplarForOptionYayinevi = []
        postgres_read = "SELECT * FROM \"YAYINEVI\" WHERE LOWER(\"Yayinevi_Ismi\") LIKE %(par)s"
        cursor.execute(postgres_read, dict(par='%'+aranacak+'%'))
        yayinevis = cursor.fetchall()
        for yayinevi in yayinevis:
            cursor.execute("""SELECT DISTINCT "KITAP"."Kitap_Id", \"Kitap_Ismi\", \"Fiyat\", \"Fotograf_Adi\" FROM "KITAP", "BASAR" WHERE "Yayinevi_Id" = %s  AND "KITAP"."Kitap_Id" = "BASAR".\"Kitap_Id\"""", (yayinevi[0], ))
            for kitap in cursor.fetchall():
                kitaplarForOptionYayinevi.append(kitap)

        kitaplarForOptionYazar = []
        postgres_read = "SELECT * FROM \"YAZAR\" WHERE LOWER(\"Yazar_Ismi\") LIKE %(par)s or LOWER(\"Yazar_Soyismi\") LIKE %(par)s"
        cursor.execute(postgres_read, dict(par='%'+aranacak+'%'))
        yazarlar = cursor.fetchall()
        for yazar in yazarlar:
            cursor.execute("""SELECT DISTINCT \"Kitap_Id\", \"Kitap_Ismi\", \"Fiyat\", \"Fotograf_Adi\" FROM "KITAP" WHERE "Yazar_Id" = %s""", (yazar[0], ))
            for kitap in cursor.fetchall():
                kitaplarForOptionYazar.append(kitap)

        if option == "Kitap":
            kitaplar += kitaplarForOptionKitap
        elif option == "Yayinevi": 
            kitaplar += kitaplarForOptionYayinevi
        elif option == "Yazar":
            kitaplar += kitaplarForOptionYazar
        else:
            kitaplar += kitaplarForOptionKitap
            kitaplar += kitaplarForOptionYayinevi
            kitaplar += kitaplarForOptionYazar
        if condition == "AZ":
            kitaplar.sort(key=lambda k: k[1])
        elif condition == "ZA":
            kitaplar.sort(key=lambda k: k[1], reverse=True)
        elif condition == "FiyatArtan":
            kitaplar.sort(key=lambda k: k[2])
        elif condition == "FiyatAzalan":
            kitaplar.sort(key=lambda k: k[2], reverse=True)
        elif condition == "PuanArtan":
            for i in range (0, len(kitaplar)):
                cursor.execute("""SELECT "Puan_Id" FROM "YAPAR" WHERE "Kitap_Id" = %s""", (kitaplar[i][0], ))
                puanIds = cursor.fetchall()
                puanMiktari = 0
                for j in range (0, len(puanIds)):
                    cursor.execute("""SELECT "Puan_Miktari" FROM "PUAN" WHERE "Puan_Id" = %s""", (puanIds[j], ))
                    puanMiktari += cursor.fetchone()[0]
                if not len(puanIds) == 0:
                    puanMiktari = float(puanMiktari) / len(puanIds)
                kitaplar[i] = kitaplar[i] + (puanMiktari, )
            kitaplar.sort(key=lambda k: k[3])
        elif condition == "PuanAzalan":
            for i in range (0, len(kitaplar)):
                cursor.execute("""SELECT "Puan_Id" FROM "YAPAR" WHERE "Kitap_Id" = %s""", (kitaplar[i][0], ))
                puanIds = cursor.fetchall()
                puanMiktari = 0
                for j in range (0, len(puanIds)):
                    cursor.execute("""SELECT "Puan_Miktari" FROM "PUAN" WHERE "Puan_Id" = %s""", (puanIds[j], ))
                    puanMiktari += cursor.fetchone()[0]
                if not len(puanIds) == 0:
                    puanMiktari = float(puanMiktari) / len(puanIds)
                kitaplar[i] = kitaplar[i] + (puanMiktari,)
            kitaplar.sort(key=lambda k: k[3], reverse=True)

        for kitap in kitaplar:
            print(kitap)
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return render_template("search.html", aranacak = aranacak, kitaplar = kitaplar)        

@app.route("/kategori_user/<string:kategori_adi>/<string:username>", methods=['GET'])
def kategori_user(kategori_adi, username):
    kitaplar = []
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()
        sepet_adet = get_sepet_kitaplar(username)[1]
        favori_adet = get_favori_kitaplar(username)[1] 
        if kategori_adi == "edebiyat":
            cursor.execute("""SELECT "Kitap_Id" FROM "AITTIR" WHERE "Kategori_Id" = %s""", (0, ))
        elif kategori_adi == "müzik":
            cursor.execute("""SELECT "Kitap_Id" FROM "AITTIR" WHERE "Kategori_Id" = %s""", (1, ))
        elif kategori_adi == "ekonomi":
            cursor.execute("""SELECT "Kitap_Id" FROM "AITTIR" WHERE "Kategori_Id" = %s""", (4, ))
        elif kategori_adi == "tarih":
            cursor.execute("""SELECT "Kitap_Id" FROM "AITTIR" WHERE "Kategori_Id" = %s""", (3, ))
        elif kategori_adi == "saglik":
            cursor.execute("""SELECT "Kitap_Id" FROM "AITTIR" WHERE "Kategori_Id" = %s""", (2, ))
        elif kategori_adi == "psikoloji":
            cursor.execute("""SELECT "Kitap_Id" FROM "AITTIR" WHERE "Kategori_Id" = %s""", (5, ))
        kitapIds = cursor.fetchall()
        for id in kitapIds:
            cursor.execute("""SELECT "Kitap_Id", "Kitap_Ismi", "Fiyat", "Fotograf_Adi" FROM "KITAP" WHERE "Kitap_Id" = %s""", (id, ))
            kitaplar.append(cursor.fetchone())
        for kitap in kitaplar:
            print(kitap)
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data from AITTIR table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return render_template("kategori_user.html", kitaplar=kitaplar, username=username, sepet_adet=sepet_adet, favori_adet=favori_adet, kategori = kategori_adi)

@app.route("/kategori/<string:kategori_adi>", methods=['GET'])
def kategori(kategori_adi):
    kitaplar = []
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        if kategori_adi == "edebiyat":
            cursor.execute("""SELECT "Kitap_Id" FROM "AITTIR" WHERE "Kategori_Id" = %s""", (0, ))
        elif kategori_adi == "müzik":
            cursor.execute("""SELECT "Kitap_Id" FROM "AITTIR" WHERE "Kategori_Id" = %s""", (1, ))
        elif kategori_adi == "ekonomi":
            cursor.execute("""SELECT "Kitap_Id" FROM "AITTIR" WHERE "Kategori_Id" = %s""", (4, ))
        elif kategori_adi == "tarih":
            cursor.execute("""SELECT "Kitap_Id" FROM "AITTIR" WHERE "Kategori_Id" = %s""", (3, ))
        elif kategori_adi == "saglik":
            cursor.execute("""SELECT "Kitap_Id" FROM "AITTIR" WHERE "Kategori_Id" = %s""", (2, ))
        elif kategori_adi == "psikoloji":
            cursor.execute("""SELECT "Kitap_Id" FROM "AITTIR" WHERE "Kategori_Id" = %s""", (5, ))
        kitapIds = cursor.fetchall()
        for id in kitapIds:
            cursor.execute("""SELECT "Kitap_Id", "Kitap_Ismi", "Fiyat", "Fotograf_Adi" FROM "KITAP" WHERE "Kitap_Id" = %s""", (id, ))
            kitaplar.append(cursor.fetchone())
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data from AITTIR table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return render_template("kategori.html", kitaplar = kitaplar, kategori = kategori_adi)

@app.route("/kullanici/<string:kullanici_adi>", methods=['GET'])
def kullanici(kullanici_adi):
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        sql_select_query = """SELECT * FROM \"KULLANICI\" WHERE "Kullanici_Adi" = %s"""
        cursor.execute(sql_select_query, (kullanici_adi, ))
        kullanici = cursor.fetchone()

        yorumlar = []
        sql_select_yapar_query = """SELECT * FROM "YAPAR" WHERE "Kullanici_Adi" = %s"""
        cursor.execute(sql_select_yapar_query, (kullanici_adi, ))
        yaparTableRecords = cursor.fetchall()

        for yaparTableRecord in yaparTableRecords:
            cursor.execute("""SELECT "Puan_Miktari" FROM "PUAN" WHERE "Puan_Id" = %s""", (yaparTableRecord[2], ))
            puan = cursor.fetchone()
            cursor.execute("""SELECT "Yorum_Icerigi" FROM "YORUM" WHERE "Yorum_Id" = %s""", (yaparTableRecord[3], ))
            yorum = cursor.fetchone()
            cursor.execute("""SELECT "Kitap_Ismi" FROM "KITAP" WHERE "Kitap_Id" = %s""", (yaparTableRecord[0], ))
            kitap = cursor.fetchone()
            yorumlar.append((kitap[0], yaparTableRecord[1], puan, yorum[0], yaparTableRecord[4]))

            
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data from KULLANICI table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return render_template("kullanici.html", kullanici = kullanici, yorumlar = yorumlar)

@app.route("/kullanici_bilgileri_guncelle/<string:kullanici_adi>", methods=['POST'])
def kullanici_bilgileri_guncelle(kullanici_adi):
    try:
        email = request.form.get("email")
        isim = request.form.get("kullanici_ismi")
        soyisim = request.form.get("kullanici_soyadi")
        adres = request.form.get("adres")

        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        sql_update_query = """UPDATE "KULLANICI" SET "Kullanici_Ismi" = %s, "Kullanici_Soyismi" = %s, "Kullanici_EMail" = %s, "Kullanici_Adresi" = %s WHERE "Kullanici_Adi" = %s"""
        record_to_update = (isim, soyisim, email, adres, kullanici_adi)
        cursor.execute(sql_update_query, record_to_update)

        connection.commit()
        print(cursor.rowcount, "Record updated successfully in KULLANICI table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to update record in KULLANICI table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return redirect(url_for("kullanici", kullanici_adi = kullanici_adi))

@app.route("/bakiye_ekle/<string:kullanici_adi>", methods=['POST'])
def bakiye_ekle(kullanici_adi):
    try:
        bakiye = request.form.get("bakiye_id")
        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        cursor.execute("""SELECT "Kullanici_Bakiyesi" FROM "KULLANICI" WHERE "Kullanici_Adi" = %s""", (kullanici_adi, ))
        guncelBakiye = cursor.fetchone()[0]
        eklenmisBakiye = int(guncelBakiye) + int(bakiye)

        cursor.execute("""UPDATE "KULLANICI" SET "Kullanici_Bakiyesi" = %s WHERE "Kullanici_Adi" = %s""", (eklenmisBakiye, kullanici_adi))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data from KULLANICI table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return redirect(url_for("kullanici", kullanici_adi = kullanici_adi))

@app.route("/kitap/<int:kitap_id>", methods=['GET'])
def kitap(kitap_id):
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        sql_select_query = """SELECT * FROM \"KITAP\" WHERE "Kitap_Id" = %s"""
        cursor.execute(sql_select_query, (kitap_id, ))
        kitap = cursor.fetchone()
        kitap = kitap[:4]+getYayineviOfKitap(kitap[0])+kitap[4:]

        yorumlar = []
        sql_select_yapar_query = """SELECT * FROM "YAPAR" WHERE "Kitap_Id" = %s"""
        cursor.execute(sql_select_yapar_query, (kitap_id, ))
        yaparTableRecords = cursor.fetchall()
        
        for yaparTableRecord in yaparTableRecords:
            cursor.execute("""SELECT "Puan_Miktari" FROM "PUAN" WHERE "Puan_Id" = %s""", (yaparTableRecord[2], ))
            puan = cursor.fetchone()
            cursor.execute("""SELECT "Yorum_Icerigi" FROM "YORUM" WHERE "Yorum_Id" = %s""", (yaparTableRecord[3], ))
            yorum = cursor.fetchone()
            yorumlar.append((yaparTableRecord[0], yaparTableRecord[1], puan, yorum[0], yaparTableRecord[4]))
            
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data from KITAP table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return render_template("kitap.html", kitap = kitap, yorumlar = yorumlar)

@app.route("/yorum_ekle/<int:kitap_id>", methods=['POST'])
def yorum_ekle(kitap_id):
    try:
        puan = request.form.get("rate")
        yorum = request.form.get("yorum")
        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        cursor.execute("""SELECT MAX("Puan_Id") FROM \"PUAN\"""")
        maxPuanId = cursor.fetchone()[0]

        cursor.execute("""SELECT MAX("Yorum_Id") FROM \"YORUM\"""")
        maxYorumId = cursor.fetchone()[0]

        cursor.execute("""INSERT INTO "PUAN" ("Puan_Id", "Puan_Miktari") VALUES (%s, %s)""", (int(maxPuanId) + 1, puan))
        cursor.execute("""INSERT INTO "YORUM" ("Yorum_Id", "Yorum_Icerigi") VALUES (%s, %s)""", (int(maxYorumId) + 1, yorum))

        sql_insert_query = """INSERT INTO "YAPAR" ("Kitap_Id", "Kullanici_Adi", "Puan_Id", "Yorum_Id", "Y_Timestamp") VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql_insert_query, (kitap_id, "okarahan", int(maxPuanId) + 1, int(maxYorumId) + 1, datetime.today().strftime('%Y-%m-%d')))

        connection.commit()
            
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data from PUAN or YORUM table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return redirect(url_for("kitap", kitap_id = kitap_id))

@app.route("/kullanici_crud", methods=['GET'])
def kullanici_crud():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        sql_select_query = """SELECT * FROM \"KULLANICI\""""
        cursor.execute(sql_select_query)
        kullanicilar = cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data from KULLANICI table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return render_template("kullanici_crud.html", kullanicilar = kullanicilar)

@app.route("/kitap_crud", methods=['GET'])
def kitap_crud():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        sql_select_query = """SELECT * FROM \"KITAP\""""
        cursor.execute(sql_select_query)
        kitaplar = cursor.fetchall()
        
        for i in range(0, len(kitaplar)):
            kitaplar[i] = kitaplar[i][:4]+getYayineviOfKitap(kitaplar[i][0])+kitaplar[i][4:]
        
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data from KITAP table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")  
        return render_template("kitap_crud.html", kitaplar = kitaplar)

@app.route("/kategori_crud", methods=['GET'])
def kategori_crud():
    return render_template("kategori_crud.html", kategoriler=get_kategori_details())

@app.route("/yayinevi_crud", methods=['GET'])
def yayinevi_crud():
    return render_template("yayinevi_crud.html", yayinevleri=get_yayinevi_details())

@app.route("/yazar_crud", methods=['GET'])
def yazar_crud():
    return render_template("yazar_crud.html", yazarlar=get_yazar_details())

@app.route("/yorum_crud", methods=['GET'])
def yorum_crud():
    return render_template("yorum_crud.html", yorumlar=get_yorum_details())

@app.route("/kullanici_ekle", methods=['POST'])
def kullanici_ekle():
    try:
        kullaniciAdi = request.form.get("kullanici_adi")
        sifre = request.form.get("sifre")
        email = request.form.get("email")
        isim = request.form.get("isim")
        soyisim = request.form.get("soyisim")
        adres = request.form.get("adres")
        bakiye = request.form.get("bakiye")

        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        sql_insert_query = """INSERT INTO "KULLANICI" ("Kullanici_Adi", "Kullanici_Sifresi", "Kullanici_EMail", "Kullanici_Ismi", "Kullanici_Soyismi", "Kullanici_Adresi", "Kullanici_Bakiyesi") VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        record_to_insert = (kullaniciAdi, sifre, email, isim, soyisim, adres, bakiye)
        cursor.execute(sql_insert_query, record_to_insert)

        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into KULLANICI table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into KULLANICI table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return redirect(url_for("kullanici_crud"))

@app.route("/kullanici_guncelle", methods=['POST'])
def kullanici_guncelle():
    try:
        kullaniciAdi = request.form.get("kullanici_adi")
        sifre = request.form.get("sifre")
        email = request.form.get("email")
        isim = request.form.get("isim")
        soyisim = request.form.get("soyisim")
        adres = request.form.get("adres")
        bakiye = request.form.get("bakiye")

        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        sql_update_query = """UPDATE "KULLANICI" SET "Kullanici_Adi" = %s, "Kullanici_Sifresi" = %s, "Kullanici_EMail" = %s, "Kullanici_Ismi" = %s, "Kullanici_Soyismi" = %s, "Kullanici_Adresi" = %s, "Kullanici_Bakiyesi" = %s WHERE "Kullanici_Adi" = %s"""
        record_to_insert = (kullaniciAdi, sifre, email, isim, soyisim, adres, bakiye, kullaniciAdi)
        cursor.execute(sql_update_query, record_to_insert)

        connection.commit()
        print(cursor.rowcount, "Record updated successfully in KULLANICI table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to update record in KULLANICI table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return redirect(url_for("kullanici_crud"))

@app.route("/delete_kullanici/<string:kullanici_adi>")
def kullanici_sil(kullanici_adi):
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        sql_delete_query = """DELETE FROM "KULLANICI" WHERE "Kullanici_Adi" = %s"""
        cursor.execute(sql_delete_query, (kullanici_adi, ))

        connection.commit()
        print(cursor.rowcount, "Record deleted successfully from KULLANICI table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to delete record from KULLANICI table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return redirect(url_for("kullanici_crud"))

@app.route("/kitap_ekle", methods=['POST'])
def kitap_ekle():
    try:
        kitapIsmi = request.form.get("kitap_ismi")
        fiyat = request.form.get("fiyat")
        basimTarihi = request.form.get("basim_tarihi")
        yayinevi = request.form.get("yayinevi")
        hamurTipi = request.form.get("hamur_tipi")
        sayfaSayisi = request.form.get("sayfa_sayisi")
        ebat = request.form.get("ebat")
        dil = request.form.get("dil")
        cevirmen = request.form.get("cevirmen")
        yazarId = request.form.get("yazar_id")
        baskiSayisi = request.form.get("baski_sayisi")
        
        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        cursor.execute("""SELECT MAX("Kitap_Id") FROM \"KITAP\"""")
        kitapId = int(cursor.fetchone()[0]) + 1

        sql_insert_query = """INSERT INTO "KITAP" ("Kitap_Id", "Kitap_Ismi", "Fiyat", "Basim_Tarihi", "Hamur_Tipi", "Sayfa_Sayisi", "Ebat", "Dil", "Cevirmen", "Yazar_Id", "Baski_Sayisi") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        record_to_insert = (kitapId, kitapIsmi, fiyat, basimTarihi, hamurTipi, sayfaSayisi, ebat, dil, cevirmen, yazarId, baskiSayisi)
        cursor.execute(sql_insert_query, record_to_insert)

        if checkIfYayineviExists(yayinevi):
            cursor.execute("""SELECT "Yayinevi_Id" FROM "YAYINEVI" WHERE "Yayinevi_Ismi" = %s""", (yayinevi, ))
            yayineviId = cursor.fetchone()[0]
            sql_insert_basar_query = """INSERT INTO "BASAR" ("Kitap_Id", "Yayinevi_Id") VALUES (%s, %s)"""
            record_to_insert_basar = (kitapId, yayineviId)
            cursor.execute(sql_insert_basar_query, record_to_insert)
        else:
            cursor.execute("""SELECT MAX("Yayinevi_Id") FROM \"YAYINEVI\"""")
            yayineviId = int(cursor.fetchone()[0]) + 1
            sql_insert_yayinevi_query = """INSERT INTO "YAYINEVI" ("Yayinevi_Id", "Yayinevi_Ismi") VALUES (%s, %s)"""
            record_to_insert_yayinevi = (yayineviId, yayinevi)
            cursor.execute(sql_insert_yayinevi_query, record_to_insert_yayinevi)

            sql_insert_basar_query = """INSERT INTO "BASAR" ("Kitap_Id", "Yayinevi_Id") VALUES (%s, %s)"""
            record_to_insert_basar = (kitapId, yayineviId)
            cursor.execute(sql_insert_basar_query, record_to_insert_basar)

        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into KULLANICI table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into KULLANICI table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return redirect(url_for("kitap_crud"))

@app.route("/kitap_guncelle", methods=['POST'])
def kitap_guncelle():
    try:
        kitapId = request.form.get("kitap_id")
        kitapIsmi = request.form.get("kitap_ismi")
        fiyat = request.form.get("fiyat")
        basimTarihi = request.form.get("basim_tarihi")
        yayinevi = request.form.get("yayinevi")
        hamurTipi = request.form.get("hamur_tipi")
        sayfaSayisi = request.form.get("sayfa_sayisi")
        ebat = request.form.get("ebat")
        dil = request.form.get("dil")
        cevirmen = request.form.get("cevirmen")
        yazarId = request.form.get("yazar_id")
        baskiSayisi = request.form.get("baski_sayisi")

        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        sql_update_query = """UPDATE "KITAP" SET "Kitap_Ismi" = %s, "Fiyat" = %s, "Basim_Tarihi" = %s, "Hamur_Tipi" = %s, "Sayfa_Sayisi" = %s, "Ebat" = %s, "Dil" = %s, "Cevirmen" = %s, "Yazar_Id" = %s, "Baski_Sayisi" = %s WHERE "Kitap_Id" = %s"""
        record_to_update = (kitapIsmi, fiyat, basimTarihi, hamurTipi, sayfaSayisi, ebat, dil, cevirmen, yazarId, baskiSayisi, kitapId)
        cursor.execute(sql_update_query, record_to_update)

        if checkIfYayineviExists(yayinevi):
            cursor.execute("""SELECT "Yayinevi_Id" FROM "YAYINEVI" WHERE "Yayinevi_Ismi" = %s""", (yayinevi, ))
            yayineviId = cursor.fetchone()[0]
            cursor.execute("""UPDATE "BASAR" SET "Yayinevi_Id" = %s WHERE "Kitap_Id" = %s""", (yayineviId, kitapId))

        connection.commit()
        print(cursor.rowcount, "Record updated successfully in KITAP table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to update record in KITAP table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return redirect(url_for("kullanici_crud"))

@app.route("/delete_kitap/<int:kitap_adi>")
def kitap_sil(kitap_id):
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        sql_delete_query = """DELETE FROM "KITAP" WHERE "Kitap_Id" = %s"""
        cursor.execute(sql_delete_query, (kitap_id, ))

        connection.commit()
        print(cursor.rowcount, "Record deleted successfully from KITAP table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to delete record from KITAP table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return redirect(url_for("kullanici_crud"))

@app.route("/yayinevi_ekle", methods=['POST'])
def yayinevi_ekle():
    try:
        name = request.form.get("yayinevi_ismi")
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()

        cursor.execute("""SELECT MAX("Yayinevi_Id") FROM \"YAYINEVI\"""")
        id = int(cursor.fetchone()[0]) + 1

        postgres_insert_query = """ INSERT INTO \"YAYINEVI\" (\"Yayinevi_Id\", \"Yayinevi_Ismi\") VALUES (%s,%s)"""
        record_to_insert = (id, name)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        print("Inserted successfully")
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return redirect(url_for("yayinevi_crud"))

@app.route("/yayinevi_guncelle", methods=["POST"])
def yayinevi_guncelle():
    try:
        id = request.form.get("yayinevi_id")
        name = request.form.get("yayinevi_ismi")
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")

        cursor = connection.cursor()
        sql_update_query = """Update \"YAYINEVI\" set \"Yayinevi_Ismi\" = %s where \"Yayinevi_Id\" = %s"""
        cursor.execute(sql_update_query, (name, id))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return render_template("yayinevi_crud.html", yayinevleri=get_yayinevi_details())    

@app.route("/delete_yayinevi/<string:id>")
def yayinevi_sil(id):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")

        cursor = connection.cursor()

        sql_delete_query = """Delete from \"YAYINEVI\" where \"Yayinevi_Id\" = %s"""
        record_to_delete = (id,)
        cursor.execute(sql_delete_query, record_to_delete)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record deleted successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error in Delete operation", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return redirect(url_for("yayinevi_crud"))

@app.route("/yazar_ekle", methods=['POST'])
def yazar_ekle():
    try:
        name = request.form.get("yazar_ismi")
        surname = request.form.get("yazar_soyismi")
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()

        cursor.execute("""SELECT MAX("Yazar_Id") FROM \"YAZAR\"""")
        id = int(cursor.fetchone()[0]) + 1

        postgres_insert_query = """ INSERT INTO \"YAZAR\" (\"Yazar_Id\", \"Yazar_Ismi\", \"Yazar_Soyismi\") VALUES (%s,%s,%s)"""
        record_to_insert = (id, name, surname)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        print("Inserted yazar successfully")
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return redirect(url_for("yazar_crud"))


@app.route("/yazar_guncelle", methods=["POST"])
def yazar_guncelle():
    try:
        id = request.form.get("yazar_id")
        name = request.form.get("yazar_ismi")
        surname = request.form.get("yazar_soyismi")
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="localhost",
                                      port="5432",
                                      database="takebook_db")

        cursor = connection.cursor()
        sql_update_query = """Update \"YAZAR" set \"Yazar_Ismi\" = %s , \"Yazar_Soyismi\" = %s  where \"Yazar_Id\" = %s"""
        cursor.execute(sql_update_query, (name, surname, id))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return render_template("yazar_crud.html", yazarlar=get_yazar_details())


@app.route("/delete_yazar/<string:id>")
def yazar_sil(id):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="localhost",
                                      port="5432",
                                      database="takebook_db")

        cursor = connection.cursor()

        sql_delete_query = """Delete from \"YAZAR\" where \"Yazar_Id\" = %s"""
        record_to_delete = (id,)
        cursor.execute(sql_delete_query, record_to_delete)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record deleted successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error in Delete operation", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return redirect(url_for("yazar_crud"))


@app.route("/delete_yorum/<string:id>")
def yorum_sil(id):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="localhost",
                                      port="5432",
                                      database="takebook_db")

        cursor = connection.cursor()

        sql_delete_query = """Delete from \"YORUM\" where \"Yorum_Id\" = %s"""
        record_to_delete = (id,)
        cursor.execute(sql_delete_query, record_to_delete)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record deleted successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error in Delete operation", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return redirect(url_for("yorum_crud"))

@app.route("/kategori_ekle", methods=['POST'])
def kategori_ekle():
    try:
        name = request.form.get("kategori_ismi")
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="localhost",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()

        cursor.execute("""SELECT MAX("Kategori_Id") FROM \"KATEGORI\"""")
        id = int(cursor.fetchone()[0]) + 1

        postgres_insert_query = """ INSERT INTO \"KATEGORI\" (\"Kategori_Id\", \"Kategori_Ismi\") VALUES (%s,%s)"""
        record_to_insert = (id, name)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        print("Inserted successfully")
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return redirect(url_for("kategori_crud"))

@app.route("/kategori_guncelle", methods=["POST"])
def kategori_guncelle():
    try:
        id = request.form.get("kategori_id")
        name = request.form.get("kategori_ismi")
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="localhost",
                                      port="5432",
                                      database="takebook_db")

        cursor = connection.cursor()
        sql_update_query = """Update \"KATEGORI\" set \"Kategori_Ismi\" = %s where \"Kategori_Id\" = %s"""
        cursor.execute(sql_update_query, (name, id))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return render_template("kategori_crud.html", kategoriler=get_kategori_details())

@app.route("/delete_kategori/<string:id>")
def kategori_sil(id):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="localhost",
                                      port="5432",
                                      database="takebook_db")

        cursor = connection.cursor()
        sql_delete_query = """Delete from \"KATEGORI\" where \"Kategori_Id\" = %s"""
        record_to_delete = (id,)
        cursor.execute(sql_delete_query, record_to_delete)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record deleted successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error in Delete operation", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return redirect(url_for("kategori_crud"))

@app.route("/kullanici_ara", methods=["POST"])
def kullanici_ara():
    kullanici = []
    try:
        aranacak = request.form.get("search_word")
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="localhost",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        aranacak = aranacak.lower()
        postgres_read = "SELECT * FROM \"KULLANICI\" WHERE LOWER(\"Kullanici_Adi\") LIKE %(par)s or LOWER(\"Kullanici_Sifresi\") LIKE %(par)s or LOWER(\"Kullanici_EMail\") LIKE %(par)s or LOWER(\"Kullanici_Ismi\") LIKE %(par)s or LOWER(\"Kullanici_Soyismi\") LIKE %(par)s or LOWER(\"Kullanici_Adresi\") LIKE %(par)s or CAST(\"Kullanici_Bakiyesi\" as text) LIKE %(par)s"
        cursor.execute(postgres_read, dict(par='%'+aranacak+'%'))
        kullanici = cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return render_template("kullanici_crud.html", kullanicilar=kullanici)

@app.route("/kitap_ara", methods=["POST"])
def kitap_ara():
    kitap = []
    try:
        aranacak = request.form.get("search_word")
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="localhost",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        aranacak = aranacak.lower()
        postgres_read = "SELECT * FROM \"KITAP\" WHERE CAST(\"Kitap_Id\" as text) LIKE %(par)s or LOWER(\"Kitap_Ismi\") LIKE %(par)s or CAST(\"Fiyat\" as text) LIKE %(par)s or CAST(\"Basim_Tarihi\" as text) LIKE %(par)s or LOWER(\"Hamur_Tipi\") LIKE %(par)s or CAST(\"Sayfa_Sayisi\" as text) LIKE %(par)s or LOWER(\"Ebat\") LIKE %(par)s or LOWER(\"Dil\") LIKE %(par)s or LOWER(\"Cevirmen\") LIKE %(par)s or CAST(\"Yazar_Id\" as text) LIKE %(par)s or LOWER(\"Baski_Sayisi\") LIKE %(par)s"
        cursor.execute(postgres_read, dict(par='%'+aranacak+'%'))
        kitap = cursor.fetchall()
        for i in range(0, len(kitap)):
            kitap[i] = kitap[i][:4]+getYayineviOfKitap(kitap[i][0])+kitap[i][4:]

        postgres_read = "SELECT * FROM \"YAYINEVI\" WHERE CAST(\"Yayinevi_Id\" as text) LIKE %(par)s or LOWER(\"Yayinevi_Ismi\") LIKE %(par)s"
        cursor.execute(postgres_read, dict(par='%'+aranacak+'%'))
        yayinevis = cursor.fetchall()
        for yayinevi in yayinevis:
            cursor.execute("""SELECT DISTINCT "KITAP"."Kitap_Id", "Kitap_Ismi", "Fiyat", "Basim_Tarihi", "Hamur_Tipi", "Sayfa_Sayisi", "Ebat", "Dil", "Cevirmen", "Yazar_Id", "Baski_Sayisi" FROM "KITAP", "BASAR" WHERE "Yayinevi_Id" = %s  AND "KITAP"."Kitap_Id" = "BASAR".\"Kitap_Id\"""", (yayinevi[0], ))
            kitapTuples = cursor.fetchall()
            for i in range(0, len(kitapTuples)):
                kitap.append(kitapTuples[i][:4]+(yayinevi[1], )+kitapTuples[i][4:])
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return render_template("kitap_crud.html", kitaplar=kitap)

@app.route("/yorum_ara", methods=["POST"])
def yorum_ara():
    yorum = []
    try:
        aranacak = request.form.get("search_word")
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="localhost",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        aranacak = aranacak.lower()
        postgres_read = "SELECT * FROM \"YORUM\" WHERE CAST(\"Yorum_Id\" as text) LIKE %(par)s or LOWER(\"Yorum_Icerigi\") LIKE %(par)s"
        cursor.execute(postgres_read, dict(par='%'+aranacak+'%'))
        yorum = cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return render_template("yorum_crud.html", yorumlar=yorum)

@app.route("/yazar_ara", methods=["POST"])
def yazar_ara():
    yazar = []
    try:
        aranacak = request.form.get("search_word")
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="localhost",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        aranacak = aranacak.lower()
        postgres_read = "SELECT * FROM \"YAZAR\" WHERE CAST(\"Yazar_Id\" as text) LIKE %(par)s or LOWER(\"Yazar_Ismi\") LIKE %(par)s or LOWER(\"Yazar_Soyismi\") LIKE %(par)s"
        cursor.execute(postgres_read, dict(par='%'+aranacak+'%'))
        yazar = cursor.fetchall()
        print(yazar)
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed") 
        return render_template("yazar_crud.html", yazarlar=yazar)  

@app.route("/yayinevi_ara", methods=["POST"])
def yayinevi_ara():
    yayinevi = []
    try:
        aranacak = request.form.get("search_word")
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="localhost",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        aranacak = aranacak.lower()
        postgres_read = "SELECT * FROM \"YAYINEVI\" WHERE CAST(\"Yayinevi_Id\" as text) LIKE %(par)s or LOWER(\"Yayinevi_Ismi\") LIKE %(par)s"
        cursor.execute(postgres_read, dict(par='%'+aranacak+'%'))
        yayinevi = cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return render_template("yayinevi_crud.html", yayinevleri=yayinevi)

@app.route("/kategori_ara", methods=["POST"])
def kategori_ara():
    kategori = []
    try:
        aranacak = request.form.get("search_word")
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="localhost",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        aranacak = aranacak.lower()
        postgres_read = "SELECT * FROM \"KATEGORI\" WHERE CAST(\"Kategori_Id\" as text) LIKE %(par)s or LOWER(\"Kategori_Ismi\") LIKE %(par)s "
        cursor.execute(postgres_read, dict(par='%'+aranacak+'%'))
        kategori = cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return render_template("kategori_crud.html", kategoriler=kategori)

def getYayineviOfKitap(kitapId):
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        sql_select_query = "SELECT \"Yayinevi_Ismi\" FROM \"BASAR\", \"YAYINEVI\" WHERE \"Kitap_Id\" = %s AND \"BASAR\".\"Yayinevi_Id\" = \"YAYINEVI\".\"Yayinevi_Id\""
        cursor.execute(sql_select_query, (kitapId, ))
        return cursor.fetchone()
        
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch YAYINEVI id", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()

def checkIfYayineviExists(yayineviIsmi):
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="bahadir",
            host="localhost",
            port="5432",
            database="takebook_db")
        cursor = connection.cursor()

        sql_select_query = """SELECT * FROM \"YAYINEVI\""""
        cursor.execute(sql_select_query)
        yayinevleri = cursor.fetchall()

        for yayinevi in yayinevleri:
            dbYayineviIsmi = yayinevi[1]
            if dbYayineviIsmi == yayineviIsmi:
                return True
        return False

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into KULLANICI table", error)

    finally:
        #closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def get_yayinevi_details():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="localhost",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        postgres_read = "SELECT * FROM \"YAYINEVI\""
        cursor.execute(postgres_read)
        yayinevi = cursor.fetchall()
        return yayinevi
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def get_yazar_details():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="localhost",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        postgres_read = "SELECT * FROM \"YAZAR\""
        cursor.execute(postgres_read)
        yazar = cursor.fetchall()
        return yazar
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def get_yorum_details():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="localhost",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        postgres_read = "SELECT * FROM \"YORUM\""
        cursor.execute(postgres_read)
        yazar = cursor.fetchall()
        return yazar
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")    

def get_kategori_details():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="bahadir",
                                      host="localhost",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        postgres_read = "SELECT * FROM \"KATEGORI\""
        cursor.execute(postgres_read)
        kategori = cursor.fetchall()
        return kategori
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")                    


if __name__ == "__main__":
    app.run(debug=True)
