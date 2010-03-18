from webob.multidict import MultiDict

def normalise_title(title):
    """ convenience utility for deriving a url/commandline friendly version of a string.
        
        >>> title = 'Some Abstract title'
        >>> normalise_title(title)
        u'some_abstract_title'
    """
    return unicode(title.lower().replace(' ', '_'))

def add_dict_prefix(prefix, data):
    """ Adds `prefix` to all keys in `original_data`.
        
            >>> i = {'foo': 1, 'bar': 2}
            >>> add_dict_prefix('prefix.', i)
            {'prefix.foo': 1, 'prefix.bar': 2}
    """
    new_data = {}
    for k,v in data.items():
        new_data['%s%s' % (prefix,k)] = v
    return new_data

def remove_dict_prefix(prefix, original_data):
    new_value_dict = MultiDict()
    for k,v in original_data.items():
        if k.startswith(prefix):
            new_value_dict.add(k.replace(prefix,''), v)
    return new_value_dict


