# Digitizing Criticality Assessments using SAP AI Core and SAP AI Launchpad

[![REUSE status](https://api.reuse.software/badge/github.com/SAP-samples/aicore-multioutput-regression-restaurant-inspections)](https://api.reuse.software/info/github.com/SAP-samples/aicore-multioutput-regression-restaurant-inspections)

## Description

Assessing risk or criticality often requires manual input from experts and rarely benefits
from past assessments. This makes the overall process time-consuming and potentially leads
to inconsistency over time. To digitize the computation of the criticality, we propose a
machine learning (ML) service for criticality assessments in this mission. The
assessments that are used throughout this mission are exemplary and based on restaurant
inspections where a health inspector, the expert, screens a restaurant and protocols
violations. In the end the inspector comes up with a suitable score for the
restaurant. The provided data comes from a publicly available dataset
(Restaurant Scores - LIVES Standard in San Francisco published by Public Health) which has
been restructured to fit the ML approach of multi-output-regression. Since the SAP Data Attribute Recommendation service
(DAR) does not support multi-output-regression yet, this mission showcases a solution
leveraging SAP AI Core and open source. The approach of this mission can be easily adapted
to similar kinds of criticality assessments.

This mission is based on a real customer use case about criticality assessments which is currently in productization.

### Current Position - What is the challenge?

Organizations can have complex rules for their criticality assessments. Many times, the
assessment is dominated by manual input, which is prone to errors and can be time-consuming.
Besides that, due to individual approaches of different processors, inconsistencies can
arise over the time, yielding different results for similar inputs.

### Destination - What is the outcome?

The solution uses ML to assist the processor of criticality assessments by translating descriptions and details of a criticality assessment to multiple scores necessary to conclude the assessment.

### How You Get There - What is the solution?

A machine learning service that leverages the capabilities of SAP Business Technology Platform
(SAP AI Core and SAP AI Launchpad). The service assesses the criticality based on the descriptions of the criticality
assessment itself. In this case the descriptions are the violations the
inspector protocols during the inspections. Since the descriptions consist of unstructured
text, they first will be transformed to vectors, so-called embeddings. Finally,
a multi-output-regression can be performed to determine multiple scores.

## Requirements

### Mandatory mission steps

1. [Upload training data to Amazon S3 bucket](mission/upload-data-s3.md)
2. [Build and push Docker images for training and serving](mission/build-push-docker-imgs.md)
3. [Register general artifacts](mission/register-general-artifacts.md)
4. [Setup and execute training](mission/setup-execution-training.md)
5. [Setup and deploy inference service](mission/setup-deployment-inference-service.md)
6. [Test inference service](mission/test-deployed-service.md)

### Boilerplate AI Core

You can use this repository as a boilerplate for AI Core and adjust it quickly to your own AI Core
use case. The interaction with the AI Core instance happens programmatically using Python.
To do so, consider the following instructions:

1. In the _resources/_ directory adjust the credentials and setup information so that
   they match yours.
   - Save your AI Core service key as _aic_service_key.json_
   - Add Docker credentials to _docker_secret.json_. It is recommended to use a Docker Hub Personal Access
     Token (PAT) instead of your Docker Hub password.
   - Add details about the git repository that is going to be onboarded later to
     _git_setup.json_. Further, specify a name for your application in this file.
   - Add your Amazon S3 bucket service key to _s3_service_key.json_. This is actually the
     service key of your Object Store instance that creates the S3 bucket behind the
     scenes for you.
   - Make sure to not publish the _resources/_ directory as it contains credentials.
2. Upload your training data to the Amazon S3 bucket via the command line. Look [here](mission/upload-data-s3.md)
   to see how to do this.
3. Integrate your own training script into _src/train/train.py_
   - `DATASET_PATH` is the directory in the Docker container file system in which your uploaded
     training data will sit later on.
   - `environ["OUTPUT_PATH"]` is the directory under which to save the model after training
     to in the Docker container file system.
4. Integrate your serving code into _src/serve/serve.py_
   - Make sure `MODEL_NAME` is the same name under which your save your trained model previously.
5. Add the requirements (required python libraries) that are necessary to run your
   training script to _src/train/requirements.txt_. Analog, list your requirements to run
   your serving script in _src/serve/requirements.txt_.
6. Adjust both Dockerfiles (_src/train/Dockerfile_ and _src/serve/Dockerfile_)
   - Make sure the specified python base image matches the python version you used when you
     installed your python libraries requirements locally (e.g., for testing purposes).
7. Build both Dockerfiles and upload the images to your Docker Hub repository. Tags can be used to differentiate between
   different Docker images here. See [here](mission/build-push-docker-imgs.md) for more
   details.
   - Make sure the specified URLs for the Docker images in the workflow files
     (_workflows/serve.yaml_ and _workflows/train.yaml_) match the URLs to the images
     inside your Docker Hub repository.
8. Adjust the naming of the values inside the workflow files so that they fit your use
   case.
9. Finally, execute each step in _src/main.ipynb_ in sequential order. Here the
   interaction with the AI Core instance takes place. For example, you are going to
   initiate the training and serving here.

## Known Issues

<!-- You may simply state "No known issues. -->

## How to obtain support

[Create an issue](https://github.com/SAP-samples/<repository-name>/issues) in this repository if you find a bug or have questions about the content.

For additional support, [ask a question in SAP Community](https://answers.sap.com/questions/ask.html).

## Contributing

If you wish to contribute code, offer fixes or improvements, please send a pull request. Due to legal reasons, contributors will be asked to accept a DCO when they create the first pull request to this project. This happens in an automated fashion during the submission process. SAP uses [the standard DCO text of the Linux Foundation](https://developercertificate.org/).

## License

Copyright (c) 2023 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0 except as noted otherwise in the [LICENSE](LICENSE) file.
