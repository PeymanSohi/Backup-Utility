import logging

def setup_logger():
    logging.basicConfig(filename="backup.log",
                        format='%(asctime)s %(message)s',
                        level=logging.INFO)
    return logging.getLogger()
