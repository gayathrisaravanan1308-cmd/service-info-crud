from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

def get_db():
    return pymysql.connect(host="localhost", user="root", password="YOUR_PASSWORD", database="qrCode", cursorclass=pymysql.cursors.Cursor)

# 1. LISTING + FILTERS
@app.route("/")
def index():
    db = get_db()
    cur = db.cursor()
    q = "SELECT * FROM serviceInfo WHERE 1=1"
    if request.args.get("location"):
        q += f" AND locationName='{request.args.get('location')}'"
    if request.args.get("region"):
        q += f" AND regionName='{request.args.get('region')}'"
    if request.args.get("status"):
        q += f" AND status='{request.args.get('status')}'"
    q += " ORDER BY id DESC"
    cur.execute(q)
    data = cur.fetchall()
    db.close()
    return render_template("index.html", rows=data)

# 2. ADD
@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        db = get_db(); cur = db.cursor()
        cur.execute("INSERT INTO serviceInfo (name,email,phoneNumber,productType,issueDescription,locationName,regionName,status,remarks) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (request.form['name'], request.form['email'], request.form['phone'], request.form['product'], request.form['issue'], request.form['location'], request.form['region'], request.form['status'], request.form['remarks']))
        db.commit(); db.close()
        return redirect("/")
    return render_template("add.html")

# 3. EDIT
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):
    db = get_db(); cur = db.cursor()
    if request.method == "POST":
        cur.execute("UPDATE serviceInfo SET name=%s,email=%s,phoneNumber=%s,productType=%s,issueDescription=%s,locationName=%s,regionName=%s,status=%s,remarks=%s WHERE id=%s",
        (request.form['name'], request.form['email'], request.form['phone'], request.form['product'], request.form['issue'], request.form['location'], request.form['region'], request.form['status'], request.form['remarks'], id))
        db.commit(); db.close()
        return redirect("/")
    cur.execute("SELECT * FROM serviceInfo WHERE id=%s", (id,))
    row = cur.fetchone(); db.close()
    return render_template("edit.html", r=row)

# 4. DELETE
@app.route("/delete/<int:id>")
def delete(id):
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM serviceInfo WHERE id=%s", (id,))
    db.commit(); db.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)