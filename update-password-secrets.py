import boto3
import getpass
import json
from botocore.exceptions import ClientError
from neo4j import GraphDatabase

def get_secret():
  secret_name = "prod/test/test1"
  region_name = "us-east-1"

  # Create a Secrets Manager client
  session = boto3.session.Session()
  client = session.client(
    service_name='secretsmanager',
    region_name=region_name
  )

  try:
    get_secret_value_response = client.get_secret_value(
      SecretId=secret_name
    )
  except ClientError as e:
    raise e

  secret = get_secret_value_response['SecretString']
  return json.loads(secret)

def rotate_secret():
  secret_name = "prod/test/test1"
  region_name = "us-east-1"

  # Create a Secrets Manager client
  session = boto3.session.Session()
  client = session.client(
    service_name='secretsmanager',
    region_name=region_name
  )

  try:
    response = client.rotate_secret(
      SecretId=secret_name,
      RotationLambdaARN=""
    )
  except ClientError as e:
    raise e

  print(response)


def get_driver(password):
  uri = "bolt://localhost:7687"
  return GraphDatabase.driver(uri, auth=("neo4j", password))

def update_neo4j_password(tx, secret, passwd):
  results = list(tx.run(f"ALTER CURRENT USER SET PASSWORD FROM '{passwd}' TO '{secret}'"))
  for record in results:
    print(record)

def run_neo_tx(method_name, tx_type, secret, password):
  driver = get_driver(password)
  with driver.session(database="system") as session:
    if tx_type == "write":
      return session.write_transaction(eval(method_name), secret, password)
    elif tx_type == "read":
      return session.read_transaction(eval(method_name), secret, password)
  driver.close()

if __name__ == "__main__":
  rotate_secret()
  '''
  passwd = getpass.getpass()
  result = get_secret()
  secret = result["password"]
  print(f"secret: {secret}")
  run_neo_tx("update_neo4j_password", "write", secret, passwd)
  '''
