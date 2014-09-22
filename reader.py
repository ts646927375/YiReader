#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import re
import os
import sys
import time

import chardet
from PySide import QtCore, QtGui

import const

class YiReader(QtGui.QMainWindow):
    """a text novel reader which can split chapters"""
    def __init__(self):
        super(YiReader, self).__init__()

        # 存放书签，章节信息
        self.book_info = dict()
        self.file_name = None
        self.file_coding = None
        self.position = 0

        self.text_viewer = QtGui.QTextEdit()
        self.setCentralWidget(self.text_viewer)
        self.setWindowTitle("YiReader")

        self.create_actions()
        self.create_menus()
        self.create_toolbars()
        # self.create_statusbar()
        self.create_dock_windows()
        # maximize window
        # self.showMaximized()

    def create_actions(self):
        """create actions for menus and toolbar"""
        self.open_act = QtGui.QAction(QtGui.QIcon("images/open.png"),
            "&Open Book", self, triggered = self.open_book)

        self.close_act = QtGui.QAction(QtGui.QIcon("images/close.png"),
            "&Close Book", self, triggered = self.close_book)

        self.add_bookmark_act = QtGui.QAction(QtGui.QIcon("images/add.png"),
            "&Add Bookmark", self, triggered = self.add_bookmark)

        self.del_bookmark_act = QtGui.QAction(QtGui.QIcon("images/del.png"),
            "&Del Bookmark", self, triggered = self.del_bookmark)

        self.split_book_act = QtGui.QAction(QtGui.QIcon("images/split.png"),
            "&Split Chapter", self, triggered = self.split_book)

        self.about_act = QtGui.QAction(QtGui.QIcon("images/about.png"),
            "&About", self, triggered = self.about)

    def create_menus(self):
        """create menus"""
        self.file_menu = self.menuBar().addMenu("&File")
        self.file_menu.addAction(self.open_act)
        self.file_menu.addAction(self.close_act)

        self.edit_menu = self.menuBar().addMenu("&Edit")
        self.edit_menu.addAction(self.add_bookmark_act)
        self.edit_menu.addAction(self.del_bookmark_act)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.split_book_act)

        self.help_menu = self.menuBar().addMenu("&Help")
        self.help_menu.addAction(self.about_act)

    def create_toolbars(self):
        """create toobars, familar with menus"""
        self.file_toolbar = self.addToolBar("File")
        self.file_toolbar.addAction(self.open_act)
        self.file_toolbar.addAction(self.close_act)

        self.edit_toolbar = self.addToolBar("Edit")
        self.edit_toolbar.addAction(self.add_bookmark_act)
        self.edit_toolbar.addAction(self.del_bookmark_act)
        self.edit_toolbar.addAction(self.split_book_act)

    # def create_statusbar(self):
    #     """create status bar"""
    #     self.statusBar().showMessage("Ready")

    def create_dock_windows(self):
        """create dock windows"""
        dock = QtGui.QDockWidget("Chapters", self)
        dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.chapter_list = QtGui.QListWidget(dock)
        self.chapter_list.itemDoubleClicked.connect(self.chapter_click)
        dock.setWidget(self.chapter_list)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)

        dock = QtGui.QDockWidget("Bookmarks", self)
        dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.bookmark_list = QtGui.QListWidget(dock)
        self.bookmark_list.itemDoubleClicked.connect(self.item_click)
        dock.setWidget(self.bookmark_list)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)

    def chapter_click(self, item):
        """找到对应的章节，并展示内容"""
        index = self.chapter_list.row(item)
        try:
            pos = self.book_info["chapters"][index][1]
            size = self.book_info["chapters"][index + 1][1] - pos
        except IndexError, e:
            self.create_error_msg

    def item_click(self, item):
        mark = item.text()
        pos1 = self.bookmarks.get(mark)
        pos2 = self.chapters.get(mark)
        if pos1:
            pos = pos1
        elif pos2:
            pos = pos2
        if pos:
            cursor = file(self.filename, "r")
            cursor.seek(pos)
            content = cursor.read(const.BUFFER_SIZE).decode("GB2312", "ignore")
            self.text_viewer.setText(content)
            cursor.close()
        else:
            self.create_error_msg(u"Sorry, can not find bookmark/chapter!")

    def open_book(self):
        """open a new book from file system"""
        # open an file dialog
        filepath, filtr = QtGui.QFileDialog.getOpenFileName(
            self,
            "Open Book",
            const.DEFAULT_DIR,
            const.FILE_PATTERN
        )
        self.filename = os.path.normcase(filepath)

        self.split_book()
        text_size = self.chapters[self.cur_pos + 1][1] - self.chapters[self.cur_pos][1]

        with open(self.filename, "r") as f:
            text = f.read()
            self.coding = chardet.detect(text).get("encoding")
            self.text_viewer.setText(text.decode(self.coding, "ignore"))
            f.close()

        self.cursor = file(self.filename, "r")
        content = self.cursor.read(const.BUFFER_SIZE)
        self.coding = chardet.detect(content).get("encoding")
        self.text_viewer.setText(content.decode(self.coding, "ignore"))
        self.cursor.close()

    def close_book(self):
        """close book, clear memory"""
        if self.filename:
            self.filename = None
            self.coding = None
            self.chapters = dict()
            self.bookmarks = dict()
            self.bookmark_list.clear()
            self.chapter_list.clear()
            self.text_viewer.setText("")
        else:
            self.create_error_msg(u"No book to close!")

    def add_bookmark(self):
        """add bookmark"""
        if self.filename:
            mark, ok = QtGui.QInputDialog.getText(self, u"Please enter a name of this bookmark",
                u"Bookmark Name", QtGui.QLineEdit.Normal, u"Bookmark1")
            if ok and mark != "":
                self.bookmarks[mark] = self.cursor.tell()
                print mark, self.bookmarks[mark]
                self.bookmark_list.addItem(mark)
                self.bookmark_list.sortItems()
        else:
            self.create_error_msg(u"No book to mark!")


    def del_bookmark(self):
        print "call del_bookmark"

    def split_book(self):
        """split book into chapters"""
        # if file is opened
        if self.filename:
            offset = 0
            pattern = re.compile(const.TITLE_PATTERN)
            self.chapter_list.clear()

            with open(self.filename, "r") as f:
                for line in iter(f.readline, ''):
                    line = line.decode(self.coding, "ignore").strip()
                    match = pattern.match(line)
                    if match:
                        self.chapters[line] = offset
                        self.chapter_list.addItem(line)
                        # print u"add chapter:\t" + line + "\t" + str(offset)
                    else:
                        pass
                        # print u"normal:\t" + line + "\t" + str(offset)
                    # current file position
                    offset = f.tell()
        else:
            # there is no open books
            self.create_error_msg(u"No book to split! \nPlease open a book.")

    def create_error_msg(self, msg):
        """pop up an error msg"""
        msg_box = QtGui.QMessageBox()
        msg_box.setWindowTitle(u"Error")
        msg_box.setText(msg)
        msg_box.setIcon(QtGui.QMessageBox.Warning)
        msg_box.exec_()

    def about(self):
        print "call about"

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    reader = YiReader()
    reader.show()
    sys.exit(app.exec_())
