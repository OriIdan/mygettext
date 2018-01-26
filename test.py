#!/usr/python
# -*- coding: utf-8 -*-
#
# Demo of using mygettext
# This file shows how to use the mygettext module
#
# Written by: Ori Idan <ori@heliconbooks.com>
import mygettext

mygettext.init('messages', 'he_IL', 'locales')

_ = mygettext.gettext

print _("Choose group")

