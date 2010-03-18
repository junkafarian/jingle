from repoze.bfg.router import make_app
from repoze.zodbconn.finder import PersistentApplicationFinder

def app(global_config, **kw):
    """ This function returns a repoze.bfg.router.Router object.
        
        It is usually called by the PasteDeploy framework during ``paster serve``.
        
        >>> from repoze.bfg.router import Router
        >>> app({})
        Traceback (most recent call last):
        ...
        ValueError: No 'zodb_uri' in application configuration.
        
        #>>> isinstance(app({}, zodb_uri='/tmp/tmp.fs'), Router) # currently fails based on multiple configuration init
        #True
        
    """
    # paster app config callback
    import jingle
    from jingle.models import AppMaker
    zodb_uri = kw.get('zodb_uri')
    if zodb_uri is None:
        raise ValueError("No 'zodb_uri' in application configuration.")
    
    zodb_base = kw.get('zodb_base', 'root')
    
    appmaker = AppMaker(zodb_base)
    get_root = PersistentApplicationFinder(zodb_uri, appmaker)
    return make_app(get_root, jingle, options=kw)
