from dremio_simple_query.connect import get_token

login_endpoint = "http://173.212.237.61:9047/apiv2/login"

payload = {"userName": "admin", "password": "FatherOfTheYear()12"}

token = get_token(uri=login_endpoint, payload=payload)
print(token)
