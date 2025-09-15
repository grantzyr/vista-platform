# VISTA - Backend

## Requirements

* [Docker](https://www.docker.com/).
* [uv](https://docs.astral.sh/uv/) for Python package and environment management.

## Usage

Install [uv](https://docs.astral.sh/uv/).

From `./backend/` you can install all the dependencies with:

```console
$ uv sync
```

Then activate the virtual environment with:

```console
$ source .venv/bin/activate
```

Make sure your editor is using the correct Python virtual environment, with the interpreter at `backend/.venv/bin/python`.

Then you can simply run main file:

```console
$ python app/main.py
```

## Data Sync
Run:
```console
$ sh scripts/prestart.sh
```

## Docker Usage

Build docker image with:

```console
$ docker build -t [image-name]:[image-tag] -f Dockerfile .

# For MacOS to build amd64 images
$ docker buildx build --platform linux/amd64 -t [image-name]:[image-tag] -f Dockerfile .
```

Run image locally:

```console
docker run --env-file [.env file path] -e PORT=8000 -p 8000:8000 [--rm] [image-id] 
```

## License

This project is licensed under the MIT License.  
This project used template from [full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template/tree/master).