from flask.json.provider import DefaultJSONProvider
import json
from bson import ObjectId

def convertForExport(data, to=True):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_value = convertForExport(value, to)
            if to and key == "_id":
                key = "id"
            elif not to and key == "id":
                key = "_id"
                new_val = ObjectId(new_val)
            new_dict[key] = new_value
        return new_dict
    elif isinstance(data, list):
        return [convertForExport(item, to) for item in data]
    else:
        return data
def convertForImport(data):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_value = convertForImport(value)
            if key == 'id':
                new_key = '_id'
                try:
                    new_value = ObjectId(new_value)
                except Exception as e:
                    print(f"Warning: Could not convert value {new_value} to ObjectId: {e}")
            else:
                new_key = key
            new_dict[new_key] = new_value
        return new_dict
    elif isinstance(data, list):
        return [convertForImport(item) for item in data]
    else:
        return data

class CustomJSONEncoder(json.JSONEncoder):
    """Extend json-encoder class"""
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # convert ObjectId to string
        return super(CustomJSONEncoder, self).default(obj)
class CustomJSONProvider(DefaultJSONProvider):
  def dumps(self, obj, **kwargs):
    obj = convertForExport(obj)
    return json.dumps(obj, **kwargs, cls=CustomJSONEncoder)

  def loads(self, s, **kwargs):
    obj = json.loads(s, **kwargs)
    obj = convertForImport(obj)
    return obj