#!/usr/bin/env python3

import gc
import vos
import time
import asyncio
import nest_asyncio
from prefect import task, flow, get_run_logger
from skaha.images import Images
from skaha.session import Session


nest_asyncio.apply()
RUNNING_STATES = ['Pending', 'Running', 'Terminating']
COMPLETE_STATES = ['Failed', 'Succeeded']
MIRIAD_IMAGE = "images.canfar.net/srcnet/miriad:dev"
SOFIA_IMAGE = "images.canfar.net/srcnet/sofia2:v2.6.0"


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
async def check_file_exists(client, path, filename):
    logger = get_run_logger()
    contents = client.listdir(path)
    assert filename in contents, 'File does not exist in the searched path.'
    logger.info(contents)
    return


@task(task_run_name='{name}')
async def job(name, session, params, interval=0.5, *args, **kwargs):
    """Job wrapper for CANFAR containers

    """
    logger = get_run_logger()
    logger.info(name)
    completed = False
    session_id = session.create(**params)
    while not completed:
        res = session.info(session_id)
        states = [s['status'] for s in res]
        completed = all([status in COMPLETE_STATES for status in states])
        time.sleep(interval)
        logger.info(states)
    return


@flow(name='skaha_pipeline')
async def pipeline():
    path = 'arc:/projects/WALLABY_test'
    filename = 'POSSUM.mfs.band1.1029-55_1017-60_1058-60.11400.i.fits'

    # setup
    logger = get_run_logger()
    client, session = setup()

    # check file
    await check_file_exists(client, path, filename)

    # submit miraid job
    params = {
        'name': "miriad", 'image': MIRIAD_IMAGE,
        'cores': 2, 'ram': 4, 'kind': "headless",
        'cmd': "sleep", 'args': "0.5", 'env': {}
    }
    await job(params['name'], session, params)
    logger.info('Miriad job complete')

    # submit parallel source finding jobs
    params = [
        {'name': "sofia1", 'image': SOFIA_IMAGE, 'cores': 2, 'ram': 2, 'kind': "headless", 'cmd': "sleep", 'args': "1", 'env': {}},
        {'name': "sofia2", 'image': SOFIA_IMAGE, 'cores': 2, 'ram': 2, 'kind': "headless", 'cmd': "sleep", 'args': "1", 'env': {}}
    ]
    task_list = []
    for i, param in enumerate(params):
        name = f'{param["name"]}.{i}'
        task = asyncio.create_task(job(name, session, param))
        task_list.append(task)
    logger.info(task_list)
    await asyncio.gather(*task_list)

    # submit miraid job again after
    params = {
        'name': "miriad", 'image': MIRIAD_IMAGE,
        'cores': 2, 'ram': 4, 'kind': "headless",
        'cmd': "sleep", 'args': "1", 'env': {}
    }
    await job(params['name'], session, params)
    logger.info('Miriad job complete')


if __name__ == '__main__':
    asyncio.run(pipeline())