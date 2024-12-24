import sqlite3
import pyodbc
import logging

# Set up logging
logging.basicConfig(filename='sync_errors.log', level=logging.ERROR)

# Fungsi untuk menghubungkan ke SQLite
def connect_to_sqlite(db_path):
    conn = sqlite3.connect(db_path)
    print("   Berhasil terhubung ke SQLite.")
    return conn

# Fungsi untuk menghubungkan ke SQL Server
def connect_to_sql_server():
    server = '202.162.194.91'  # Host SQL Server Anda
    database = 'DatabaseAudiometri'  # Nama database Anda
    username = 'laptopaudiometri'  # Username SQL Server Anda
    password = 'audio12345'  # Password SQL Server Anda
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 18 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password};'
        f'Encrypt=yes;'
        f'TrustServerCertificate=yes;'
    )
    print("   Berhasil terhubung ke SQL Server.")
    return conn

# Fungsi untuk mendapatkan data dari SQLite
def get_sqlite_data(sqlite_conn, table_name):
    cursor = sqlite_conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    return data

# Fungsi untuk mendapatkan semua nilai unik yang sudah ada di SQL Server
def get_existing_values(sql_server_conn, table_name, unique_column):
    cursor = sql_server_conn.cursor()
    cursor.execute(f"SELECT {unique_column} FROM {table_name}")
    existing_values = set(row[0] for row in cursor.fetchall())
    return existing_values

# Fungsi untuk menyisipkan data ke tabel SQL Server, mengabaikan kolom identity
def insert_data_to_sql_server(sql_server_conn, table_name, columns, data, identity_column, unique_column):
    existing_values = get_existing_values(sql_server_conn, table_name, unique_column)
    cursor = sql_server_conn.cursor()

    # Hapus kolom identity (auto increment) dari kolom yang akan diinsert
    columns_without_identity = [col for col in columns if col != identity_column]

    # Menyiapkan placeholder untuk nilai yang akan diinsert
    placeholders = ', '.join(['?' for _ in columns_without_identity])
    column_names = ', '.join(columns_without_identity)
    
    insert_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
    
    new_data_count = 0
    batch_data = []  # Untuk menampung data sebelum di-insert dalam batch
    for row in data:
        # Pastikan unique_column ada dalam kolom SQLite
        if unique_column not in columns:
            print(f"Kolom {unique_column} tidak ditemukan di tabel {table_name}.")
            continue
        
        unique_value = row[columns.index(unique_column)]
        
        # Cek apakah data dengan unique value sudah ada di SQL Server
        if unique_value not in existing_values:
            # Simpan row ke batch_data
            batch_data.append([row[columns.index(col)] for col in columns_without_identity])
            existing_values.add(unique_value)  # Tambahkan value ke set untuk cek duplikasi selanjutnya
            new_data_count += 1

            # Batasi jumlah data dalam batch (misalnya 1000 baris) untuk menghindari penggunaan memori berlebihan
            if len(batch_data) >= 1000:
                try:
                    cursor.executemany(insert_query, batch_data)
                    sql_server_conn.commit()
                except pyodbc.Error as e:
                    logging.error(f"Error saat menambahkan data ke tabel {table_name}: {e}")
                batch_data = []  # Kosongkan batch_data setelah commit
    
    # Insert sisa data yang belum ter-commit
    if batch_data:
        try:
            cursor.executemany(insert_query, batch_data)
            sql_server_conn.commit()
        except pyodbc.Error as e:
            logging.error(f"Error saat menambahkan data ke tabel {table_name}: {e}")
    
    print(f"   {new_data_count} data baru berhasil ditambahkan.\n")

# Fungsi utama untuk menjalankan proses
def main():
    try:
        print("\n" + "="*50)
        print("          MCU: Database Sync by RizkyKR")
        print("="*50)

        sqlite_db_path = 'AM33.db'  # Nama file SQLite yang telah Anda tentukan
        sqlite_tables = ['customer', 'test_results']  # Nama tabel SQLite yang akan diduplikasi
        sql_server_tables = ['customer', 'test_results']  # Nama tabel SQL Server yang akan diisi
        
        # Kolom unik yang akan dicek untuk menghindari duplikasi
        unique_columns = {
            'customer': 'customer_no',  # Kolom unik untuk tabel 'customer'
            'test_results': 'test_results_no'  # Kolom unik untuk tabel 'test_results'
        }

        # Kolom identity untuk setiap tabel
        identity_columns = {
            'customer': 'customer_auto_id',
            'test_results': 'test_results_auto_id'
        }

        # Koneksi ke SQLite dan SQL Server
        print("Menghubungkan database:")
        sqlite_conn = connect_to_sqlite(sqlite_db_path)
        sql_server_conn = connect_to_sql_server()

        print("\nSinkronisasi Data:")
        # Proses penyalinan data
        for sqlite_table, sql_server_table in zip(sqlite_tables, sql_server_tables):
            print(f"   {sqlite_table} (SQLite) to {sql_server_table} (MSSQL)")

            # Ambil data dari tabel SQLite
            sqlite_data = get_sqlite_data(sqlite_conn, sqlite_table)
            print(f"   Jumlah data di tabel {sqlite_table}: {len(sqlite_data)}")

            # Ambil nama kolom dari SQLite
            sqlite_columns = [col[1] for col in sqlite_conn.execute(f"PRAGMA table_info({sqlite_table})")]

            # Sisipkan data ke SQL Server hanya jika data belum ada
            insert_data_to_sql_server(
                sql_server_conn,
                sql_server_table,
                sqlite_columns,
                sqlite_data,
                identity_columns[sqlite_table],
                unique_columns[sqlite_table]
            )

    finally:
        # Pastikan koneksi ditutup meskipun ada error
        sqlite_conn.close()
        sql_server_conn.close()
        print("="*50)
        print("Proses selesai!")
        print("="*50)

if __name__ == '__main__':
    main()
