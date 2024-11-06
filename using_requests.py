#!/usr/bin/env python3

import logging
import requests


logging.basicConfig(level=logging.INFO)


IMAGE_BASEURL = 'https://ws-uv.canfar.net/skaha/v0/image'
SESSION_BASEURL = 'https://ws-uv.canfar.net/skaha/v0/session'
CERTIFICATE = '/Users/she393/.ssl/cadcproxy.pem'


def submit_job(name, image, command):
    url = f'{SESSION_BASEURL}'
    data = {
        'name': name,
        'image': image,
        'cmd': command
    }
    cert = (CERTIFICATE)
    r = requests.post(url, data=data, cert=cert)
    if r.status_code != 200:
        logging.error(r.status_code)
        raise Exception(f'Request failed {r.content}')
    logging.info(r.content)
    return r.content.decode('utf-8')


def get_job(session_id, logs=False):
    url = f'{SESSION_BASEURL}/{session_id}'
    if logs:
        url = f'{SESSION_BASEURL}/{session_id}?view=logs'
    cert = (CERTIFICATE)
    r = requests.get(url, cert=cert)
    if r.status_code != 200:
        logging.error(r.status_code)
        logging.error(r.content)
    logging.info(r.content)
    return r.content.decode('utf-8')


def get_images(type='headless'):
    url = f'{IMAGE_BASEURL}?type={type}'
    cert = (CERTIFICATE)
    r = requests.get(url, cert=cert)
    logging.info(r.status_code)
    return r


def main():
    # Fetch all images
    # get_images()

    # Submit a job
    image = 'images.canfar.net/srcnet/sofia2:v2.6.0'
    command = 'sleep 5m'
    name = 'sofia-test'
    # session_id = submit_job(name=name, image=image, command=command)

    # Check job
    session_id = 'fl0xa88j'
    get_job(session_id)

    # Check logs

if __name__ == '__main__':
    main()