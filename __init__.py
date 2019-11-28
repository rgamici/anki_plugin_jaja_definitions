# -*- mode: Python ; coding: utf-8 -*-
#
# https://github.com/steviepoppe/anki_plugin_remove_missing_audio_references
# Authors: Stevie Poppe
#
# Description: Plugin to add Japanese translations on Korean vocabulary,
# based on the Sanseido Definitions plugin for Anki
# pulls definitions from Weblio's KJ-JK dictionary.

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
expressionField = 'Korean'
jap_transField = 'Japanese'
# ==============================================================================

# Fetch definition from Weblio ================================================


def fetchDef(term):
    defText = ""
    pageUrl = ("http://kjjk.weblio.jp/content/"
               + urllib.parse.quote(term.encode('utf-8')))
    response = urllib.request.urlopen(pageUrl)
    soup = BeautifulSoup(response)
    NetDicBody = soup.find('div', class_="kiji")

    if NetDicBody is not None:
        test = NetDicBody.find_all('span', {"lang": "ja"})
        counter = 1

        if test is not None:
            for line in test:
                if str(line).find(term) == -1:
                    defText += "(" + str(counter) + ") " + str(line) + "<br/>"
                    counter = counter + 1

    if defText != "":
        defText = string.replace(defText, ',', ', ')
    return defText

# Update note =================================================================


def glossNote(f):
    if f[jap_transField]:
        return
    f[jap_transField] = fetchDef(f[expressionField])


def setupMenu(ed):
    a = QAction('Regenerate KJ definitions', ed)
    a.triggered.connect(lambda e=ed: onRegenGlosses(e))
    ed.form.menuEdit.addAction(a)


def onRegenGlosses(ed):
    n = "Regenerate KJ definitions"
    ed.editor.saveNow()
    regenGlosses(ed, ed.selectedNotes())
    mw.requireReset()


def regenGlosses(ed, fids):
    mw.progress.start(max=len(fids), immediate=True)
    for (i, fid) in enumerate(fids):
        mw.progress.update(label='Generating KJ definitions...', value=i)
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
