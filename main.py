import subprocess


class CustomException(Exception):
    pass


def backupper(src_path_raw, dst_path_raw, backups_quantity):
    pass


def main():
    service_name = None
    src_path = None
    dst_path = None
    backups_quantity = None

    if not service_name or not src_path or not dst_path or not backups_quantity:
        raise CustomException('Missed some parameters!')

    subprocess.run(['systemctl', f'stop {service_name}'])

    subprocess.run(['systemctl', f'start {service_name}'])


if __name__ == '__main__':
    main()
