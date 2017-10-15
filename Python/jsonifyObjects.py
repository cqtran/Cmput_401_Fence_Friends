from flask.json import JSONEncoder

class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, EqltByGene):
            return {
                'gene_id': obj.gene_id, 
                'gene_symbol': obj.gene_symbol,
                'p_value': obj.p_value,
            }
        return super(MyJSONEncoder, self).default(obj)