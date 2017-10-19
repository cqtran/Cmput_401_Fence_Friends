from flask.json import JSONEncoder
from Python.models import Customer

class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Customer):
            return {
            	'customer_id': obj.customer_id,
                'email': obj.email,
                'first_name': obj.first_name,
                'last_name': obj.last_name,
                'cellphone': obj.cellphone,
                'company_name': obj.company_name,
            }
        return super(MyJSONEncoder, self).default(obj)