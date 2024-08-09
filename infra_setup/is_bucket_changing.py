import argparse
import boto3
import os
import subprocess
from time import sleep
from traceback import print_exc
from typing import cast, NoReturn

DR_LOCAL_S3_BUCKET = os.getenv('DR_LOCAL_S3_BUCKET')
DR_LOCAL_S3_METRICS_PREFIX = os.getenv('DR_LOCAL_S3_METRICS_PREFIX')


def get_interval() -> float:
    parser = argparse.ArgumentParser(
        description='keep checking s3 bucket at given interval')
    parser.add_argument(
        'interval_secs', type=float,
        help='interval seconds as float')
    args = parser.parse_args()
    return cast(float, args.interval_secs)


def keep_checking_metrics(interval_secs: float) -> NoReturn:
    prev_size = 0
    obj_name = None
    while True:
        sleep(interval_secs)
        try:
            if DR_LOCAL_S3_BUCKET is None \
                    or DR_LOCAL_S3_METRICS_PREFIX is None:
                print('Missing environment vars: DR_LOCAL_S3_BUCKET'
                      + ', DR_LOCAL_S3_METRICS_PREFIX')
                reboot_system()
            else:
                obj_name = f'{DR_LOCAL_S3_METRICS_PREFIX}/TrainingMetrics.json'
                size = get_obj_size(obj_name)
                if size == prev_size:
                    print('No change in size of object: '
                          + f'S3://{DR_LOCAL_S3_BUCKET}/{obj_name}')
                    print(f'Elapsed {interval_secs} secs: '
                          + f'prev_size={prev_size}, size_now={size}')
                    reboot_system()
                prev_size = size
        except Exception:
            print_exc()
            reboot_system()


def get_obj_size(key: str) -> int:
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(DR_LOCAL_S3_BUCKET)
    obj = bucket.Object(key)
    return obj.content_length


def reboot_system() -> None:
    print('stopping training')
    subprocess.run(['bash', '-c', 'cd $DR_DIR/scripts/training && ./stop.sh'])
    print('Rebooting')
    subprocess.run(['sudo', 'shutdown', '-r', '1'])


def main() -> None:
    interval_secs = get_interval()
    print(f'checking s3 bucket at {interval_secs} second intervals')
    keep_checking_metrics(interval_secs)


if __name__ == '__main__':
    main()
