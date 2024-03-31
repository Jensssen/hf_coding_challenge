# Question3: Container Creation and Testing Exercise

This Dockerfile can be used to build an environment that supports CUDA for GPU acceleration and the Hugging Face
Transformers library for training LLMs.

## How to build

You can build the docker image locally by executing the following command (make sure to specify a docker image name):

```shell
docker build -t <DOCKER_IMAGE_NAME> .
```

Optionally, you can provide the following build arguments to set specific python, cuda and torch versions:

```shell
docker build --build-arg PYTHON_VERSION=3.9 --build-arg CUDA_VERSION=cu118 --build-arg TORCH_VERSION=2.2.0 -t <DOCKER_IMAGE_NAME> .
```

Additional dependencies can be specified in the `requirements.txt` file.

## How to test

You can test the docker image by executing the following command:

```shell
docker run --gpus all --rm <DOCKER_IMAGE_NAME> python3 test.py
```

The output of the test file should look similar to this:

```
Cuda available: True
Number of available GPUs: 1
GPU Name: NVIDIA GeForce RTX 3070
[{'label': 'POSITIVE', 'score': 0.9998798370361328}]
```

## How to push the image to a GCP artifact registry

Pushing the image to the GCP artifact registry can be achieved by executing the following two commands:

1. ```shell 
   docker tag <DOCKER_IMAGE_NAME> <REGION>-docker.pkg.dev/<PROJECT_NAME>/<REPO_NAME>/<DOCKER_IMAGE_NAME>:<TAG>
   ```
2. ```shell
   docker push <REGION>-docker.pkg.dev/<PROJECT_NAME>/<REPO_NAME>/<DOCKER_IMAGE_NAME>:<TAG>
   ```

Example commands could look like this:

```shell
   docker tag inference-image us-east1-docker.pkg.dev/my-project/my-repo/my-inference-image:latest
   docker push us-east1-docker.pkg.dev/my-project/my-repo/my-inference-image:latest
```

For more detailed information, please have a look at the official documentation [HERE](https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling?hl=en).