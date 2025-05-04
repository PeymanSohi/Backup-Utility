import subprocess
import datetime
import gzip
import os
import yaml

def load_config():
    with open("config.yaml", 'r') as file:
        return yaml.safe_load(file)

def backup():
    config = load_config()
    mysql_cfg = config.get("mysql", {})
    
    host = mysql_cfg.get("host")
    port = mysql_cfg.get("port", 3306)
    user = mysql_cfg.get("username")
    password = mysql_cfg.get("password")
    database = mysql_cfg.get("database")

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_filename = f"{database}_{timestamp}.sql"
    compressed_filename = backup_filename + ".gz"

    try:
        # Export using mysqldump
        dump_cmd = [
            "mysqldump",
            f"-h{host}",
            f"-P{port}",
            f"-u{user}",
            f"-p{password}",
            database
        ]
        with open(backup_filename, "wb") as f:
            result = subprocess.run(dump_cmd, stdout=f, stderr=subprocess.PIPE)

        if result.returncode != 0:
            print("Error during mysqldump:", result.stderr.decode())
            return

        # Compress the backup file
        with open(backup_filename, "rb") as f_in, gzip.open(compressed_filename, "wb") as f_out:
            f_out.writelines(f_in)

        os.remove(backup_filename)
        print(f"Backup completed and compressed to {compressed_filename}")

    except Exception as e:
        print(f"Backup failed: {e}")
