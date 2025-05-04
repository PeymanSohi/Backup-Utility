import subprocess
import datetime
import gzip
import os
import yaml
from logger.logger import setup_logger

logger = setup_logger()

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

    logger.info(f"Starting MySQL backup for database '{database}'")

    try:
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
            error_msg = result.stderr.decode()
            logger.error(f"MySQL backup failed: {error_msg}")
            print(f"Error during mysqldump: {error_msg}")
            return

        with open(backup_filename, "rb") as f_in, gzip.open(compressed_filename, "wb") as f_out:
            f_out.writelines(f_in)

        os.remove(backup_filename)

        logger.info(f"Backup completed successfully: {compressed_filename}")
        print(f"Backup completed and compressed to {compressed_filename}")

    except Exception as e:
        logger.exception(f"MySQL backup failed: {e}")
        print(f"Backup failed: {e}")
