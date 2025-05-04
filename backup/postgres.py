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
    pg_cfg = config.get("postgres", {})

    host = pg_cfg.get("host", "localhost")
    port = pg_cfg.get("port", 5432)
    user = pg_cfg.get("username")
    password = pg_cfg.get("password")
    database = pg_cfg.get("database")

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_filename = f"{database}_{timestamp}.sql"
    compressed_filename = backup_filename + ".gz"

    logger.info(f"Starting PostgreSQL backup for database '{database}'")

    try:
        env = os.environ.copy()
        env["PGPASSWORD"] = password

        dump_cmd = [
            "pg_dump",
            "-h", host,
            "-p", str(port),
            "-U", user,
            "-F", "p",  # plain text format
            "-f", backup_filename,
            database
        ]

        result = subprocess.run(dump_cmd, env=env, stderr=subprocess.PIPE)

        if result.returncode != 0:
            error_msg = result.stderr.decode()
            logger.error(f"PostgreSQL backup failed: {error_msg}")
            print(f"Error during pg_dump: {error_msg}")
            return

        with open(backup_filename, "rb") as f_in, gzip.open(compressed_filename, "wb") as f_out:
            f_out.writelines(f_in)

        os.remove(backup_filename)

        logger.info(f"Backup completed successfully: {compressed_filename}")
        print(f"Backup completed and compressed to {compressed_filename}")

    except Exception as e:
        logger.exception(f"PostgreSQL backup failed: {e}")
        print(f"Backup failed: {e}")
