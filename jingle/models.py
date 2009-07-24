from formencode import Invalid
from persistent import Persistent
from persistent.mapping import PersistentMapping
from persistent.dict import PersistentDict
import schemas

class Page(Persistent):
    __name__ = None
    __parent__ = None
    __children__ = []
    
    title = u''
    
    layout_template = u''
    
    _default_behaviour = ('page',)
    extra_behaviour = []
    
    def __init__(self, title):
        self.title = title
        self.__name__ = title.lower().replace(' ', '_')
        self._properties = PersistentDict({})
        self._update_properties()
    
    @property
    def behaviour(self):
        behaviour = []
        behaviour.extend(self._default_behaviour)
        behaviour.extend(self.extra_behaviour)
        return behaviour
    
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
    
    def update(self, key, data):
        if key not in self.behaviour:
            return dict(self._properties)
        schema = schemas.registry.lookup(key)
        formatted = schema.to_python(data)
        for k,v in formatted.items():
            self._properties['%s.%s' % (key, k)] = v
        return self._properties
    
    
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
