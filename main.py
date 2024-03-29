import argparse
import boto3
import os

bucket = 'd17.itiscl.ru'


def upload(path, album):
    if path is None or album is None:
        raise Exception('Path or arguments is not present')
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        files.extend(filenames)
        break
    for file in files:
        s3.Bucket(bucket).upload_file(path + '/' + file, album + '/' + file)


def download(path, album):
    if path is None or album is None:
        raise Exception('Path or arguments is not present')
    files = filter(lambda x: x.key[:len(album)] == album, s3.Bucket(bucket).objects.all())
    for file in files:
        s3.Bucket(bucket).download_file(file.key, path + '/' + file.key.split('/')[-1])


def list(album):
    if album is None:
        albums = set()
        files = s3.Bucket(bucket).objects.all()
        for file in files:
            albums.add(file.key.split('/')[0])
        for album in albums:
            print(album)
    else:
        files = filter(lambda x: x.key[:len(album)] == album, s3.Bucket(bucket).objects.all())
        for file in files:
            print(file.key)


parser = argparse.ArgumentParser(description='Arguments Parser')
parser.add_argument('command', type=str, help='Command name')
parser.add_argument(
    '-p',
    type=str,
    help='Path to directory with files'
)

parser.add_argument(
    '-a',
    type=str,
    help='Album name'
)

args = parser.parse_args()
session = boto3.session.Session()
s3 = session.resource(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

if args.command == 'upload':
    upload(args.p, args.a)
elif args.command == 'download':
    download(args.p, args.a)
elif args.command == 'list':
    list(args.a)
else:
    raise Exception('Unknown command')
