
import base64
import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    method: str
    url: str
    headers: dict
    data: str
    other: dict


@app.get("")
def index():
    return {"message": "Hello World"}

@app.post("/url")
def psst_url(item: Item):
    _kwargs = dict()
    if item.headers:
        _kwargs['headers'] = item.headers
    if item.data:
        _kwargs['data'] = base64.b64decode(item.data.encode())
    if item.other:
        _kwargs.update(item.other)
    if 'timeout' not in _kwargs:
        _kwargs['timeout'] = 30
    response_dict = {
        'success': False,
        'request': dict(),
        'response': dict()
    }
    try_count = 0
    response = None
    while try_count < 5:
        try:
            response = requests.request(item.method, item.url, **_kwargs)
            break
        except:
            try_count += 1
    if response is None:
        return response_dict
    response_dict['success'] = True
    response_dict['request']['method'] = response.request.method
    response_dict['request']['url'] = response.request.url
    response_dict['request']['body'] = base64.b64encode(response.request.body).decode() if response.request.body else ''
    response_dict['request']['headers'] = dict(response.request.headers)
    response_dict['response']['status_code'] = response.status_code
    response_dict['response']['url'] = response.url
    response_dict['response']['headers'] = dict(response.headers)
    response_dict['response']['body'] = base64.b64encode(response.content).decode()
    return response_dict
