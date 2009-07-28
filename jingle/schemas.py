import formencode
from formencode.validators import UnicodeString
from repoze.component import Registry
import sys

registry = Registry()

class Schema(formencode.Schema):
    """ Augmented `formencode.Schema` object to provide the ability to process
        multiple forms by restricting the validated data to keys beginning
        with the `prefix` attribute.
        
        >>> from formencode.validators import UnicodeString
        >>> class TestSchema(Schema):
        ...     title = UnicodeString(default=u'',
        ...                           not_empty=True)
        >>> s = TestSchema()
        >>> s.to_python({})
        Traceback (most recent call last):
        ...
        Invalid: title: Missing value
        >>> s.validate({})
        Traceback (most recent call last):
        ...
        Invalid: title: Missing value
        >>> s.to_python({'title':u'Test Title'})
        {'title': u'Test Title'}
        >>> s.validate({'title': u'Test Title'})
        {'title': u'Test Title'}
        >>> s.validate({'title':u'Test Title', 'extra_field':u'A field not in the schema'})
        {'title': u'Test Title'}
        >>> s.to_python({'test.title':u'Test Title', 'test.extra_field':u'A field not in the schema'})
        Traceback (most recent call last):
        ...
        Invalid: title: Missing value
        >>> s.validate({'test.title':u'Test Title', 'test.extra_field':u'A field not in the schema'}, prefix='test.')
        {'title': u'Test Title'}
        
    """
    
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

