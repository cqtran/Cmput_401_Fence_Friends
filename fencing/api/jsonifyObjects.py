from flask.json import JSONEncoder
from database.models import User, Customer, Status, Project, Quote, Picture, Material, Layout, Appearance

class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {
                'id' : obj.id,
                'username' : obj.username,
                'email' : obj.email,
                'company_name' : obj.company_name,
                'active' : obj.active,
                'confirmed_at' : dump_datetime(obj.confirmed_at)
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
                'status_name'         : obj.status_name,
                'status_number'       : obj.status_number
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
                'project_name'       : obj.project_name,
                'layout_selected'    : obj.layout_selected,
    			'appearance_selected': obj.appearance_selected
            }

        if isinstance(obj, Layout):
            return {
                'layout_id'               : obj.layout_id,
                'project_id'              : obj.project_id,
                'layout_name'             : obj.layout_name,
                'layout_info'             : obj.layout_info
            }

        if isinstance(obj, Picture):
            return {
                'picture_id'                : obj.picture_id,
                'project_id'                : obj.project_id,
                'file_name'                 : obj.file_name,
                'thumbnail_name'            : obj.thumbnail_name,
                'upload_date'               : dump_datetime(obj.upload_date)
            }

        if isinstance(obj, Material):
            return {
                'material_id'           : obj.material_id,
                'material_name'         : obj.material_name,
                'my_price'              : str(obj.my_price),
                'pieces_in_bundle'      : str(obj.pieces_in_bundle),
                'category'              : obj.category,
                'note'                  : obj.note,
                'company_name'          : obj.company_name
            }

        if isinstance(obj, Appearance):
            return {
                'appearance_id'         : obj.appearance_id,
                'appearance_name'       : obj.appearance_name,
                'project_id'            : obj.project_id,
                'panel_gap'             : obj.panel_gap,
                'height'                : obj.height
                #TODO: Define other columns related to materials
            }

        return super(MyJSONEncoder, obj).default(obj)

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing"""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d")]
