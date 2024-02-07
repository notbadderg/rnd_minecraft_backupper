import os
from dotenv import find_dotenv, load_dotenv

from backupper import backupper_core
from utils import CustomException


def get_config() -> dict:
    load_dotenv(find_dotenv())

    params_ = [
        'SERVICE_NAME',
        'SERVER_NAME',

        'SRC_PATH',
        'BACKUPS_PATH',
        'EXCLUDE_TXT_PATH',

        'DAILY_BACKS_QUANTITY',
        'HOURLY_BACKS_QUANTITY',
        'HOURLY_BACKS_INTERVAL',
    ]

    cfg_ = {}
    for param in params_:
        value = os.getenv(param)
        if not value:
            raise CustomException(f'Missed {value}')
        cfg_[param] = value

    return cfg_


def main():
    cfg = get_config()
    backupper_core(cfg)


if __name__ == '__main__':
    main()
