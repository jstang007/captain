import json

string = {
  "args": {
    "name": "nginx-deployment",
    "namespace": "default"
  }
}

args = string.get('args')
for arg in args:
    print(arg)


