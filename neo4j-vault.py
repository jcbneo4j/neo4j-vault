import hvac
import getpass
from neo4j import GraphDatabase

def get_secret(client):
  return client.read("secret/neo4j/password")["data"]["password"]

def get_vault_client():
  client = hvac.Client(
    url='http://127.0.0.1:8200',
    token='hvs.uH7grZMLOEeMqnsK41Fbm2BU',
  )
  return client

def get_driver(password):
  uri = "bolt://localhost:7687"
  return GraphDatabase.driver(uri, auth=("neo4j", password))

def update_neo4j_password(tx, secret, password):
  results = list(tx.run(f"ALTER CURRENT USER SET PASSWORD FROM '{password}' TO '{secret}'"))
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
  neopassword = getpass.getpass()
  client = get_vault_client()
  print("logged in vault...")
  secret = get_secret(client)
  print("obtained vault secret...")
  run_neo_tx("update_neo4j_password", "write", secret, neopassword)
  print("updated neo4j password with secret...")
