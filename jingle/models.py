from formencode import Invalid
from persistent import Persistent
from persistent.mapping import PersistentMapping
from persistent.dict import PersistentDict
from persistent.list import PersistentList
import schemas

from jingle import config
from jingle.utils import normalise_title

class Page(Persistent):
    __name__ = None
    __parent__ = None
    __children__ = []
    
    title = u''
    
    layout_template = u''
    
    _default_behaviour = config['DEFAULT_PAGE_BEHAVIOUR']
    
    def __init__(self, title):
        self.title = title
        self.__name__ = normalise_title(title)
        self._properties = PersistentDict({})
        self._extra_behaviour = PersistentList([])
        
        self._update_properties()
    
    ### Behaviour ###
    
    @property
    def behaviour(self):
        """ Collates the default and user-added behaviour into a list
            
            >>> page = Page('test')
            >>> page.behaviour == list(page._default_behaviour) + list(page._extra_behaviour)
            True
        """
        return list(self._default_behaviour) + list(self._extra_behaviour)
    
    def add_behaviour(self, key, data=None, prefix=''):
        """ Adds additional behaviour as defined by a Schema object
            
            >>> page = Page('test')
            >>> page.add_behaviour('test')
            Traceback (most recent call last):
            ...
            InvalidSchema: There is no Schema registered to provide `test`
            >>> from jingle.schemas import registry, Schema
            >>> from formencode.validators import UnicodeString
            >>> class TestSchema(Schema):
            ...     title = UnicodeString(default=u'',
            ...                           not_empty=True)
            >>> registry.register('test', TestSchema())
            >>> page.add_behaviour('test')
            ['page', 'test']
            
        """
        if key not in schemas.registry:
            raise schemas.InvalidSchema('There is no Schema registered to provide `%s`' % key)
        elif key not in self.behaviour:
            self._extra_behaviour.append(key)
            self._update_properties()
            if data is not None:
                return self.update(key, data, prefix)
        return self.behaviour
    
    def remove_behaviour(self, key):
        if key in self._extra_behaviour:
            self._extra_behaviour.remove(key)
        elif key in self._default_behaviour:
            raise Exception('Cannot remove default behaviour')
        return self.behaviour
    
    ### Properties ###
    
    def _update_properties(self):
        for behaviour in self.behaviour:
            schema = schemas.registry.lookup(behaviour)
            for field, ob in schema.fields.items():
                key = '%s.%s' % (behaviour, field)
                if key not in self._properties.keys():
                    self._properties[key] = ob.default
    
    @property
    def properties(self):
        # really should move this to update events on self.extra_behaviour
        self._update_properties()
        return dict(self._properties)
    
    def update(self, key, data, prefix=''):
        if key not in self.behaviour:
            return dict(self._properties)
        schema = schemas.registry.lookup(key)
        formatted = schema.validate(data, prefix=prefix)
        for k,v in formatted.items():
            self._properties['%s.%s' % (key, k)] = v
        return self._properties
    
    
    ### Navigation / Hierarchy ###
    
    def add_child(self, child):
        """ This method will process setting / syncing the __parent__ and children attributes
        """
        if not isinstance(child, Page):
            raise TypeError('Children must be inherited from the Page class, not %s' % type(child))
        self.__children__.append(child.__name__)
        child.__parent__ = self.__name__
        return self.__children__
    


class Root(PersistentMapping):
    __parent__ = __name__ = None
    
    def __setitem__(self, name, value):
        value.__name__ = name
        super(Root, self).__setitem__(name, value)
    

def appmaker(zodb_root):
    if not 'root' in zodb_root:
        from data import page_defaults
        app_root = Root()
        home = Page('Home')
        home.layout_template = u'master.html'
        home.update('page', page_defaults.get('home', {'title': u'Home'}))
        app_root['home'] = home
        zodb_root['root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['root']
