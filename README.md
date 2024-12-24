# Sinkronisasi Database SQLite ke SQL Server

Script Python ini dirancang untuk menyinkronkan data dari database SQLite ke SQL Server. Script ini memastikan bahwa data yang sudah ada di SQL Server tidak akan diduplikasi, sementara data baru akan ditambahkan.

---

## Fitur Utama
1. **Koneksi Otomatis**: Menghubungkan ke database SQLite dan SQL Server.
2. **Pemeriksaan Duplikasi**: Memastikan data dengan kolom unik tertentu tidak diduplikasi di SQL Server.
3. **Penanganan Kolom Identity**: Mengabaikan kolom identity (auto increment) selama proses penyisipan.
4. **Logging Proses**: Memberikan laporan jumlah data yang disinkronkan.

---

## Prasyarat
1. **Python**: Versi 3.6 atau lebih baru.
2. **Pustaka Python**:
   - `sqlite3`
   - `pyodbc`
3. **ODBC Driver**: Pastikan driver ODBC untuk SQL Server terinstal (contoh: ODBC Driver 18 for SQL Server).
4. **Database SQLite**: Pastikan Anda memiliki file database SQLite yang valid.
5. **Hak Akses SQL Server**: Kredensial dengan hak akses untuk menyisipkan data ke tabel SQL Server.

---

## Instalasi

1. **Clone Repository**
   ```bash
   git clone https://github.com/username/repository-name.git
   cd repository-name
   ```

2. **Instal Dependensi**
   Pastikan Python dan pip telah terinstal. Jalankan:
   ```bash
   pip install pyodbc
   ```

3. **Sesuaikan Konfigurasi**
   Buka file Python dan sesuaikan bagian berikut:
   ```python
   # Konfigurasi SQL Server
   server = 'alamat_server_anda'
   database = 'nama_database_anda'
   username = 'username_anda'
   password = 'password_anda'
   ```

   Sesuaikan juga nama file SQLite:
   ```python
   sqlite_db_path = 'nama_file_sqlite.db'
   ```

4. **Jalankan Script**
   ```bash
   python script_name.py
   ```

---

## Cara Kerja

1. **Menghubungkan ke Database**:
   - Script akan menghubungkan ke database SQLite dan SQL Server menggunakan konfigurasi yang disediakan.

2. **Membaca Data dari SQLite**:
   - Data dari tabel yang ditentukan di SQLite akan dibaca.

3. **Pemeriksaan dan Penyisipan Data**:
   - Script memeriksa apakah data sudah ada di SQL Server menggunakan kolom unik yang ditentukan.
   - Data baru akan ditambahkan ke SQL Server, sementara data yang sudah ada akan dilewati.

4. **Logging Hasil**:
   - Jumlah data yang ditambahkan akan dicetak ke konsol.

---

## Struktur Tabel yang Dibutuhkan

**Contoh Tabel SQL Server:**

1. **Tabel `customer`**
   ```sql
   CREATE TABLE customer (
       customer_auto_id INT IDENTITY(1,1) PRIMARY KEY,
       customer_no NVARCHAR(50) UNIQUE,
       customer_name NVARCHAR(100),
       ... -- kolom lainnya
   );
   ```

2. **Tabel `test_results`**
   ```sql
   CREATE TABLE test_results (
       test_results_auto_id INT IDENTITY(1,1) PRIMARY KEY,
       test_results_no NVARCHAR(50) UNIQUE,
       result_value NVARCHAR(100),
       ... -- kolom lainnya
   );
   ```

---

## Laporan Output
Contoh hasil output dari script:
```
--------------------------------------------------
          MCU: Database Sync by RizkyKR
--------------------------------------------------
Menghubungkan database:
   Berhasil terhubung ke SQLite.
   Berhasil terhubung ke SQL Server.

Sinkronisasi Data:
   customer (SQLite) to customer (MSSQL)
   Jumlah data di tabel customer: 150
      10 data baru berhasil ditambahkan.

   test_results (SQLite) to test_results (MSSQL)
   Jumlah data di tabel test_results: 1269
      25 data baru berhasil ditambahkan.
--------------------------------------------------
Proses selesai!
--------------------------------------------------
```

---

## Kontak
Untuk informasi lebih lanjut atau bantuan, silakan hubungi:
**Email**: [me@rizkykr.com](mailto:me@rizkykr.com)

---

## Lisensi
Script ini dilisensikan di bawah [MIT License](LICENSE).
