#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015 FUJITSU LABORATORIES OF EUROPE

"""
Python LOD4ALL library.
A Python library to access LOD4ALL and query a SPARQL.

List of error codes:

    Error     Code    Description
    ------------------------------------------------------
    EAPPID    0       Invalid App Id
    ESYNTX    1       SPARQL Syntax Error
    ETIMEO    2       Connection timeout
    ESERVR    3       The server returned an error status

"""
__version__ = '0.1.1'
from lod4all import *
