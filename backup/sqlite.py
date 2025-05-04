import shutil
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
    sqlite_cfg = config.get("sqlite", {})

    db_path = sqlite_cfg.get("db_path")
    if not db_path or not os.path.exists(db_path):
        logger.error("SQLite database file not found.")
        print("Error: SQLite database file not found.")
        return

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_filename = f"sqlite_backup_{timestamp}.db"
    compressed_filename = backup_filename + ".gz"

    logger.info(f"Starting SQLite backup from '{db_path}'")

    try:
        shutil.copy2(db_path, backup_filename)

        with open(backup_filename, "rb") as f_in, gzip.open(compressed_filename, "wb") as f_out:
            f_out.writelines(f_in)

        os.remove(backup_filename)

        logger.info(f"Backup completed successfully: {compressed_filename}")
        print(f"Backup completed and compressed to {compressed_filename}")

    except Exception as e:
        logger.exception(f"SQLite backup failed: {e}")
        print(f"Backup failed: {e}")
