# CANFAR pipeline

An example Python pipeline running on the CANFAR science platform

## Getting started

To run this example CANFAR pipeline there are a few setup steps required. First we need to create a Python environment and install all of the dependencies

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then, we need to deploy the prefect server, and to do this we need to have a running PostgreSQL instance. The easiest way to do this is to run the following Docker command

```
docker run -d --name prefect-postgres -v \
    data:/var/lib/postgresql/data \
    -p 5432:5432 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=prefect \
    postgres:latest
```

And finally we will be able to run the prefect server. Run the following command

```
prefect config set PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://postgres:password@localhost:5432/prefect"
prefect server start
```

Once all of this is set up, we can run the example pipeline with

```
python3 pipeline.py
```

## Background

Here is some background about CANFAR and the tools that may be required to get started using their platform, with links to key reference material. You need to sign up for a CADC account first and then run `pip install vos` in your preferred environment.

### Publishing containers

Push your containers that you have built locally to the project space. This will require certain permissions (I have developer access) for the project space to which you push your image. For this work we have used the `srcnet` project space.

```
docker push images.canfar.net/srcnet/miriad:dev
docker push images.canfar.net/srcnet/sofia2:v2.6.0
```

You will then need to label images as `headless`, which can be done using the GUI at https://images.canfar.net/, to be able to run them in the batch processing mode. You can also view the available images at the web page linked.

### Batch processing

All of your jobs cnan be monitored at the science portal at https://www.canfar.net/science-portal/. To start with get the certificate with the following

```
cadc-get-cert -u axshen
```

This will generate an SSL certificate at `~/.ssl/cadcproxy.pem`. You can then perform a GET request for images available for headless with the following query:

```
curl -E ~/.ssl/cadcproxy.pem https://ws-uv.canfar.net/skaha/v0/image\?type\=headless
```

Then you can run a headless container and monitor/check logs with the following set of commands

```
# Run a job
curl -E ~/.ssl/cadcproxy.pem https://ws-uv.canfar.net/skaha/v0/session -d "name=sofia-test" -d "image=images.canfar.net/srcnet/sofia2:v2.6.0" --data-urlencode "cmd=sofia"

# List the sessions
curl -E ~/.ssl/cadcproxy.pem https://ws-uv.canfar.net/skaha/v0/session

# View the logs for a given session
curl -E ~/.ssl/cadcproxy.pem https://ws-uv.canfar.net/skaha/v0/session/<sessionID>?view=logs
```

Or you can use the Python client which makes everything a lot easier.

Links:

* Docs: https://www.opencadc.org/science-containers/complete/headless/
* Science containers (SKAHA) https://www.opencadc.org/science-containers/
* Python client https://shinybrar.github.io/skaha/session/
* API reference https://ws-uv.canfar.net/skaha/

### Data access

Data storage https://www.canfar.net/en/docs/storage/

Use the storage management command line tools to list VOspaces. You can list the possible spaces with `vls vos:` and `vls arc:` which are two different vospaces where data can be stored. Here are a list of useful commands to set up the VOspace for a project

```
vls arc:projects
vmkdir arc:projects/wallaby_test
vcp file1.txt arc:projects/wallaby_test/file1.txt
```

### Execution

You can use the web browser to view status and logs

https://ws-uv.canfar.net/skaha/v0/session/
https://ws-uv.canfar.net/skaha/v0/session/nrkhsmiq?view=events
https://ws-uv.canfar.net/skaha/v0/session/nrkhsmiq?view=logs