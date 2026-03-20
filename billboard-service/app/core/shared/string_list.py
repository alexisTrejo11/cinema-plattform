import json
from sqlalchemy import TypeDecorator, Text


class StringList(TypeDecorator):
    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return '[]'

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return []