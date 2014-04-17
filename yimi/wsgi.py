#!/usr/bin/env python
#coding:utf8

import os
import sys
reload(sys)

sys.setdefaultencoding('utf-8')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yimi.settings")

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
