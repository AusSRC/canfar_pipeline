#!/usr/bin/env python3

import logging
import vos
from skaha.images import Images
from skaha.session import Session


logging.basicConfig(level=logging.INFO)


CERTIFICATE = '/Users/she393/.ssl/cadcproxy.pem'


def main():
    # List images
    images = Images()
    session = Session(certificate=CERTIFICATE)

    # res = images.fetch(kind='headless')
    # logging.info(res)

    # Submit headless job
    params = {
        'image': 'images.canfar.net/srcnet/miriad:dev',
        'name': 'miriad-test',
        'cmd': 'ls /arc/projects/WALLABY_test/',
        'env': {'NAME': 'test'}
    }
    # session_ids = session.create(**params)
    # logging.info(session_ids)

    # Check logs and monitor headless job
    session_id = ['ogow4beq']
    res = session.info(session_id)
    logging.info(res)

    # # List files in VOspace
    # client = vos.Client()
    # res = client.listdir('arc:home/axshen')
    # logging.info(res)
    # res = client.listdir('arc:projects/WALLABY_test')
    # logging.info(res)

    # # Copy files to VOspace
    # # client.copy('/Users/she393/Downloads/data/POSSUM.mfs.band1.1029-55_1017-60_1058-60.11400.i.fits', 'arc:projects/WALLABY_test/POSSUM.mfs.band1.1029-55_1017-60_1058-60.11400.i.fits')
    # res = client.listdir('arc:projects/WALLABY_test')
    # logging.info(res)


if __name__ == '__main__':
    main()