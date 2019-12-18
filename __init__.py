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


# Variables (can be edited on Addons > Config
config = mw.addonManager.getConfig(__name__)
expressionField = config['expressionField']
definitionField = config['definitionField']
keybinding = config['keybinding']

# Labels
# text shown while processing cards
label_progress_update = 'Generating Japanese definitions...'
# text shown on menu to run the functions
label_menu = 'Regenerate Japanese definitions'

# regex lists
# crawling correct page
crawling_list = [
    # [search_string, command, compiled_regex]
    ['名詞「(.*?)」に、接頭辞「.」がついたもの。','fetch', None],
    ['活用の動詞「(.*?)(?:する)?」の.*?形', 'fetch', None],
    ['出典: フリー百科事典『ウィキペディア（Wikipedia）』', '', None],
]

# parsing
parsing_list = [
    # [search_string, substitution, compiled_regex]
    ['^.*】 *', '', None],
    ['^.{1,10} ?読み方：[ぁ-んーア-ンａ-ｚＡ-Ｚ（）]+ *', '', None],
    [' *» 類語の一覧を見る *', '', None],
    [' *>>『三省堂 大辞林 第三版』の表記・記号についての解説を見る', '', None],
    ['「.{1,10}」に似た言葉', '<br/><b>似た言葉：</b>　', None],
]

# Fetch definition from Weblio ================================================


def fetchDef(term):
    defText = ""
    pageUrl = ("http://www.weblio.jp/content/"
               + urllib.parse.quote(term.encode('utf-8')))
    response = urllib.request.urlopen(pageUrl)
    soup = BeautifulSoup(response, features="html.parser")
    soup = soup.find('div', {'class': "kiji"})
    # looking for <div class=NetDicBody> would be simpler,
    # but it would lose the synomyms
    if soup is not None:
        if len(soup.find_all('div', {'class': 'NetDicBody'}, limit=2)) > 1:
            # some entries have two words inside it and a different structure
            # the second one looks bogus
            soup = soup.find('div', {'class': 'NetDicBody'})
        if soup.find('span', {'style': "text-indent:0;"}):
            # Definition is composed of multiple elements
            counter = 1
            for line in soup.find_all('span', {'style': "text-indent:0;"}):
                if line.find('span', {'style': "text-indent:0;"}) is None:
                    # Some parents are marked with the same style
                    # including them would create duplicated texts
                    defText += ("<b>(" + str(counter) + ")</b> "
                                + line.get_text().strip() + "<br/>")
                    counter = counter + 1
        else:
            defText = soup.get_text().strip()
            # crawl correct page
            for line in crawling_list:
                search = line[2].search(defText)
                if search:
                    if line[1] == 'fetch':
                        return(fetchDef(search.group(1)))
                    else:
                        return('')
            # parsing
            for line in parsing_list:
                defText = line[2].sub(line[1], defText)
    return defText
# Update note =================================================================


class Regen():
    def __init__(self, ed, fids):
        self.ed = ed
        self.fids = fids
        self.completed = 0
        self.config = mw.addonManager.getConfig(__name__)
        # self.force_update = config['force_update']
        # self.update_separator = config['update_separator']
        self.sema = threading.BoundedSemaphore(config['max_threads'])
        self.values = {}
        if len(self.fids) == 1:  # Single card selected
            self.row = self.ed.currentRow()
            self.ed.form.tableView.selectionModel().clear()
        mw.progress.start(max=len(self.fids), immediate=True)
        mw.progress.update(
            label=label_progress_update,
            value=0)

    def prepare(self):
        fs = [mw.col.getNote(id=fid) for fid in self.fids]
        i = 0
        for f in fs:
            try:
                if self.config['force_update'] == 'no' and f[definitionField]:
                    self.completed += 1
                    mw.progress.update(
                        label=label_progress_update,
                        value=self.completed)
                else:
                    self.values[i] = {}
                    self.values[i]['f'] = f
                    self.values[i]['word'] = f[expressionField]
                    thread = threading.Thread(target=self.fetch_def,
                                              args=(i,))
                    self.values[i]['thread'] = thread
                    thread.start()
                    i += 1
            except:
                print('definitions failed:')
                traceback.print_exc()

    def fetch_def(self, i):
        with self.sema:
            self.values[i]['definition'] = fetchDef(self.values[i]['word'])

    def wait_threads(self):
        for i, _ in self.values.items():
            thread = self.values[i]['thread']
            thread.join()
            self.update_def(i)
        mw.progress.finish()
        if len(self.fids) == 1:
            self.ed.form.tableView.selectRow(self.row)

    def update_def(self, i):
        f = self.values[i]['f']
        try:
            if self.config['force_update'] == "append":
                if f[definitionField]:
                    f[definitionField] += self.config['update_separator']
                f[definitionField] += self.values[i]['definition']
            else:
                f[definitionField] = self.values[i]['definition']
        except:
            print('definitions failed:')
            traceback.print_exc()
        try:
            f.flush()
        except:
            raise Exception()
        self.completed += 1
        mw.progress.update(
            label=label_progress_update,
            value=self.completed)


def prepare_regex():
    for i in range(len(crawling_list)):
        crawling_list[i][2] = re.compile(crawling_list[i][0])
    for i in range(len(parsing_list)):
        parsing_list[i][2] = re.compile(parsing_list[i][0])


def setupMenu(ed):
    a = QAction(label_menu, ed)
    a.triggered.connect(lambda _, e=ed: onRegenGlosses(e))
    ed.form.menuEdit.addAction(a)
    a.setShortcut(QKeySequence(keybinding))


def addToContextMenu(view, menu):
    menu.addSeparator()
    a = menu.addAction(label_menu)
    a.triggered.connect(lambda _, e=view: onRegenGlosses(e))
    a.setShortcut(QKeySequence(keybinding))


def onRegenGlosses(ed):
    regen = Regen(ed, ed.selectedNotes())
    regen.prepare()
    regen.wait_threads()
    mw.requireReset()


prepare_regex()
addHook('browser.setupMenus', setupMenu)
addHook('browser.onContextMenu', addToContextMenu)
