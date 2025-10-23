# JamaAlca
JamaAlca is an AI Powered Farming App

## Setup

- Install dependencies:

```powershell
pip install -r requirements.txt
```

- If you want Azure SQL persistence, set the `AZURE_SQL_CONN` environment variable to a valid pyodbc connection string. Example (PowerShell):

```powershell
$env:AZURE_SQL_CONN = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=<your_server>;DATABASE=<your_db>;UID=<user>;PWD=<password>;Encrypt=yes;TrustServerCertificate=no;'
```

Expected database tables (example):

- `Users` table with columns: `id` (INT PRIMARY KEY, IDENTITY), `name`, `phone`, `location`, `farm_size`, `main_crop`.
- `Scans` table with columns: `id` (NVARCHAR(50) PRIMARY KEY), `user_id` (INT), `crop` (NVARCHAR(50)), `disease` (NVARCHAR(200)), `confidence` (FLOAT), `treatment` (NVARCHAR(MAX)), `image_path` (NVARCHAR(500)), `created_at` (DATETIME).

The app will save images locally under `./scans/` and will attempt to insert metadata into the `Scans` table when `AZURE_SQL_CONN` is configured.

## Run

```powershell
python .\jamaalca.py
```

## Notes
- For production consider uploading images to Azure Blob Storage and storing blob URLs in the database instead of local file paths.
- The project currently contains a placeholder user flow (no authentication). When a profile is saved the app will try to upsert the user into the `Users` table and use the returned id for scans.
