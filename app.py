from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # diperlukan untuk flash message

# Konfigurasi koneksi database Railway
app.config['MYSQL_HOST'] = 'shinkansen.proxy.rlwy.net'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'BzUobQyvRWDoeVzGQpDIvsRpdkfwqIns'
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_PORT'] = 58092
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # biar fetchall jadi dict
# app.config['MYSQL_CHARSET'] = 'utf8mb4'  # opsional, kalau ada masalah encoding

mysql = MySQL(app)

# Route untuk membuat tabel sekali saja
@app.route('/create_table')
def create_table():
    try:
        with mysql.connection.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    email VARCHAR(100)
                )
            ''')
            mysql.connection.commit()
        return "Tabel berhasil dibuat!"
    except Exception as e:
        return f"Error saat membuat tabel: {str(e)}"

# Home, tampilkan semua data users
@app.route('/')
def index():
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
    return render_template('index.html', users=users)

# Form tambah data
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        # Validasi sederhana
        if not name or not email:
            flash("Nama dan Email harus diisi!")
            return redirect('/add')

        try:
            with mysql.connection.cursor() as cur:
                cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
                mysql.connection.commit()
            flash("Data berhasil ditambahkan!")
            return redirect('/')
        except Exception as e:
            flash(f"Error saat menambahkan data: {str(e)}")
            return redirect('/add')

    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
