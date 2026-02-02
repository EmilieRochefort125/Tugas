from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_zidane = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_zidane"
)

@app.route("/", methods=["GET", "POST"])
def transaksi_zidane():
    cursor = db_zidane.cursor(dictionary=True)

    if request.method == "POST":
        cursor.execute("""
            INSERT INTO transaksi_zidane
            (id_pasien_zidane, total_biaya_zidane, status_pembayaran_zidane, tgl_zidane)
            VALUES (%s,%s,%s,CURDATE())
        """, (
            request.form["id_pasien_zidane"],
            request.form["total_biaya_zidane"],
            request.form["status_pembayaran_zidane"]
        ))
        db_zidane.commit()
        return redirect("/")

    cursor.execute("""
        SELECT t.id_transaksi_zidane, p.nama_zidane,
               t.total_biaya_zidane, t.status_pembayaran_zidane, t.tgl_zidane
        FROM transaksi_zidane t
        JOIN pasien_zidane p ON t.id_pasien_zidane=p.id_pasien_zidane
    """)
    data = cursor.fetchall()

    cursor.execute("SELECT * FROM pasien_zidane")
    pasien = cursor.fetchall()

    return render_template("transaksi.html", data=data, pasien=pasien)


@app.route("/edit/<int:id>")
def edit(id):
    cursor = db_zidane.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transaksi_zidane WHERE id_transaksi_zidane=%s",(id,))
    transaksi = cursor.fetchone()
    cursor.execute("SELECT * FROM pasien_zidane")
    pasien = cursor.fetchall()
    return render_template("edit_transaksi.html", transaksi=transaksi, pasien=pasien)


@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    cursor = db_zidane.cursor()
    cursor.execute("""
        UPDATE transaksi_zidane SET
        id_pasien_zidane=%s,
        total_biaya_zidane=%s,
        status_pembayaran_zidane=%s
        WHERE id_transaksi_zidane=%s
    """, (
        request.form["id_pasien_zidane"],
        request.form["total_biaya_zidane"],
        request.form["status_pembayaran_zidane"],
        id
    ))
    db_zidane.commit()
    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    cursor = db_zidane.cursor()
    cursor.execute("DELETE FROM transaksi_zidane WHERE id_transaksi_zidane=%s",(id,))
    db_zidane.commit()
    return redirect("/")


@app.route("/pasien")
def pasien():
    cursor = db_zidane.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pasien_zidane")
    data = cursor.fetchall()
    return render_template("pasien.html", data=data)


@app.route("/pasien/pdf")
def pasien_pdf():
    cursor = db_zidane.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pasien_zidane")
    data = cursor.fetchall()
    return render_template("pasien_pdf.html", data=data)

@app.route("/transaksi/pdf")
def transaksi_pdf():
    cursor = db_zidane.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.id_transaksi_zidane, p.nama_zidane,
               t.total_biaya_zidane, t.status_pembayaran_zidane, t.tgl_zidane
        FROM transaksi_zidane t
        JOIN pasien_zidane p ON t.id_pasien_zidane=p.id_pasien_zidane
    """)
    data = cursor.fetchall()
    return render_template("transaksi_pdf.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
