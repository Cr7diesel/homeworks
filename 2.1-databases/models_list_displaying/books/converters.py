from datetime import datetime


class PubDateConverter:
    regex = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
    format = '%Y-%m-%d'

    def to_python(self, value):
        return datetime.date(datetime.strptime(value, self.format))

    def to_url(self, value):
        return datetime.strftime(value, self.format)
