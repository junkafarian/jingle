def normalise_title(title):
    """ convenience utility for deriving a url/commandline friendly version of a string.
        
        >>> title = 'Some Abstract title'
        >>> normalise_title(title)
        u'some_abstract_title'
    """
    return unicode(title.lower().replace(' ', '_'))
