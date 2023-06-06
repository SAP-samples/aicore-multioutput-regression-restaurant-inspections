# Register general Artifacts for Deployment in AI Core

Before you can start to train the model, you will first need to register different
artifacts for your AI Core instance. These artifacts include setup details and credentials
that AI Core needs in order to proceed. First, create a *resources/* directory at the root
level of your folder and copy the following files into *resources/*:

- Service key of your AI Core instance
- Service key of your Object Store instance. This service key contains the credentials to access
  the Amazon S3 bucket which the Object Store created behind the scenes.
- A JSON file with the details of your GitHub repository like the repository URL. You are
  going to onboard this repository in a later step.
- A JSON file with your Docker secret. Make sure to use a Docker Hub Personal Access Token
  (PAT) instead of your normal Docker Hub password. The AI Core instance needs this secret
  to pull the docker images from your Docker Hub repository later on for training and serving.

Next, follow the first few steps inside the [main.ipynb](../src/main.ipynb) file. In the
following steps the AI API Python SDK is used to interact with the AI Core instance and
the AI API. 

## Connect to your AI Core instance

Read the credentials from your AI Core service key file and create an AI API
client.

```python
with open(aic_service_key_path) as ask:
    aic_service_key = json.load(ask)

ai_api_client = AIAPIV2Client(
    base_url = aic_service_key["serviceurls"]["AI_API_URL"] + "/v2",
    auth_url=  aic_service_key["url"] + "/oauth/token",
    client_id = aic_service_key['clientid'],
    client_secret = aic_service_key['clientsecret']
)
```

## Onboard your Git repository

You need a git repository on GitHub that contains the workflow files that will be used for
training and serving. Onboard this repository by doing the following:

```python
with open(git_setup_file_path) as gs:
		setup_json = json.load(gs)

repo_json = setup_json["repo"]

response = ai_api_client.rest_client.post(
		path="/admin/repositories",
		body={
				"name": repo_json["name"],
				"url": repo_json["url"],
				"username": repo_json["username"],
				"password": repo_json["password"]
		}
)
print(response)
```

## Register an application

Register an application for your onboarded repository.

```python
app_json = setup_json["app"]
response = ai_api_client.rest_client.post(
		path="/admin/applications",
		body={
				"applicationName": app_json["applicationName"],
				"repositoryUrl": app_json["repositoryUrl"],
				"revision": app_json["revision"],
				"path": app_json["path"]
		}
)
```

## Docker secret

To register your Docker secret, do the following:

```python
with open(docker_secret_file_path) as dsf:
    docker_secret = json.load(dsf)

response = ai_api_client.rest_client.post(
    path="/admin/dockerRegistrySecrets",
    body={
        "name": docker_secret["name"],
        "data": docker_secret["data"]
    }
)
print(response)
```

## Create a resource group

Now, create a resource group. Think of it as a scope for your registered artifacts.

```python
ai_api_client.rest_client.post(
    path="/admin/resourceGroups",
    body={
        "resourceGroupId": resource_group
    }
)
```

## Register Amazon S3 bucket secret

To download the training dataset that your store in the Amazon S3 bucket created by the
Object Store, the AI Core instance has to be able to access this bucket. Therefore, register the
secret for the bucket:

```python
with open(s3_service_key_path) as s3sk:
    s3_service_key = json.load(s3sk)

default_secret = {
    "name": connection_name,
    "type": "S3",
    "endpoint": s3_service_key["host"],
    "bucket": s3_service_key["bucket"],
    "pathPrefix": path_prefix,
    "region": s3_service_key["region"],
    "data": {
        "AWS_ACCESS_KEY_ID": s3_service_key["access_key_id"],
        "AWS_SECRET_ACCESS_KEY": s3_service_key["secret_access_key"]
    }
}

ai_api_client.rest_client.post(
    path="/admin/objectStoreSecrets",
    body = default_secret,
    resource_group = resource_group
)
```

## Register training data as artifact

In order to execute the training workflow later on, you further need to register the training
data as an artifact for the AI Core instance:

```python
with open(training_workflow_file) as twf:
    training_workflow = yaml.safe_load(twf)

scenario_id = training_workflow['metadata']['labels']['scenarios.ai.sap.com/id']

artifact = {
        "name": resource_group,
        "kind": Artifact.Kind.DATASET,
        "url": f"ai://{connection_name}/data",
        "description": "The training data set.",
        "scenario_id": scenario_id
}

artifact_resp = ai_api_v2_client.artifact.create(**artifact)
print(f"Artifacts registered for {scenario_id} scenario!")
pprint(vars(artifact_resp)) 

assert artifact_resp.message == 'Artifact acknowledged'
```