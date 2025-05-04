# Database Backup CLI Tool

## Overview

This command-line interface (CLI) tool allows you to back up various types of databases (MySQL, PostgreSQL, MongoDB, SQLite) efficiently. It supports automatic backup scheduling, compression of backup files, storage options (local and cloud), and logging of backup activities.

The tool also includes restore functionality for recovering databases from backups.

---

## Features

* **Database Connectivity**:

  * Supports MySQL, PostgreSQL, MongoDB, SQLite.
  * Allows specifying connection parameters (host, port, username, password, and database name).
  * Validates credentials for each DBMS before proceeding with backup operations.

* **Backup Operations**:

  * Supports full, incremental, and differential backup types.
  * Compresses backup files using gzip to reduce storage space.

* **Storage Options**:

  * Backup files can be stored locally or on cloud services like AWS S3, Google Cloud Storage, or Azure Blob Storage.

* **Logging & Notifications**:

  * Logs backup operations, including timestamps, status, and errors.
  * Optionally send Slack notifications on completion of backup operations.

* **Restore Operations**:

  * Restore operations to recover databases from backups.
  * Selective restore of specific tables or collections if supported by DBMS.

---

## Installation

### Prerequisites

* Python 3.6+
* Required Python libraries (`subprocess`, `pyyaml`, `gzip`, `shutil`, `tarfile`).

### 1. Clone the repository

```bash
git clone https://github.com/peymansohi/backup-utility.git
cd db-backup-cli
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

### `config.yaml`

You need to configure the connection settings for your databases. Example:

```yaml
mysql:
  host: localhost
  port: 3306
  username: root
  password: rootpass
  database: mydb

postgres:
  host: localhost
  port: 5432
  username: postgres
  password: pgpass
  database: mydb

mongodb:
  host: localhost
  port: 27017
  username: myuser
  password: mypass
  auth_db: admin
  database: mydb

sqlite:
  db_path: ./mydatabase.sqlite
```

---

## Usage

### Backup

To back up a database, use the following command:

```bash
python cli.py backup --db-type <db_type>
```

Where `<db_type>` can be:

* `mysql`
* `postgres`
* `mongodb`
* `sqlite`

Example:

```bash
python cli.py backup --db-type mysql
```

This will back up the database as specified in the `config.yaml` file. The backup will be compressed and saved in the current directory with a timestamped filename.

### Restore

To restore a backup, use the following command:

```bash
python cli.py restore --db-type <db_type> --backup-file <backup_filename>
```

Example:

```bash
python cli.py restore --db-type mysql --backup-file mysql_backup_20230503.sql.gz
```

This command will restore the database from the specified backup file.

### Logging

The tool logs all backup activities in the `logs/backup.log` file. Logs will include the start time, end time, status, errors, and the time taken for each backup.

---

## Cloud Storage Integration (Optional)

For cloud storage integration (AWS S3, Google Cloud Storage, Azure), you can modify the `backup` scripts to add cloud upload functionality. The required libraries for cloud storage must be installed (e.g., `boto3` for AWS S3).

---

## Example Output

```bash
Starting PostgreSQL backup for database 'mydb'
Backup completed and compressed to postgres_backup_20230503_102030.sql.gz
```

### Error Example:

```bash
Error during pg_dump: Could not connect to server: Connection refused
```

---

## Advanced Features

### Automatic Scheduling

You can set up automatic backups using cron jobs (Linux/macOS) or Task Scheduler. For example, to schedule backups daily at 3 AM:

#### (`crontab`):

```bash
0 3 * * * /usr/bin/python3 cli.py backup --db-type mysql
```

### Notifications (Slack)

You can configure the tool to send a Slack notification after each backup operation by modifying the `backup` script to include Slack API integration (using the `requests` library).

---

