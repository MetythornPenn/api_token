## Secure FastAPI using API Key with reverse proxy 


### How to run service 

```bash
# generate key
python generate_api_key.py

# copy key to .env 
API_KEY = 

# build images
docker compose up -d --build

# test api with swagger 
http://localhost:2000/docs

```


### Reference

- [Medium article](https://nilsdebruin.medium.com/fastapi-authentication-revisited-enabling-api-key-authentication-122dc5975680)

- [Sebastián's code](https://gist.githubusercontent.com/nilsdebruin/a78c5e200e7df014a92580b4fc51c53f/raw/7f18229ab35f843fe603b45ec9f7cc5f2b3c8d57/fastapi_api_key.py)