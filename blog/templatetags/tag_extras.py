# -*- encoding:utf-8 -*-
from django import template
import re

register = template.Library()

@register.filter(is_safe=True)
def get_dict_value(key, dic):
    if dic:
        return dic.get(key)
    else:
        return ''

@register.filter(is_safe=True)
def cut_get_field(a, b):
    list_ = a.split('&')
    new_ = ''
    for l in list_:
        if l.split('=')[0] not in b and l:
           new_ += l + '&'
    return new_



@register.filter(is_safe=True)
def convert_to(a, b):
    if b == 'str':
        return str(b)
    elif b == 'int':
        return int(b)
