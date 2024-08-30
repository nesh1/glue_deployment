import boto3
from botocore.exceptions import ClientError



AWS_S3_BUCKET_NAME = 'glue-buck1'
AWS_REGION = 'us-east-1'
AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''

LOCAL_FILE = 'glue_job.py'
NAME_FOR_S3 = 'codes/glue_job.py'

def upload_file_to_s3():
    print('in main method')

    s3_client = boto3.client(
        service_name='s3',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    response = s3_client.upload_file(LOCAL_FILE, AWS_S3_BUCKET_NAME, NAME_FOR_S3)

    print(f'upload_log_to_aws response: {response}')





class GlueWrapper:
    """Encapsulates AWS Glue actions."""

    def __init__(self, glue_client):
        """
        :param glue_client: A Boto3 Glue client.
        """
        self.glue_client = glue_client


    def create_job(self, name, description, role_arn, script_location):
        """
        Creates a job definition for an extract, transform, and load (ETL) job that can
        be run by AWS Glue.

        :param name: The name of the job definition.
        :param description: The description of the job definition.
        :param role_arn: The ARN of an IAM role that grants AWS Glue the permissions
                         it requires to run the job.
        :param script_location: The Amazon S3 URL of a Python ETL script that is run as
                                part of the job. The script defines how the data is
                                transformed.
        """
        try:
            self.glue_client.create_job(
                Name=name,
                Description=description,
                Role=role_arn,
                Command={
                    "Name": "glueetl",
                    "ScriptLocation": script_location,
                    "PythonVersion": "3",
                },
                GlueVersion="3.0",
            )
        except ClientError as err:
            print(
                "Couldn't create job %s. Here's why: %s: %s",
                name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise


upload_file_to_s3()


name = 'test_job'
description= 'description'
role_arn = "arn:aws:iam::236284140018:role/IAM_GitHub"
script_location = 's3://glue-buck1/codes/glue_job.py'

glue = boto3.client("glue",region_name='us-east-1',aws_access_key_id='',
        aws_secret_access_key='')
gw = GlueWrapper(glue)

gw.create_job(name,description,role_arn,script_location)

