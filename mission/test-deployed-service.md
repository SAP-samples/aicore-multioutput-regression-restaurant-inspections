# Test the deployed Inference service

Now that the inference service is running, send a request with some data about an
inspection to the service and receive a prediction from the model as a response. Use
the following code snippet:

```python
body = {
    "payload": [
        {
            "business_postal_code": "94102",
            "violation_description": "Unapproved or unmaintained equipment or utensils. Moderate risk food holding temperature. Noncompliance with HAACP plan or variance. Inadequate food safety knowledge or lack of certified food safety manager."
        },
        {
            "business_postal_code": "94102",
            "violation_description": "Moderate risk food holding temperature. Noncompliance with HAACP plan or variance. Inadequate food safety knowledge or lack of certified food safety manager."
        }
    ]
}

endpoint = f"{deployment.deployment_url}/v1/models/{resource_group}:predict"
headers = {"Authorization": ai_api_v2_client.rest_client.get_token(),
           'ai-resource-group': resource_group,
           "Content-Type": "application/json"}
response = requests.post(endpoint, headers=headers, json=body)

print('Inference result:', response.json())
pprint(vars(response))
```

After testing, stop the deployment again to save resources, by
running this code:

```python
delete_resp = ai_api_v2_client.deployment.modify(deployment_resp.id,
                                                 target_status=TargetStatus.STOPPED)
status = None
while status != Status.STOPPED:
    time.sleep(5)
    clear_output(wait=True)
    deployment = ai_api_v2_client.deployment.get(deployment_resp.id)
    status = deployment.status
    print('...... stopping deployment ......', flush=True)
    print(f"Deployment status: {deployment.status}")
```

AI Core will take some time to finish stop the deployment. Afterwards you van decide at any
point to deploy the inferencing service again.
