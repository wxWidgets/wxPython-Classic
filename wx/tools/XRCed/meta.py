# Name:         meta.py
# Purpose:      
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      05.07.2007
# RCS-ID:       $Id: core.py 47129 2007-07-04 22:38:37Z ROL $

from component import *

# Test

TRACE('*** creating meta components')

### Plugin

c = SimpleComponent(
    'Component', ['component'],
    ['groups', 'attributes', 'styles', 'has_name',
     'menu', 'item', 'help',
     'panel', 'bitmap'],
    specials={'groups': ContentAttribute,
              'attributes': ContentAttribute,
              'styles': ContentAttribute,
              'bitmap': BitmapAttribute},
    params={'groups': params.ParamContent,
            'attributes': params.ParamContent,
            'styles': params.ParamContent,
            'has_name': params.ParamBool})

Manager.register(c)
Manager.setMenu(c, 'TOP_LEVEL', 'component', 'component plugin')
