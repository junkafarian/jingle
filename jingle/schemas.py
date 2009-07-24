import formencode
from formencode.validators import UnicodeString
from repoze.component import Registry
from repoze.component import provides
import sys

registry = Registry()

class Schema(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    
    def validate(self, value_dict, state=None, prefix=''):
        new_value_dict = dict([(k.replace(prefix,''),unicode(v)) for k,v in value_dict.items() if k.startswith(prefix)])
        return self.to_python(new_value_dict, state)
    


class Page(Schema):
    title = UnicodeString(default=u'',
                          not_empty=True)
    content = UnicodeString(default=u'',
                            not_empty=True)

registry.register('page', Page)

