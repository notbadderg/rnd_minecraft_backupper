import datetime
import os
import subprocess
import time

from utils import CustomException


def is_need_do_backup(considered_path: os.path, prefix: str, period: int) -> bool:
    for path, folder, files in os.walk(considered_path):
        for file in files:
            if (prefix in file and
                    (time.time() - os.path.getmtime(os.path.join(path, file)) <= period)):
                return False
    return True


def stop_server(service_name: str, server_name: str) -> None:
    print('Countdown 60 secs...')
    msg_cmd = (f'"su -l minecraft -s" /usr/bin/screen -p 0 -S mc-{server_name} -X eval ' +
               'stuff "say SERVER RESTARTING FOR BACKING IN 60 SECONDS."\015')
    subprocess.run(msg_cmd, shell=True)
    time.sleep(60)
    print(f'Stopping {service_name}...')
    subprocess.run(f'systemctl stop {service_name}', shell=True)


def start_server(service_name: str) -> None:
    print('Countdown 10 secs...')
    time.sleep(10)
    print(f'Starting {service_name}...')
    subprocess.run(f'systemctl start {service_name}', shell=True)


def do_backup(src: str, dst: str, exc_path: str, prefix: str, service_name: str, server_name: str) -> None:
    stop_server(service_name, server_name)

    arch_path_name = f'{dst}/{prefix}_{datetime.datetime.now():%Y-%m-%d_%H-%M-%S-%f}.7z'
    arch_cmd = f'7z a -xr@{exc_path} -mx9 {arch_path_name} {src}'
    out = subprocess.run(arch_cmd, shell=True)
    if out.returncode != 0:
        raise CustomException(f'do_backup error code {out.returncode}')

    start_server(service_name)


def backupper_core(cfg) -> None:
    server_name = cfg['SERVER_NAME']

    backups_path = cfg['BACKUPS_PATH']
    current_server_backups_path = os.path.join(backups_path, server_name)
    daily_path = os.path.join(str(current_server_backups_path), 'daily')
    hourly_path = os.path.join(str(current_server_backups_path), 'hourly')

    # check or create backup paths
    for path in [backups_path, current_server_backups_path, daily_path, hourly_path]:
        if not os.path.exists(path):
            os.mkdir(path)

    arch_prefix = server_name
    hourly_backs_period = int(cfg['HOURLY_BACKS_INTERVAL'])*3600

    if is_need_do_backup(daily_path, arch_prefix, 86400):
        # DO DAY BACKUP
        do_backup(cfg['SRC_PATH'],
                  str(daily_path),
                  cfg['EXCLUDE_TXT_PATH'],
                  arch_prefix,
                  cfg['SERVICE_NAME'],
                  cfg['SERVER_NAME'])
        was_backed_now = True

    elif (is_need_do_backup(daily_path, arch_prefix, hourly_backs_period) and
          is_need_do_backup(hourly_path, arch_prefix, hourly_backs_period)):
        # DO HOUR BACKUP
        do_backup(cfg['SRC_PATH'],
                  str(hourly_path),
                  cfg['EXCLUDE_TXT_PATH'],
                  arch_prefix,
                  cfg['SERVICE_NAME'],
                  cfg['SERVER_NAME'])
        was_backed_now = True

    else:
        was_backed_now = False

    if was_backed_now:
        # DO CLEARINGS
        pass
