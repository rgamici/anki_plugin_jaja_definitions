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
import threading
import traceback


# Variables
# Edit these field names if necessary =========================================
expressionField = 'Japanese'
jap_defField = 'JapaneseDefinition'
# ==============================================================================
max_threads = 15
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
            defText = re.sub('^.{1,10}読み方：[^ ]{1,20} +', '', defText)
            defText = re.sub(' *» 類語の一覧を見る *', '', defText)
            defText = re.sub(' *>>『三省堂 大辞林 第三版』の表記' +
                             '・記号についての解説を見る', '', defText)
            defText = re.sub('「.{1,10}」に似た言葉',
                             '<br/><b>似た言葉：</b>　', defText)
    return defText
# Update note =================================================================


class Regen():
    def __init__(self, ed, fids):
        self.ed = ed
        self.fids = fids
        self.completed = 0
        self.sema = threading.BoundedSemaphore(max_threads)
        self.values = {}
        if len(self.fids) == 1:  # Single card selected
            self.row = self.ed.currentRow()
            self.ed.form.tableView.selectionModel().clear()
        mw.progress.start(max=len(self.fids), immediate=True)
        mw.progress.update(
            label='Generating Japanese definitions...',
            value=0)

    def prepare(self):
        fs = [mw.col.getNote(id=fid) for fid in self.fids]
        for f in fs:
            try:
                if f[jap_defField]:
                    self.completed += 1
                    mw.progress.update(
                        label='Generating Japanese definitions...',
                        value=self.completed)
                else:
                    word = f[expressionField]
                    thread = threading.Thread(target=self.fetch_def,
                                              args=(word,))
                    self.values[word] = {}
                    self.values[word]['f'] = f
                    self.values[word]['thread'] = thread
                    thread.start()
            except:
                print('definitions failed:')
                traceback.print_exc()

    def fetch_def(self, word):
        with self.sema:
            definition = fetchDef(word)
            self.values[word]['definition'] = definition

    def wait_threads(self):
        for word, info in self.values.items():
            thread = self.values[word]['thread']
            thread.join()
            self.update_def(word)
        mw.progress.finish()
        if len(self.fids) == 1:
            self.ed.form.tableView.selectRow(self.row)

    def update_def(self, word):
        definition = self.values[word]['definition']
        f = self.values[word]['f']
        try:
            f[jap_defField] = definition
        except:
            print('definitions failed:')
            traceback.print_exc()
        try:
            f.flush()
        except:
            raise Exception()
        self.completed += 1
        mw.progress.update(
            label='Generating Japanese definitions...',
            value=self.completed)


def setupMenu(ed):
    a = QAction('Regenerate Japanese definitions', ed)
    a.triggered.connect(lambda _, e=ed: onRegenGlosses(e))
    ed.form.menuEdit.addAction(a)


def onRegenGlosses(ed):
    n = "Regenerate Ja-Ja definitions"
    regen = Regen(ed, ed.selectedNotes())
    regen.prepare()
    regen.wait_threads()
    mw.requireReset()


addHook('browser.setupMenus', setupMenu)
