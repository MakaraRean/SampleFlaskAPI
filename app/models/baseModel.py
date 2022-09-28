import json

from sqlalchemy.orm import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError as e:
                    error_message = e.args[0]
                    if error_message == 'Object of type datetime is not JSON serializable':
                        fields[field] = data.strftime('%Y-%m-%d %H:%M:%S')
                    elif error_message == 'Object of type Decimal is not JSON serializable':
                        fields[field] = float(data)
                    else:
                        fields[field] = None

            return fields
        return json.JSONEncoder.default(self, obj)
