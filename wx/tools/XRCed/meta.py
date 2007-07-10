# Name:         meta.py
# Purpose:      
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      05.07.2007
# RCS-ID:       $Id: core.py 47129 2007-07-04 22:38:37Z ROL $

from globals import g
from component import *

# Test

TRACE('*** creating meta components')

### Plugin

c = SimpleComponent(
    'Component', ['component'],
    ['provider', 'version', 'url',
     'groups', 'attributes', 'styles', 'has-name',
     'DL', 'module', 'handler',
     'menu', 'label', 'help', 'index',
     'panel', 'icon', 'pos', 'span'],
    specials={'provider': AttributeAttribute,
              'version': AttributeAttribute,
              'url': AttributeAttribute,
              'groups': ContentAttribute,
              'attributes': ContentAttribute,
              'styles': ContentAttribute},
    params={'provider': params.ParamLongText,
            'url': params.ParamLongText,
            'groups': params.ParamContent,
            'attributes': params.ParamContent,
            'styles': params.ParamContent,
            'icon': params.ParamImage,
            'has-name': params.ParamBool,
            'handler': params.ParamLongText,
            'index': params.ParamInt,
            'pos': params.ParamPosSize, 
            'span': params.ParamPosSize})

Manager.register(c)
Manager.setMenu(c, 'TOP_LEVEL', 'component', 'component plugin')
