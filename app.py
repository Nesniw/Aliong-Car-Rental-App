import os
import logging
logging.basicConfig(level=logging.DEBUG)
from flask import Flask, render_template, request, flash, redirect, session
from datetime import date, datetime, timedelta
app = Flask(__name__)
from model import Database
app.secret_key = '@#$123456&*()'
app.config['UPLOAD_FOLDER'] = 'static/upload_images'
db = Database()

@app.route('/')
def index():

    return render_template('index.html', homeactive=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form['password'] == request.form['konfirmasi']:
            if db.checkuser(request.form):
                if db.tambahuser(request.form):
                    flash('Akun berhasil dibuat. Silahkan login.')
                    return redirect('/login')
                else:
                    flash('Akun gagal dibuat. Tolong ulangi registrasi')
                    return redirect('/register')
            else:
                flash('Username yang dimasukkan sudah terdaftar, coba buat username lain')
                return redirect('/register')
        else:
            flash('Password yang Anda masukan tidak cocok')
            return redirect('/register')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if db.checklogin(request.form):
            username = request.form['username']

            user_role = db.get_user_role(username)

            session['username'] = username
            session['roles'] = user_role

            return redirect('/')
        else:
            flash('Username atau Password salah')
            return redirect('/login')
        
    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/about')
def about():

    return render_template('about.html', aboutactive=True)

@app.route('/services')
def services():

    return render_template('services.html', servicesactive=True)

@app.route('/contact')
def contact():

    return render_template('contact.html', contactactive=True)


@app.route('/details/<int:id>')
def details(id):
    session['idmobil'] = id
    return redirect('/detailcar')

@app.route('/detailcar')
def detailcar():

    id = session['idmobil']
    data_mobil = db.read(id)
    return render_template('detailcar.html', caractive=True, data_mobil=data_mobil)

@app.route('/displaycardata')
def displaycardata():
    data = db.read(None)
    return render_template('datacar.html', managecaractive = True, data=data)


@app.route('/createmobil', methods=['GET', 'POST'])
def createmobil():
    if request.method == 'POST':
        # Cek 'file1' ada atau tidak
        if 'file1' not in request.files:
            flash("File tidak ditemukan")
        else:
            file1 = request.files['file1']
            # Cek apakah nama file kosong
            if file1.filename == '':
                flash("File name is empty")
            else:
                # Ambil data dari form
                data = {
                    'nama_mobil': request.form['nama_mobil'],
                    'brand_mobil': request.form['brand_mobil'],
                    'kilometer': request.form['kilometer'],
                    'transmisi': request.form['transmisi'],
                    'kapasitas_mobil': request.form['kapasitas_mobil'],
                    'jenis_bensin': request.form['jenis_bensin'],
                    'harga' : request.form['harga'],
                    'deskripsi': request.form['deskripsi']
                }

                # Urusan file upload
                if file1:
                    # Menentukan path yang dipake untuk nyimpan file gambar
                    path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], file1.filename)
                    # Simpan file sesuai path yang dibuat
                    file1.save(path)
                    data['gambar'] = file1.filename  # masukin filename ke atribut gambar di database nanti

                # Masukin data ke database
                if db.insert(data):
                    flash("Data berhasil dimasukkan")
                else:
                    flash("Data gagal dimasukkan")

    return render_template('creatembl.html', managecaractive=True)

@app.route('/readcatalog')
def readcatalog():
    data = db.read_available_cars()
    return render_template('car.html', caractive=True, data=data)

@app.route('/deletemobil/<int:id>')
def deletemobil(id):
    # Ambil image filename lama yang mau dihapus
    file_name = db.get_image_filename(id)
    if db.delete(id):
        flash('Data berhasil di delete')
        if file_name:
            file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
        return redirect('/readcatalog')
    else:
        flash('Data gagal di delete')
        return redirect('/readcatalog')
    
@app.route('/editmobil/<int:id>')
def editmobil(id):
    session['idmobil'] = id
    return redirect('/edit')

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    id = session['idmobil']
    data_mobil = db.read(id)
    
    if request.method == 'POST':
        # Ambil image filename yang lama
        existing_image_filename = db.get_image_filename(id)
        
        # Cek 'file1' ada atau enggak di request.file
        if 'file1' in request.files:
            file1 = request.files['file1']
            # Cek apakah ada file gambar yang baru
            if file1.filename != '':
                # Simpan file gambar yang baru
                path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], file1.filename)
                file1.save(path)
                new_image_filename = file1.filename
                
                # Update data dengan file gambar baru
                data = {
                    'gambar': new_image_filename,
                    'nama_mobil': request.form['nama_mobil'],
                    'brand_mobil': request.form['brand_mobil'],
                    'kilometer': request.form['kilometer'],
                    'transmisi': request.form['transmisi'],
                    'kapasitas_mobil': request.form['kapasitas_mobil'],
                    'jenis_bensin': request.form['jenis_bensin'],
                    'harga' : request.form['harga'],
                    'deskripsi': request.form['deskripsi']
                }
                
                # Hapus image sebelumnya kalau masih tersimpan
                if existing_image_filename:
                    existing_image_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], existing_image_filename)
                    if os.path.exists(existing_image_path):
                        os.remove(existing_image_path)
            else:
                # Kalau tidak ada file baru, update data tanpa mengubah file
                data = {
                    'nama_mobil': request.form['nama_mobil'],
                    'brand_mobil': request.form['brand_mobil'],
                    'kilometer': request.form['kilometer'],
                    'transmisi': request.form['transmisi'],
                    'kapasitas_mobil': request.form['kapasitas_mobil'],
                    'jenis_bensin': request.form['jenis_bensin'],
                    'harga' : request.form['harga'],
                    'deskripsi': request.form['deskripsi']
                }

            # Update data di database
            if db.edit(id, data):
                flash('Data berhasil di update')
                return redirect('/readcatalog')
            else:
                flash('Data gagal di update')
                return redirect('/readcatalog')

    return render_template('edit.html', data_mobil=data_mobil)


# Belum kepakai nanti tunggu UAS
@app.route('/loginpage', methods=['GET', 'POST'])
def loginpage():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        return render_template('loginSuccess.html', firstname=firstname, lastname=lastname, email=email, password=password)

    return render_template('loginPage.html')

@app.route('/pilihmobil/<int:id>')
def pilihmobil(id):
    session['idmobil'] = id
    return redirect('/booking')

@app.route('/booking', methods=['GET','POST'])
def pinjam():
    if request.method == 'POST':
        try:
            # Ambil data dari formulir
            tanggalpinjam = request.form['tanggalpinjam']
            lamapinjam = int(request.form['lamapinjam'])  # Pastikan lamapinjam diubah menjadi integer

            # Ambil informasi mobil yang dipilih
            id_mobil = session.get('idmobil')  # Ambil id mobil dari session

            # Lakukan proses booking
            success, estimasikembali = db.book_car(id_mobil, session['username'], tanggalpinjam, lamapinjam)

            if success:
                flash(f'Booking berhasil! Mobil dapat diambil pada tanggal {tanggalpinjam} dan dikembalikan pada tanggal {estimasikembali}')
                return redirect('/readcatalog')
            else:
                flash(f'Booking gagal. {estimasikembali}')
                return redirect('/readcatalog')

        except Exception as e:
            flash(f'Error: {str(e)}')
            return redirect('/readcatalog')
        
    # Calculate the maximum date (today + 5 days)
    max_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')

    # Jika metode adalah GET, tampilkan halaman pilihan mobil dengan formulir booking
    return render_template('bookcar.html', min_date_today=date.today(), max_date=max_date)


@app.route('/confirmreturn')
def confirmreturn():
    
    konfirmasi_booking = db.read_konfirmasi_booking()
    return render_template('confirm-return.html', carbookactive=True, konfirmasi_booking=konfirmasi_booking)

@app.route('/complete_booking/<int:id_booking>')
def complete_booking(id_booking):

    success = db.update_booking(id_booking)

    if success:
        logging.info(f'Successfully completed booking with ID: {id_booking}')
        flash(f'Pengembalian mobil dengan ID Booking  {id_booking} telah dikonfirmasi.')
    else:
        logging.error('Failed to complete booking.')
        flash('Failed to complete booking.')

    return redirect('/confirmreturn')


if __name__ == '__main__':
    app.run(debug = True)