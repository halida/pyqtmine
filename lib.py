#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
module: lib
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import loadUi, loadUiType

import numpy as np
import random, time

app = QApplication([])

def inputBox(parent, inf="please input:"):
    name, result = QInputDialog.getText(parent, "", inf)
    if not result: 
        return None
    return name
