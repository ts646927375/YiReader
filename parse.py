#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#
# 读取书签，章节等信息
#
# 整个过程解析完成后，会返回一个字典
# self.book_info["position"]            ---> int
# self.book_info["chapters"]            ---> list
# self.book_info["bookmarks"]           ---> list

import os
import lxml.etree as tree

class BookInfoReader(object):
    """读取信息"""
    def __init__(self, filename):
        super(BookInfoReader, self).__init__()
        name, postfix = os.path.splitext(filename)
        self.filename = name + ".xml"
        self.book_info = dict()

    def get_book_info(self):
        """获取位置，章节，书签等信息"""
        if os.path.exists(self.filename):
            self.filename = os.path.normcase(self.filename)

            # 获取位置信息
            position_node = tree.parse(self.filename).xpath("/Book/position")
            try:
                self.book_info["position"] = int(position_node[0].text)
            except IndexError, ex:
                print u"IndexError: position_node length: {}, refered: {}!".format(len(position_node), 0)
                print u"Can't get book information!"
                return
            except ValueError, ex:
                print ex[0]
                print u"Can't get book information!"
                return

            # 获取章节信息
            chapter_nodes = tree.parse(self.filename).xpath("/Book/chapters/chapter")
            self.book_info["chapters"] = list()
            for node in chapter_nodes:
                root = tree.ElementTree(node)
                _name = root.xpath("/chapter/name")[0].text
                _pos = root.xpath("/chapter/pos")[0].text
                if type(_name) == str: _name = _name.decode("utf-8")
                if type(_pos) == str: _pos = _pos.decode("utf-8")
                self.book_info["chapters"].append((_name, _pos))

            # 获取书签信息
            bookmark_nodes = tree.parse(self.filename).xpath("/Book/bookmarks/bookmark")
            self.book_info["bookmarks"] = list()
            for node in bookmark_nodes:
                root = tree.ElementTree(node)
                _name = root.xpath("/bookmark/name")[0].text
                _pos = root.xpath("/bookmark/pos")[0].text
                if type(_name) == str: _name = _name.decode("utf-8")
                if type(_pos) == str: _pos = _pos.decode("utf-8")
                self.book_info["bookmarks"].append((_name, _pos))

            self.echo_book_info()

            return self.book_info
        else:
            return

    def echo_book_info(self):
        """输出信息，作调试用"""
        for key in self.book_info.keys():
            print "------------------------------------------------------------"
            print "[{}]:".format(key)
            value = self.book_info.get(key)
            if type(value) == list :
                for k in value:
                    print k[0], k[1]
            else:
                print value
            print "------------------------------------------------------------"


class BookInfoWriter(object):
    """docstring for BookInfoWriter"""
    def __init__(self, filename, book_info):
        super(BookInfoWriter, self).__init__()
        self.filename = filename
        self.book_info = book_info

    def write_info(self):
        pass

if __name__ == '__main__':
    path = "C:/Users/Shun/Desktop/reader.txt"
    parser = BookInfoReader(path)
    parser.get_book_info()