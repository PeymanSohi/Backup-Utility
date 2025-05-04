import subprocess
import datetime
import shutil
import os
import tarfile
import yaml
from logger.logger import setup_logger

logger = setup_logger()

def load_config():
    with open("config.yaml", 'r') as file:
        return yaml.safe_load(file)

def backup():
    config = load_config()
    mongo_cfg = config.get("mongodb", {})

    host = mongo_cfg.get("host", "localhost")
    port = mongo_cfg.get("port", 27017)
    username = mongo_cfg.get("username")
    password = mongo_cfg.get("password")
    auth_db = mongo_cfg.get("auth_db", "admin")
    database = mongo_cfg.get("database")

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_dir = f"mongo_backup_{timestamp}"
    compressed_filename = f"{output_dir}.tar.gz"

    logger.info(f"Starting MongoDB backup for database '{database}'")

    try:
        dump_cmd = [
            "mongodump",
            f"--host={host}",
            f"--port={port}",
            f"--db={database}",
            f"--out={output_dir}"
        ]

        if username and password:
            dump_cmd += [
                f"--username={username}",
                f"--password={password}",
                f"--authenticationDatabase={auth_db}"
            ]

        result = subprocess.run(dump_cmd, stderr=subprocess.PIPE)

        if result.returncode != 0:
            error_msg = result.stderr.decode()
            logger.error(f"MongoDB backup failed: {error_msg}")
            print(f"Error during mongodump: {error_msg}")
            return

        with tarfile.open(compressed_filename, "w:gz") as tar:
            tar.add(output_dir, arcname=os.path.basename(output_dir))

        shutil.rmtree(output_dir)

        logger.info(f"Backup completed successfully: {compressed_filename}")
        print(f"Backup completed and compressed to {compressed_filename}")

    except Exception as e:
        logger.exception(f"MongoDB backup failed: {e}")
        print(f"Backup failed: {e}")
