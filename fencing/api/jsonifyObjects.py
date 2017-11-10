from flask.json import JSONEncoder
from database.models import User, Customer, Status, Project, Quote, Picture, Material

class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {
                'id' : obj.id,
                'username' : obj.username,
                'email' : obj.email,
                'company_name' : obj.company_name,
                'active' : obj.active
            }
        if isinstance(obj, Customer):
            return {
            	'customer_id': obj.customer_id,
                'email': obj.email,
                'first_name': obj.first_name,
                'cellphone': obj.cellphone,
                'company_name': obj.company_name,
            }

        if isinstance(obj, Status):
            return {
                'status_name'         : obj.status_name
            }

        if isinstance(obj, Project):
            return {
                'project_id'         : obj.project_id,
                'customer_id'        : obj.customer_id,
                'status_name'        : obj.status_name,
                'address'            : obj.address,
                'start_date'         : dump_datetime(obj.start_date),
                'end_date'           : dump_datetime(obj.end_date),
                'note'               : obj.note,
                'project_name'       : obj.project_name
            }

        if isinstance(obj, Quote):
            return {
                'quote_id'                : obj.quote_id,
                'project_id'              : obj.project_id,
                'quote'                   : obj.quote,
                'project_info'            : obj.project_info,
                'note'                    : obj.note,
                'last_modified'           : dump_datetime(obj.last_modified)
            }

        if isinstance(obj, Picture):
            return {
                'picture_id'                : obj.picture_id,
                'project_id'                : obj.project_id,
                'file_name'                 : obj.file_name
            }

        if isinstance(obj, Material):
            # TODO
            return{}

        return super(MyJSONEncoder, obj).default(obj)

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing"""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d")]
