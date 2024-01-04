import pymysql
from datetime import date, datetime, timedelta

class Database:
    def connect (self):

        return pymysql.connect(host="localhost", user="root", password="", database="uas_kelompok6_carrental")
    
    def read(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            if id == None:
                cursor.execute("SELECT * FROM data_mobil")
            else:
                cursor.execute("SELECT * FROM data_mobil where id_mobil = %s", (id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def insert(self, data):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO data_mobil(gambar, nama_mobil, brand_mobil, kilometer, transmisi, kapasitas_mobil, jenis_bensin, harga, deskripsi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                           (data['gambar'], data['nama_mobil'], data['brand_mobil'], data['kilometer'], data['transmisi'], data['kapasitas_mobil'], data['jenis_bensin'], data['harga'],  data['deskripsi'],))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def get_image_filename(self, id):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute("SELECT gambar FROM data_mobil WHERE id_mobil = %s", (id,))
            result = cursor.fetchone()
            if result:
                return result[0]  # Kembaliin filename dari gambar
            else:
                return None
        except:
            return None
        finally:
            con.close()

    def delete(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM data_mobil WHERE id_mobil = %s",(id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def edit(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("UPDATE data_mobil SET gambar = %s, nama_mobil = %s, brand_mobil = %s, kilometer = %s, transmisi = %s, kapasitas_mobil = %s, jenis_bensin = %s, harga = %s, deskripsi = %s WHERE id_mobil = %s", 
                           (data['gambar'], data['nama_mobil'], data['brand_mobil'], data['kilometer'], data['transmisi'], data['kapasitas_mobil'], data['jenis_bensin'], data['harga'], data['deskripsi'], id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def checklogin(self, data):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM user where username = %s and password = %s',(data['username'],data['password'],))
            if len(cursor.fetchall()) != 0:
                return True
            else:
                return False
        except:
            return False
        finally:
            con.close()

    def get_user_role(self, username):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute("SELECT roles FROM user WHERE username = %s", (username,))
            result = cursor.fetchone()
            if result:
                return result[0]  # Return the user's role
            else:
                return None
        except:
            return None
        finally:
            con.close()

    def checkuser(self, data):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('SELECT * FROM user where username = %s',(str(data['username']),))
            if len(cursor.fetchall()) == 0:
                return True
            else:
                return False
        except:
            return False
        finally:
            con.close()

    def tambahuser(self, data):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute('INSERT INTO user(nama_lengkap, email, username, password, roles) VALUES(%s, %s, %s, %s, %s)',
                                (data['nama_lengkap'], data['email'], data['username'], data['password'], data['roles'],))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def read_available_cars(self):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM data_mobil WHERE status = 'Tersedia'")
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def book_car(self, id_mobil, username, tanggalpinjam, lamapinjam):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            # Cek apakah mobil sudah dibooking pada tanggal tersebut
            cursor.execute("SELECT * FROM booking_mobil WHERE id_mobil = %s AND tanggalpinjam = %s", (id_mobil, tanggalpinjam))
            existing_booking = cursor.fetchone()

            if existing_booking:
                return False, "Mobil telah dipinjam untuk hari tersebut."

            # Hitung tanggal estimasi pengembalian berdasarkan tanggal pinjam dan lama pinjam
            tanggalpinjam_obj = datetime.strptime(tanggalpinjam, "%Y-%m-%d")
            estimasikembali = tanggalpinjam_obj + timedelta(days=lamapinjam - 1)

            # Ambil harga dari mobil yang dipilih
            cursor.execute("SELECT harga FROM data_mobil WHERE id_mobil = %s", (id_mobil,))
            harga_mobil = cursor.fetchone()[0]

            # Lakukan booking dengan menambahkan data ke tabel booking_mobil
            cursor.execute("INSERT INTO booking_mobil (id_mobil, username, tanggalpinjam, lamapinjam, estimasikembali, harga, status_booking) VALUES (%s, %s, %s, %s, %s, %s, 'Dipesan')",
                       (id_mobil, username, tanggalpinjam, lamapinjam, estimasikembali, harga_mobil))
            
            cursor.execute("UPDATE data_mobil SET status = 'Dipinjam' WHERE id_mobil = %s", (id_mobil,))
            
            con.commit()
            return True, estimasikembali.strftime("%Y-%m-%d")

        except Exception as e:
            con.rollback()
            return False, str(e)

        finally:
            con.close()


    def read_konfirmasi_booking(self):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM booking_mobil WHERE status_booking = 'Dipesan'")
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def update_booking(self, id_booking):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            
            tanggalkembali = date.today()

            cursor.execute("SELECT estimasikembali, harga, lamapinjam, id_mobil FROM booking_mobil WHERE id_booking = %s", (id_booking,))
            estimasi_kembali, harga_mobil, lamapinjam, id_mobil = cursor.fetchone()
            
            # Menghitung selisih hari
            selisihhari = tanggalkembali.toordinal() - estimasi_kembali.toordinal()

            # Menghitung denda
            denda = max(0, selisihhari) * 500000

            # Menghitung total biaya
            total_biaya = (harga_mobil * lamapinjam) + denda

            # Update status dan tanggal kembali
            cursor.execute("UPDATE booking_mobil SET status_booking = 'Selesai', tanggalkembali = %s, selisih_hari = %s, denda = %s, totalbiaya = %s WHERE id_booking = %s", (tanggalkembali, selisihhari, denda, total_biaya, id_booking))

            # Update status di data_mobil
            cursor.execute("UPDATE data_mobil SET status = 'Tersedia' WHERE id_mobil = %s", (id_mobil,))
            con.commit()

            return True
        except Exception as e:
            con.rollback()
            return False, str(e)
        finally:
            con.close()

    def read_mybooking(self, username):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM booking_mobil WHERE username = %s", (username,))
            return cursor.fetchall()
        except Exception as e:
            print("Error:", e)
            return ()
        finally:
            con.close()

    def read_bookinglist(self):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM booking_mobil")
            return cursor.fetchall()
        except Exception as e:
            print("Error:", e)
            return ()
        finally:
            con.close()
            
            
    