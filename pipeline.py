#!/usr/bin/env python3

import vos
import time
from prefect import task, flow, get_run_logger
from skaha.images import Images
from skaha.session import Session


RUNNING_STATES = ['Pending', 'Running', 'Terminating']
COMPLETE_STATES = ['Failed', 'Succeeded']


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


def job(session, params, interval=1, *args, **kwargs):
    """Job wrapper for CANFAR containers

    """
    logger = get_run_logger()
    completed = False
    session_id = session.create(**params)
    while not completed:
        res = session.info(session_id)
        states = [s['status'] for s in res]
        completed = all([status in COMPLETE_STATES for status in states])
        time.sleep(interval)
        logger.info(states)
    return


@task
def s2p_setup():
    logger = get_run_logger()
    time.sleep(5)


@task
def sofia():
    logger = get_run_logger()
    time.sleep(2)


@flow(name='skaha_pipeline')
def pipeline():
    path = 'arc:/projects/WALLABY_test'
    filename = 'POSSUM.mfs.band1.1029-55_1017-60_1058-60.11400.i.fits'

    client, session = setup()
    # check_file_exists(client, path, filename)
    # s2p_setup()
    # sofia()

    params = {
        'name': "test",
        'image': "images.canfar.net/srcnet/sofia2:v2.6.0",
        'cores': 2,
        'ram': 2,
        'kind': "headless",
        'cmd': "sleep",
        'args': "5",
        'env': {},
    }
    job(session, params)


if __name__ == '__main__':
    pipeline()