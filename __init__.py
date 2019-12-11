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
    pageUrl = ("http://www.weblio.jp/content/"
               + urllib.parse.quote(term.encode('utf-8')))
    response = urllib.request.urlopen(pageUrl)
    soup = BeautifulSoup(response, features="html.parser")
    NetDicBody = soup.find('div', {'class': "kiji"})

    if NetDicBody is not None:
        mult_def = NetDicBody.find_all('span', {'style': "text-indent:0;"})
        counter = 1

        if mult_def != []:
            for line in mult_def:
                if line.find('span', {'style': "text-indent:0;"}) is None:
                    defText += ("<b>(" + str(counter) + ")</b> "
                                + line.get_text().strip() + "<br/>")
                    counter = counter + 1
        else:
            defText = NetDicBody.get_text().strip()
            # remove entry header (ends with "】 *")
            defText = re.sub('^.*】 *', '', defText)
            defText = re.sub(' *» 類語の一覧を見る *', '', defText)
            defText = re.sub(' *>>『三省堂 大辞林 第三版』の表記' +
                             '・記号についての解説を見る', '', defText)
            defText = re.sub('「' + term + '」に似た言葉',
                             '<br/><b>似た言葉：</b>　', defText)
    return defText
# Update note =================================================================


def glossNote(f):
    if f[jap_defField]:
        return
    f[jap_defField] = fetchDef(f[expressionField])


def setupMenu(ed):
    a = QAction('Regenerate Japanese definitions', ed)
    a.triggered.connect(lambda _, e=ed: onRegenGlosses(e))
    ed.form.menuEdit.addAction(a)


def onRegenGlosses(ed):
    n = "Regenerate Ja-Ja definitions"
    regenGlosses(ed, ed.selectedNotes())
    mw.requireReset()


def regenGlosses(ed, fids):
    mw.progress.start(max=len(fids), immediate=True)
    for (i, fid) in enumerate(fids):
        mw.progress.update(label='Generating Japanese definitions...', value=i)
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
