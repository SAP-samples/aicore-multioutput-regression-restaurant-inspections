# Build and push Docker Images of the implementations for Training and Inference

AI Core will run the training script *train.py* and the serving script *serve.py*
each in a separate Docker container in the cloud. Therefore, you first have to build the
Dockerfiles and then push them to your Docker Hub repository. To execute the needed Docker
commands install [Docker Desktop](https://www.docker.com/products/docker-desktop/) for your operating system if it is not installed already.

Change your working directory to *src/train/* in your
terminal. Notice this directory contains a Dockerfile. Now run the
following command to build the Dockerfile and to get a Docker image:

```bash
docker build -t <PATH-TO-DOCKERHUB-REPO>:<IMAGE-TAG> .
```

`<IMAGE-TAG>`: the tag you want to give your image as a name. 

Push this Docker image
to the Docker Hub repository by running:

```bash
docker push docker.io/<PATH-TO-DOCKERHUB-REPO>:<IMAGE-TAG>
```

Follow the same steps for the serving file. Change directory to
*src/serve/* and make sure to use a different tag for the serving Docker image.

Finally, take a look at your repository in Docker Hub and double check that both images have been
pushed successfully.