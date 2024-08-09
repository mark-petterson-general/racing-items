import boto3
import os

DR_LOCAL_S3_BUCKET = os.getenv('DR_LOCAL_S3_BUCKET')
DR_LOCAL_S3_MODEL_PREFIX = os.getenv('DR_LOCAL_S3_MODEL_PREFIX')
DR_LOCAL_S3_METRICS_PREFIX = os.getenv('DR_LOCAL_S3_METRICS_PREFIX')


def obj_exists(bucket: str, prefix: str, key: str) -> bool:
    s3 = boto3.resource('s3')
    resource = s3.Bucket(bucket)
    objs = list(resource.objects.filter(Prefix=prefix))
    return key in [x.key for x in objs]


def is_metric_present() -> bool:
    return obj_exists(
        DR_LOCAL_S3_BUCKET,
        DR_LOCAL_S3_MODEL_PREFIX,
        f'{DR_LOCAL_S3_METRICS_PREFIX}/TrainingMetrics.json'
    )


def main() -> None:
    '''
    Prints "overwrite" to the console if the folder is safe to overwrite.
    Notionally, this is if not any exceptions were thrown when reading
    the folder, and that the metrics file is not present in the folder.
    '''
    if not is_metric_present():
        print('overwrite', end='')


if __name__ == '__main__':
    main()
