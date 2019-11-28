# -*- mode: Python ; coding: utf-8 -*-
#
# https://github.com/rgamici/anki_plugin_jaja_definitions
# Authors: renato
#
# Description: Plugin to add Japanese definition on Japanese vocabulary,
# based on the Japanese Definitions for Korean Vocabulary plugin for Anki
# pulls definitions from Weblio's dictionary.

from bs4.BeautifulSoup import BeautifulSoup
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
    pageUrl = ("http://kjjk.weblio.jp/content/"  # change URL
               + urllib.parse.quote(term.encode('utf-8')))
    response = urllib.request.urlopen(pageUrl)
    soup = BeautifulSoup(response)
    NetDicBody = soup.find('div', class_="kiji")  # OK

    if NetDicBody is not None:
        test = NetDicBody.find_all('span', {"lang": "ja"})  # no such element
        counter = 1

        if test is not None:
            for line in test:
                if str(line).find(term) == -1:  # require better formating
                    defText += "(" + str(counter) + ") " + str(line) + "<br/>"
                    counter = counter + 1

    if defText != "":
        defText = string.replace(defText, ',', ', ')
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
