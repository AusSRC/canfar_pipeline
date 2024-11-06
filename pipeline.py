#!/usr/bin/env python3

import vos
from prefect import task, flow, get_run_logger
from skaha.images import Images
from skaha.session import Session


@task
def setup():
    """You will also need to run the following to set up the prefect client
        prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api

    """
    logger = get_run_logger()
    CERTIFICATE = '/Users/she393/.ssl/cadcproxy.pem'
    session = Session(certificate=CERTIFICATE)
    client = vos.Client()
    logger.info('CADC client connection established...')
    return client, session

@task
def check_file_exists(client, path, filename):
    logger = get_run_logger()
    contents = client.listdir(path)
    assert filename in contents, 'File does not exist in the searched path.'
    logger.info(contents)


@flow(name='skaha_pipeline')
def pipeline():
    path = 'arc:/projects/WALLABY_test'
    filename = 'POSSUM.mfs.band1.1029-55_1017-60_1058-60.11400.i.fits'

    client, session = setup()
    check_file_exists(client, path, filename)


if __name__ == '__main__':
    pipeline()