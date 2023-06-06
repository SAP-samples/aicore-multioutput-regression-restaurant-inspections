# Store Data in Amazon S3 bucket provided by the Object Store service

In the following steps you will upload your dataset to an Amazon S3 bucket, a storage that
sits in the cloud, which the Object Store service created behind the scenes. This is to
make the data available to AI Core later on for the purpose of training the model.

## AWS CLI

To upload the dataset you will use the AWS Command Line Interface
(CLI) and your terminal. First install the [AWS
CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). Then
open your terminal and run:

```bash
aws configure
```

![AWS configure](resources/aws-configure.png)

Then enter your AWS credentials which you can find in the service key of your Object
Store instance on SAP BTP. Note that the appearance of the screen will not change as you type. You can leave
the `Default output format` entry as blank. Press enter to submit your credentials.

## Upload Dataset

To upload the dataset to your AWS S3 bucket, paste and edit the following command in the
terminal so that the `<bucket-name>` matches the name of your bucket.

```bash
aws s3 cp inspections.csv s3://<BUCKET-NAME>/app/data/
```

To double check whether the dataset was uploaded successfully, run:

```bash
aws s3 ls s3://<BUCKET-NAME>/app/data/
```

The output of the command should include *inspections.csv*