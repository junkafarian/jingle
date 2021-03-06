import formencode
from formencode.validators import UnicodeString
from formencode.declarative import DeclarativeMeta
from repoze.component import Registry
import sys

registry = Registry()

### Exceptions ###

class InvalidSchema(Exception):
    """ A marker exception for Schemas which are not stored in the registry,
        or do not provide required behaviour.
    """
    pass

class SchemaMeta(DeclarativeMeta):
    def __new__(meta, name, bases, attrs):
        cls = DeclarativeMeta.__new__(meta, name, bases, attrs)
        behaviour = attrs.get('behaviour')
        if behaviour is None:
            raise InvalidSchema('A Schema must provide some behaviour')
        registry.register(behaviour, cls())
        return cls

class Schema(formencode.Schema):
    """ Augmented `formencode.Schema` object to provide the ability to process
        multiple forms by restricting the validated data to keys beginning
        with the `prefix` attribute.
        
        Schemas must define which behaviour they provide::
        
            >>> from formencode.validators import UnicodeString
            >>> class TestSchemaNoBehaviour(Schema):
            ...     title = UnicodeString()
            Traceback (most recent call last):
            ...
            InvalidSchema: A Schema must provide some behaviour
        
        Once configured, they behave like regular formencode.Shema() objects
        
            >>> class TestSchema(Schema):
            ...     behaviour = 'test'
            ...     title = UnicodeString(default=u'',
            ...                           not_empty=True)
            >>> s = TestSchema()
            >>> s.to_python({})
            Traceback (most recent call last):
            ...
            Invalid: title: Missing value
            >>> s.to_python({})
            Traceback (most recent call last):
            ...
            Invalid: title: Missing value
            >>> s.to_python({'title':u'Test Title'})
            {'title': u'Test Title'}
            >>> s.to_python({'title': u'Test Title'})
            {'title': u'Test Title'}
            >>> s.to_python({'title':u'Test Title', 'extra_field':u'A field not in the schema'})
            {'title': u'Test Title'}
        
        It is also possible to process prefixed data dictionaries.
        (Useful for POSTs with multiple forms)
        
            >>> s.to_python({'test.title':u'Test Title', 'test.extra_field':u'A field not in the schema'})
            Traceback (most recent call last):
            ...
            Invalid: title: Missing value
            >>> s.to_python({'test.title':u'Test Title', 'test.extra_field':u'A field not in the schema'}, prefix='test.')
            {'title': u'Test Title'}
        
    """
    
    __metaclass__ = SchemaMeta
    
    behaviour = 'none'
    
    allow_extra_fields = True
    filter_extra_fields = True
    
    def to_python(self, value_dict, state=None, prefix=''):
        from jingle.utils import remove_dict_prefix
        return super(Schema, self).to_python(remove_dict_prefix(prefix, value_dict), state)
    


class Page(Schema):
    behaviour = 'page'
    
    title = UnicodeString(default=u'',
                          not_empty=True)
    content = UnicodeString(default=u'',
                            not_empty=True)


