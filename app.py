from flask import Flask, render_template, request, redirect, url_for
import psycopg2

def get_yayinevi_details():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="password",
                                      host="127.0.0.1",
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


def add_yayinevi(id, name):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="password",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
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


def delete_yayinevi(id):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="password",
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


def search_yayinevi(search_word):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="password",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        postgres_read = "SELECT * FROM \"YAYINEVI\" WHERE CAST(\"Yayinevi_Id\" as text) LIKE %(par)s or LOWER(\"Yayinevi_Ismi\") LIKE %(par)s "
        cursor.execute(postgres_read, dict(par='%'+search_word+'%'))
        yorum = cursor.fetchall()
        return yorum
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
                                      password="password",
                                      host="127.0.0.1",
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


def add_yazar(id, name, surname):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="password",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
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


def delete_yazar(id):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="password",
                                      host="127.0.0.1",
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


def search_yazar(search_word):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="password",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        postgres_read = "SELECT * FROM \"YAZAR\" WHERE CAST(\"Yazar_Id\" as text) LIKE %(par)s or LOWER(\"Yazar_Ismi\") LIKE %(par)s or LOWER(\"Yazar_Soyismi\") LIKE %(par)s"
        cursor.execute(postgres_read, dict(par='%'+search_word+'%'))
        yorum = cursor.fetchall()
        return yorum
    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def delete_yorum(id):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="password",
                                      host="127.0.0.1",
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


def get_yorum_details():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="password",
                                      host="127.0.0.1",
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


def search_yorum(name):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="password",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        postgres_read = "SELECT * FROM \"YORUM\" WHERE CAST(\"Yorum_Id\" as text) LIKE %(par)s or LOWER(\"Yorum_Icerigi\") LIKE %(par)s "
        cursor.execute(postgres_read, dict(par='%'+name+'%'))
        yorum = cursor.fetchall()
        return yorum
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
                                      password="password",
                                      host="127.0.0.1",
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


def add_kategori(id, name):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="password",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
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


def delete_kategori(id):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="password",
                                      host="127.0.0.1",
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


def search_kategori(name):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="password",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="takebook_db")
        cursor = connection.cursor()
        postgres_read = "SELECT * FROM \"KATEGORI\" WHERE CAST(\"Kategori_Id\" as text) LIKE %(par)s or LOWER(\"Kategori_Ismi\") LIKE %(par)s "
        cursor.execute(postgres_read, dict(par='%'+name+'%'))
        kategori = cursor.fetchall()
        return kategori
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


@app.route("/yayinevi_ekle", methods=['POST'])
def yayinevi_ekle():
    id = request.form.get("yayinevi_id")
    name = request.form.get("yayinevi_ismi")
    add_yayinevi(id, name)
    return redirect(url_for("yayinevi_crud"))


@app.route("/delete_yayinevi/<string:id>")
def yayinevi_sil(id):
    delete_yayinevi(id)
    return redirect(url_for("yayinevi_crud"))


@app.route("/yazar_ekle", methods=['POST'])
def yazar_ekle():
    id = request.form.get("yazar_id")
    name = request.form.get("yazar_ismi")
    surname = request.form.get("yazar_soyismi")
    add_yazar(id, name, surname)
    return redirect(url_for("yazar_crud"))


@app.route("/delete_yazar/<string:id>")
def yazar_sil(id):
    delete_yazar(id)
    return redirect(url_for("yazar_crud"))


@app.route("/delete_yorum/<string:id>")
def yorum_sil(id):
    delete_yorum(id)
    return redirect(url_for("yorum_crud"))


@app.route("/yorum_ara", methods=["POST"])
def yorum_ara():
    aranacak = request.form.get("search_word")
    return render_template("yorum_crud.html", yorumlar=search_yorum(aranacak))


@app.route("/yayinevi_ara", methods=["POST"])
def yayinevi_ara():
    aranacak = request.form.get("search_word")
    return render_template("yayinevi_crud.html", yayinevleri=search_yayinevi(aranacak))


@app.route("/yazar_ara", methods=["POST"])
def yazar_ara():
    aranacak = request.form.get("search_word")
    return render_template("yazar_crud.html", yazarlar=search_yazar(aranacak))


@app.route("/kategori_ekle", methods=['POST'])
def kategori_ekle():
    id = request.form.get("kategori_id")
    name = request.form.get("kategori_ismi")
    add_kategori(id, name)
    return redirect(url_for("kategori_crud"))


@app.route("/delete_kategori/<string:id>")
def kategori_sil(id):
    delete_kategori(id)
    return redirect(url_for("kategori_crud"))


@app.route("/kategori_ara", methods=["POST"])
def kategori_ara():
    aranacak = request.form.get("search_word")
    return render_template("kategori_crud.html", kategoriler=search_kategori(aranacak))


if __name__ == "__main__":
    app.run(debug=True)
