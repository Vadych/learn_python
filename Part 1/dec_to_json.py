import json

def to_json (fn):
    def ret_json(*arc, **kw):
        return json.dumps(fn(*arc,**kw))
    ret_json.__name__=fn.__name__
    return ret_json


@to_json
def get_data():
  return {
    'data': 42
  }
  
print (get_data())

