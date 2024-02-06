import os
import subprocess

from dotenv import find_dotenv, load_dotenv


class CustomException(Exception):
    pass


def backupper(src_path_raw, dst_path_raw, backups_quantity):
    pass


def main():
    load_dotenv(find_dotenv())

    service_name = os.getenv('SERVICE_NAME')
    src_path = os.getenv('SRC_PATH')
    dst_path = os.getenv('DST_PATH')
    backups_quantity = int(os.getenv('BACKUPS_QUANTITY'))

    if not service_name or not src_path or not dst_path or not backups_quantity:
        raise CustomException('Missed some parameters!')

    subprocess.run(['systemctl', f'stop {service_name}'])

    subprocess.run(['systemctl', f'start {service_name}'])


if __name__ == '__main__':
    main()
