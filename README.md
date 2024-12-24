# MCU Database Sync by RizkyKR

This script facilitates the synchronization of data between a local SQLite database and a Microsoft SQL Server database, ensuring only new records are added to the target tables.

## Features
- Supports syncing multiple tables.
- Checks for duplicate records before insertion using a unique column.
- Handles identity columns during data insertion.
- Provides detailed logs of the synchronization process.

## Requirements
- Python 3.8+
- SQLite database file (`AM33.db`).
- Microsoft SQL Server.

## Dependencies
Install the required Python packages using pip:

```bash
pip install pyodbc
```

## Configuration

### SQLite Configuration
Ensure your SQLite database file (`AM33.db`) is placed in the same directory as the script or provide the correct path in the `sqlite_db_path` variable.

### SQL Server Configuration
Update the SQL Server connection details in the `connect_to_sql_server` function:

```python
server = 'hostname'  # Host SQL Server Anda
database = 'database'  # Nama database Anda
username = 'username'  # Username SQL Server Anda
password = 'password'  # Password SQL Server Anda
```

### Table and Column Mapping
Define the tables to be synchronized and their column mappings in the `main` function:

```python
sqlite_tables = ['customer', 'test_results']
sql_server_tables = ['customer', 'test_results']

unique_columns = {
    'customer': 'customer_no',
    'test_results': 'test_results_no'
}

identity_columns = {
    'customer': 'customer_auto_id',
    'test_results': 'test_results_auto_id'
}
```

## How to Use

1. Place the script and SQLite database file (`AM33.db`) in the same directory.
2. Update the configuration as per your database setup.
3. Run the script:

```bash
python sync_script.py
```

4. Monitor the console output for synchronization progress and logs.

## Desktop Shortcut (Optional)

You can create a desktop shortcut for the script to run it directly:

1. Save the script as `sync_script.py`.
2. Create a batch file (`sync_script.bat`) with the following content:

   ```bat
   @echo off
   pythonw "path\to\sync_script.py"
   pause
   ```

3. Create a shortcut to `sync_script.bat` and place it on your desktop.

## Logs

The script provides detailed logs for:
- Successful connections to SQLite and SQL Server.
- Number of records processed for each table.
- Errors encountered during data insertion.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
