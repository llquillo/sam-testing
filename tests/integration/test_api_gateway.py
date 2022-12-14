import os
import io
import boto3
import json
import pytest
import requests

"""
Make sure env variable AWS_SAM_STACK_NAME exists with the name of the stack we are going to test. 
"""


class TestApiGateway:

    @pytest.fixture()
    def api_gateway_url(self):
        """ Get the API Gateway URL from Cloudformation Stack outputs """
        stack_name = os.environ.get("AWS_SAM_STACK_NAME")

        if stack_name is None:
            raise ValueError('Please set the AWS_SAM_STACK_NAME environment variable to the name of your stack')

        client = boto3.client("cloudformation")

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name} \n" f'Please make sure a stack with the name "{stack_name}" exists'
            ) from e

        stacks = response["Stacks"]
        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == "APIEndPoint"]

        if not api_outputs:
            raise KeyError(f"APIEndPoint not found in stack {stack_name}")

        # return api_outputs[0]["OutputValue"]  # Extract url from stack outputs

        return "https://zdl60g849c.execute-api.us-east-1.amazonaws.com/Stage"

    @pytest.fixture()
    def test_login(self, api_gateway_url):
        """ Call login endpoint and check response """
        body = {
            "username": "llquillo+1@spectrumone.co",
            "password": "Passw0rd!"
        }
        login_url = api_gateway_url + '/login'

        response = requests.post(
            login_url, json=body
        )
        response_json = response.json()

        assert response.status_code == 200
        assert response_json["access_token"] is not None

        return response_json["access_token"]

    def test_get_user(self, api_gateway_url, test_login):
        params = {
            'user_id': 1
        }
        header = {
            "Authorization": "Bearer " + test_login
        }
        get_url = api_gateway_url + '/hello'

        response = requests.get(
            get_url,
            params=params,
            headers=header
        )
        assert response.status_code == 200

    def test_update_user(self, api_gateway_url, test_login):
        params = {
            'user_id': 1
        }
        header = {
            "Authorization": "Bearer " + test_login
        }
        body = {
            "updated_email": "llquillo+1@spectrumone.co",
        }

        update_url = api_gateway_url + '/update'

        response = requests.patch(
            update_url,
            params=params,
            headers=header,
            json=body
        )
        assert response.status_code == 204

    def test_upload_to_bucket(self, api_gateway_url, test_login):
        get_upload_url = api_gateway_url + '/upload'
        header = {
            "Authorization": "Bearer " + test_login,
            "Content-Type": "application/binary"
        }
        body = {
            "filename": "test_pdf.pdf",
        }

        response = requests.post(
            get_upload_url,
            headers=header,
            json=body
        )
        response_json = response.json()

        assert response.status_code == 200

        upload_url = response_json["url"]

        cwd = os.getcwd()
        file_path = cwd + '/tests/integration/dummy_pdf.pdf'

        response = requests.put(
            upload_url,
            headers=header,
            data=open(file_path, 'rb')
        )

        assert response.status_code == 200
