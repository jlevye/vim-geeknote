#!/usr/bin/python3

import vim
import os
import re

user = os.geteuid()
os.seteuid(0)

from past import autotranslate
import sys
sys.path.append("/usr/local/lib/python2.7/dist-packages/geeknote-0.2a0-py2.7.egg/")
sys.path.append("/usr/local/lib/python2.7/dist-packages/thrift-0.9.3-py2.7-linux-x86_64.egg")
autotranslate(["geeknote","geeknote.out","geeknote.editor","thrift"])

from geeknote.out    import *
from geeknote.editor import Editor

os.seteuid(user)
from bs4             import BeautifulSoup

def ENMLtoText(contentENML):
    format = 'vim-default'
    if int(vim.eval('exists("g:GeeknoteFormat")')):
        format = vim.eval('g:GeeknoteFormat')

    if format == 'pre':
        print('WARNING: g:GeeknoteFormat=pre is deprecated.')

    if format == 'vim-default' or format == 'pre':
        try:
            soup = BeautifulSoup(contentENML.decode('utf-8'))
            sections = soup.select('pre')
            if len(sections) >= 1:
                content = ''
                for c in sections[0].contents:
                    content = u''.join((content, c))
                content = re.sub(r' *\n', os.linesep, content)
                content = content.replace('&lt;', '<')
                content = content.replace('&gt;', '>')
                content = content.replace('&amp;', '&')
                return content.encode('utf-8')
        except:
            pass
            # fall-through
    return Editor.ENMLtoText(contentENML)

def textToENML(content):
    format = 'vim-default'
    if int(vim.eval('exists("g:GeeknoteFormat")')):
        format = vim.eval('g:GeeknoteFormat')

    if format == 'pre':
        print('WARNING: g:GeeknoteFormat=pre is deprecated.')

    if format != 'vim-default' and format != 'pre':
        return Editor.textToENML(content, True, format)

    content = content.replace('<', '&lt;')
    content = content.replace('>', '&gt;')
    content = content.replace('&', '&amp;')
    content = unicode(content, "utf-8")
    contentHTML = u''.join(('<pre>', content, '</pre>')).encode("utf-8")

    enml = Editor.wrapENML(contentHTML)
    return enml
