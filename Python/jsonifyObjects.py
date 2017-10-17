from flask.json import JSONEncoder
from Python.models import Customer

class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Customer):
            return {
                'email': obj.email,
                'first_name': obj.first_name,
                'cellphone': obj.cellphone,
            }
        return super(MyJSONEncoder, self).default(obj)

