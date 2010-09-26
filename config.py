#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
module: config
"""
import json
    
DEFAULTS = {
    'splash':False,
    'w': 10,
    'h': 10,
    'mines': 1,
    'scores': [],
    }

DEFAULT_SAVE_FILE = "config.cfg"

class _Conf:
    def __getattr__(self,name):
        return DEFAULTS[name]

    def __setattr__(self,name,value):
        if type(value) != type(DEFAULTS[name]):
            raise Exception("%s %s is not %s:" % 
                            (value, type(value), type(DEFAULTS[name])))
        DEFAULTS[name] = value

    def save(self,fileName=DEFAULT_SAVE_FILE):
        with open(fileName, 'w+') as fp:
            json.dump(DEFAULTS, fp, indent=True)
            
    def load(self,fileName=DEFAULT_SAVE_FILE):
        with open(fileName, 'r') as fp:
            global DEFAULTS
            DEFAULTS = json.load(fp)

conf = _Conf()
try:
    conf.load()
except:
    pass

def test():
    """
    >>> c = conf
    >>> c.splash = True
    >>> c.splash == True
    True

    >>> c.save()
    >>> c.splash = False

    >>> c.load()
    >>> c.splash == True
    True
    """
    import doctest
    doctest.testmod()

def main():
    test()
    pass

if __name__=="__main__":
    main()

