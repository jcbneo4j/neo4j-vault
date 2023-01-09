# neo4j-vault
The following tool shows how to start up vault, add a secret, spin up neo4j and dynamically update the neo4j user password with a secret from vault. The local requirements will be the vault client and the hvac (Hashicorp Vault) and neo4j Pyhton driver libraries, which can be installed as follows:

`brew install vault`

`python3 -m pip install hvac`
`python3 -m pip install neo4j`

## start up vault docker-compose

`docker compose up`

## Next, initialize Vault and copy keys and root token

`vault operator init -key-shares=6 -key-threshold=3`

Unseal Key 1: cxMGksQLpvRPVaztgKvI1gurekNSmlsLenNZzdOmYZTs
Unseal Key 2: Y254MZgCWnK9f6d7N12RTTXp69LgtuG/m5SOyM4vppl8
Unseal Key 3: bKUrg4rIi75WSFH5ergBROZJ5mbNvdPKWqXBfafGwvA4
Unseal Key 4: nMV+EzPrURZ/6FK22hSm9siK1peu9GVRlUMmsY44ZtA5
Unseal Key 5: mTPuyeMlKERa6K9+1vSQk/1uhz8gO0L4g/gLa5pD2BmB
Unseal Key 6: duWWSBTF36ZqVVEljEv+sz5PK+vcVXyibMh0F8fd311U

Initial Root Token: hvs.uH7grZMLOEeMqnsK41Fbm2BU

Vault initialized with 6 key shares and a key threshold of 3. Please securely
distribute the key shares printed above. When the Vault is re-sealed,
restarted, or stopped, you must supply at least 3 of these keys to unseal it
before it can start servicing requests.

Vault does not store the generated root key. Without at least 3 keys to
reconstruct the root key, Vault will remain permanently sealed!

It is possible to generate new unseal keys, provided you have a quorum of
existing unseal keys shares. See "vault operator rekey" for more information.

## perform unseal operation on vault with 3 of the 5 tokens
`vault operator unseal Y254MZgCWnK9f6d7N12RTTXp69LgtuG/m5SOyM4vppl8`

`vault operator unseal nMV+EzPrURZ/6FK22hSm9siK1peu9GVRlUMmsY44ZtA5`

`vault operator unseal duWWSBTF36ZqVVEljEv+sz5PK+vcVXyibMh0F8fd311U`

## check vault status
`vault status`

## login to vault
`vault login hvs.uH7grZMLOEeMqnsK41Fbm2BU`

## enable kv secrets
`vault secrets enable -version=1 -path=secret kv`

## create neo4j secret for new password
`vault kv put secret/neo4j/password password=password123`

## start up neo4j docker container
`docker run \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$HOME/neo4j/data:/data \
    neo4j`

## run vault neo4j utility. will prompt for current neo4j password (e.g. password) and will update to password in vault secret:
`python3 neo4j-vault.py`
Note: update the hard-coded vault token in the module.
