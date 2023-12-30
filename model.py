import pymysql

class Database:
    def connect (self):

        return pymysql.connect(host="localhost", user="root", password="", database="uts_kelompok6_carrental")
    
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
    