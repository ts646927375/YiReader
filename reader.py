#!/usr/bin/env python                                                                                                                                   
# -*- coding:UTF-8 -*-
         
import os
import sys
         
from PySide import QtCore, QtGui
         
import const
         
class YiReader(QtGui.QMainWindow):
    """a text novel reader which can split chapters"""
    def __init__(self):
        super(YiReader, self).__init__()
         
        self.create_actions()
        self.create_menus()
        self.create_toolbars()
        self.create_statusbar()
         
        self.text_viewer = QtGui.QTextEdit()
        self.setCentralWidget(self.text_viewer)
        self.setWindowTitle("YiReader")
         
    def create_actions(self):
        """create actions for menus and toolbar"""
        self.open_act = QtGui.QAction(QtGui.QIcon("images/open.png"),
            "&Open Book", self, triggered = self.open_book)
         
        self.close_act = QtGui.QAction(QtGui.QIcon("images/close.png"),
            "&Close Book", self, triggered = self.close_book)
         
        self.exit_act = QtGui.QAction(QtGui.QIcon("images/exit.png"),
            "&Exit", self, triggered = self.exit)
         
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
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_act)
 
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
        self.file_toolbar.addAction(self.exit_act)
                                                                                                                                                        
        self.edit_toolbar = self.addToolBar("Edit")
        self.edit_toolbar.addAction(self.add_bookmark_act)
        self.edit_toolbar.addAction(self.del_bookmark_act)
        self.edit_toolbar.addAction(self.split_book_act)
 
    def create_statusbar(self):
        """create status bar"""
        sb = self.statusBar()
        sb.progress = QtGui.QProgressBar()
        sb.addPermanentWidget(sb.progress)
        self.setStatusBar(sb)
        self.statusBar().showMessage("Ready")
         
    def open_book(self):
        """open a new book from file system"""
        # open an file dialog
        filepath, filtr = QtGui.QFileDialog.getOpenFileName(self, "Open Book",
            const.DEFAULT_DIR_LINUX, const.FILE_PATTERN)
        self.filename = os.path.normcase(filepath)
        self.reader = file(filepath, "r")
        self.text_viewer.setText(self.reader.read())
         
    def close_book(self):
        print "call close_book"
         
    def exit(self):
        print "call exit"
         
    def add_bookmark(self):
        print "call add_bookmark"
         
    def del_bookmark(self):
        print "call del_bookmark"
         
    def split_book(self):
        print "call split_book"
         
    def about(self):
        print "call about"
         
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    reader = YiReader()
    reader.show()
    sys.exit(app.exec_())                                                                                                                               
