# -*- coding: utf-8 -*-
"""
Created on Sun Dec 07 03:06:55 2014

@author: Vidar Tonaas Fauske
"""


from _tools.tool import Tool
from _tools.figuretool import FigureTool
from _tools.pointertool import PointerTool
from _tools.hometool import HomeTool
from _tools.zoompan import ZoomPanTool
from _tools.gaussiantool import GaussianTool
from _tools.croptool import CropTool

default_tools = [PointerTool, HomeTool, ZoomPanTool, GaussianTool, CropTool]