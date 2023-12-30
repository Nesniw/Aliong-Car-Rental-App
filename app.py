import os
from flask import Flask, render_template, request, flash, redirect, session
app = Flask(__name__)
from model import Database
app.secret_key = '@#$123456&*()'
app.config['UPLOAD_FOLDER'] = 'static/upload_images'
db = Database()

@app.route('/')
def index():

    return render_template('index.html', homeactive=True)

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

    return render_template('creatembl.html', createactive=True)

@app.route('/readcatalog')
def readcatalog():
    data = db.read(None)
    return render_template('car.html', caractive = True, data=data)

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

if __name__ == '__main__':
    app.run(debug = True)