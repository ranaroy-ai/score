import os
import logging
import json
import numpy
import joblib
import mlflow
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication

def init():
    """
    This function is called when the container is initialized/started, typically after create/update of the deployment.
    You can write the logic here to perform init operations like caching the model in memory
    """
    global model
    KEY_VAULT_URL = "https://kv-amlfrauddev.vault.azure.net/"

    # Replace with your secret name
    SECRET_NAME = "ContainerName"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
    logging.error(f">>>>>>>>>>>>>>>>>>>>>>>>>>> {credential}")
    # Retrieve the secret
    secret = client.get_secret(SECRET_NAME)
    secret_client_id = client.get_secret("client-id")
    secret_client_sec = client.get_secret("client-secret")
    secret_tenant_id = client.get_secret("tenant-id")
    secret_subscription = client.get_secret("subscription-id")
    secret_value = secret.value
    secret_client_id_value = secret_client_id.value
    secret_client_sec_value = secret_client_sec.value
    secret_tenant_id_value = secret_tenant_id.value
    secret_subscription_value = secret_subscription.value
    os.environ["AZURE_TENANT_ID"] = secret_tenant_id_value
    os.environ["AZURE_CLIENT_ID"] = secret_client_id_value
    os.environ["AZURE_CLIENT_SECRET"] = secret_client_sec_value
    os.environ["AZURE_SUBSCRIPTION_ID"] = secret_subscription_value
    ab = os.getenv("AZURE_TENANT_ID")
    bc = os.getenv("AZURE_CLIENT_ID")
    cd= os.getenv("AZURE_CLIENT_SECRET")
    subs_id =os.getenv("AZURE_SUBSCRIPTION_ID")
    logging.error(f">>>>>>>>>>>>>>>>>>>>>>>>>>> {ab}")
    logging.error(f">>>>>>>>>>>>>>>>>>>>>>>>>>> {bc}")
    logging.error(f">>>>>>>>>>>>>>>>>>>>>>>>>>> {cd}")
    logging.info("Init complete")
    logging.error(f">>>>>>>>>>>>>>>>>>>>>>>>>>> {secret_value}")
    
    # Authenticate with Service Principal
    sp_auth = ServicePrincipalAuthentication(
        tenant_id=ab,
        service_principal_id=bc,
        service_principal_password=cd
    )
    
    # Load the workspace
    ws = Workspace(
        subscription_id=subs_id,
        resource_group="score-inference-group",
        workspace_name="aml-fraud-dev",
        auth=sp_auth
    )
    ml_uri = ws.get_mlflow_tracking_uri()
    mlflow.set_tracking_uri(ws.get_mlflow_tracking_uri())
    logging.error(f"????????????????????????????????{ml_uri}")
    # # AZUREML_MODEL_DIR is an environment variable created during deployment.
    # # It is the path to the model folder (./azureml-models/$MODEL_NAME/$VERSION)
    # Please provide your model's folder name if there is one
    model_path = os.path.join(
        os.getenv("AZUREML_MODEL_DIR"), "sklearn_regression_model.pkl"
    )
    # # deserialize the model file back into a sklearn model
    model = joblib.load(model_path)
    logging.info("Init complete")


def run(raw_data):
    """
    This function is called for every invocation of the endpoint to perform the actual scoring/prediction.
    In the example we extract the data from the json input and call the scikit-learn model's predict()
    method and return the result back
    """
    # logging.info("model 1: request received")
    # data = json.loads(raw_data)["data"]
    # data = numpy.array(data)
    # result = model.predict(data)
    # logging.info("Request processed")
    # return result.tolist()
