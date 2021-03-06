# -*- coding: utf-8 -*-
"""
Created on Sun Dec 07 01:48:00 2014

@author: Vidar Tonaas Fauske
"""

import collections
from python_qt_binding import QtCore

from tool import Tool


class FigureTool(Tool):
    def __init__(self, windows=None):
        self.cids = {}
        if self.single_action() is not None:
            self.connect(windows)
        self.cursor = self.make_cursor()
            
    def make_cursor(self):
        """
        Initialize the cursor for this instance. Is called in constructor.
        """
        return QtCore.Qt.ArrowCursor
        
    def get_cursor(self, widget=None):
        """
        Get the cursor for the supplied widget. Is applied when a widget is
        connected to the Tool.
        """
        # This default implementation does not use the widget information for
        # anything, but descendants might.
        return self.cursor
        
    def get_window(self, event):
        """
        Get the window for the event
        """
        if event.insaxes is None:
            return None
        return event.inaxes.figure.canvas.parent()
        
    def get_pixel_size(self, event):
        """
        Get the point size in data units
        """
        ax = event.inaxes
        if ax is None:
            return (0,0)
        invtrans = self.ax.transData.inverted()
        return abs(invtrans.transform((1, 1)) -
                    invtrans.transform((0, 0)))
                    
    def _wire(self, canvas, local_key, mpl_key):
        if hasattr(self, local_key):
            if local_key not in self.cids:
                self.cids[local_key] = {}
            self.cids[local_key][canvas] = canvas.mpl_connect(
                mpl_key, getattr(self, local_key))
    
    @staticmethod
    def _iter_windows(windows):
        if windows is None:
            return ()
        if not isinstance(windows, collections.Iterable):
            windows = (windows,)
        return windows
    
    def connect(self, windows):
        windows = self._iter_windows(windows)
        for w in windows:
            canvas = w.widget()
            canvas.setCursor(self.get_cursor(canvas))
            self._wire(canvas, 'on_mousemove', 'motion_notify_event')
            self._wire(canvas, 'on_mousedown', 'button_press_event')
            self._wire(canvas, 'on_mouseup', 'button_release_event')
            self._wire(canvas, 'on_keydown', 'key_press_event')
            self._wire(canvas, 'on_keyup', 'key_release_event')
            self._wire(canvas, 'on_pick', 'pick_event')
            self._wire(canvas, 'on_scroll', 'scroll_event')
            self._wire(canvas, 'on_draw', 'draw_event')
            self._wire(canvas, 'on_resize', 'resize_event')
            self._wire(canvas, 'on_figure_enter', 'figure_enter_event')
            self._wire(canvas, 'on_figure_leave', 'figure_leave_event')
            self._wire(canvas, 'on_axes_enter', 'axes_enter_event')
            self._wire(canvas, 'on_axes_leave', 'axes_leave_event')
    
    def disconnect(self, windows):
        windows = self._iter_windows(windows)
        for w in windows:
            canvas = w.widget()
            for cid_iter in self.cids.itervalues():
                for canv, cid in cid_iter.iteritems():
                    if canv == canvas:
                        try:
                            canvas.mpl_disconnect(cid)
                        except:
                            pass