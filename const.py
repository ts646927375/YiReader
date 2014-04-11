#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#
# store const variable
#

# default directory in open book act
DEFAULT_DIR = "C:/Users/Shun/Desktop"

# file filter
FILE_PATTERN = "Text files (*.txt)"

# buffer size for reading book
BUFFER_SIZE = 4096

# system coding
CODING = "utf-8"

# pattern for novel title
TITLE_PATTERN = "^\s(前言)|^(楔子)|^(作品相关)|([第][零一二三四五六七八九十百千0123456789]{1,5}[章节回部卷集])".decode(CODING)
