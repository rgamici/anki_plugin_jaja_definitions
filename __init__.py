# -*- mode: Python ; coding: utf-8 -*-
#
# https://github.com/rgamici/anki_plugin_jaja_definitions
# Authors: renato
#
# Description: Plugin to add Japanese definition on Japanese vocabulary,
# based on the Japanese Definitions for Korean Vocabulary plugin for Anki
# pulls definitions from Weblio's dictionary.

from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import urllib.error
import re
from aqt.utils import showInfo
import string
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from anki.hooks import addHook
from anki.notes import Note
from aqt import mw

# Edit these field names if necessary =========================================
expressionField = 'Japanese'
jap_defField = 'JapaneseDefinition'
# ==============================================================================

# Fetch definition from Weblio ================================================


def fetchDef(term):
    defText = ""
    pageUrl = ("http://weblio.jp/content/"
               + urllib.parse.quote(term.encode('utf-8')))
    response = urllib.request.urlopen(pageUrl)
    soup = BeautifulSoup(response, features="lxml")
    NetDicBody = soup.find('div', {'class': "kiji"})

    if NetDicBody is not None:
        mult_def = NetDicBody.find_all('span', {'style': "text-indent:0;"})
        counter = 1

        if mult_def != []:
            for line in mult_def:
                if line.find('span', {'style': "text-indent:0;"}) is None:
                    defText += ("(" + str(counter) + ") "
                                + line.get_text().strip() + "<br/>")
                    counter = counter + 1
        else:
            defText = NetDicBody.get_text().strip()

    return defText

# Update note =================================================================


def glossNote(f):
    if f[jap_defField]:
        return
    f[jap_defField] = fetchDef(f[expressionField])


def setupMenu(ed):
    a = QAction('Regenerate KJ definitions', ed)
    a.triggered.connect(lambda e=ed: onRegenGlosses(e))
    ed.form.menuEdit.addAction(a)


def onRegenGlosses(ed):
    n = "Regenerate Ja-Ja definitions"
    ed.editor.saveNow()
    regenGlosses(ed, ed.selectedNotes())
    mw.requireReset()


def regenGlosses(ed, fids):
    mw.progress.start(max=len(fids), immediate=True)
    for (i, fid) in enumerate(fids):
        mw.progress.update(label='Generating Ja-Ja definitions...', value=i)
        f = mw.col.getNote(id=fid)
        try:
            glossNote(f)
        except:
            import traceback
            print('definitions failed:')
            traceback.print_exc()
        try:
            f.flush()
        except:
            raise Exception()
        ed.onRowChanged(f, f)
    mw.progress.finish()


addHook('browser.setupMenus', setupMenu)
