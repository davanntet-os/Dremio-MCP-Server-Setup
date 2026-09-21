from dremio_simple_query.connect import get_token

login_endpoint = "http://localhost:9047/apiv2/login"

payload = {"userName": "dremioadmin", "password": "dremio123"}

token = get_token(uri=login_endpoint, payload=payload)
print(token)
