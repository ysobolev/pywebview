#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
pywebview is a lightweight cross-platform wrapper around a webview component that allows to display HTML content in its
own dedicated window. Works on Windows, OS X and Linux and compatible with Python 2 and 3.

(C) 2014-2015 Roman Sirokov
Licensed under BSD license

http://github.com/r0x0r/pywebview/
"""


import platform
import os
import sys
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

OPEN_DIALOG = 10
FOLDER_DIALOG = 20
SAVE_DIALOG = 30


config = {
    "USE_QT": False
}

_initialized = False


def _initialize_imports():
    global _initialized, gui

    if not _initialized:
        if platform.system() == "Darwin":
            import webview.cocoa as gui
        elif platform.system() == "Linux":

            try:
                #Try QT first unless USE_GTK variable is defined
                if not config["USE_QT"]:
                    import webview.gtk as gui
                    logger.info("Using GTK")
            except ImportError as e:
                logger.warning("GTK not found")
                import_error = True
            else:
                import_error = False

            if import_error or config["USE_QT"]:
                try:
                    # If GTK is not found, then try QT
                    import webview.qt as gui
                    logger.info("Using QT")
                except ImportError as e:
                    # Panic
                    logger.error("QT not found")
                    raise Exception("You must have either QT or GTK with Python extensions installed in order to this library.")

        elif platform.system() == "Windows":
            import webview.win32 as gui
        else:
            raise Exception("Unsupported platform. Only Windows, Linux and OS X are supported.")

        _initialized = True



def create_file_dialog(dialog_type=OPEN_DIALOG, directory='', allow_multiple=False, save_filename=''):
    """
    Create a file dialog
    :param dialog_type: Dialog type: open file (OPEN_DIALOG), save file (SAVE_DIALOG), open folder (OPEN_FOLDER). Default
                        is open file.
    :param directory: Initial directory
    :param allow_multiple: Allow multiple selection. Default is false.
    :param save_filename: Default filename for save file dialog.
    :return:
    """

    if not os.path.exists(directory):
        directory = ''

    try:
        return gui.create_file_dialog(dialog_type, directory, allow_multiple, save_filename)
    except NameError:
        raise Exception("Create a web view window first, before invoking this function")



def load_url(url):
    """
    Load a new URL into a previously created WebView window. This function must be invoked after WebView windows is
    created with create_window(). Otherwise an exception is thrown.
    :param url: url to load
    """
    try:
        gui.load_url(url)
    except NameError:
        raise Exception("Create a web view window first, before invoking this function")

def load_html(content, base_uri=""):
    """
    Load a new content into a previously created WebView window. This function must be invoked after WebView windows is
    created with create_window(). Otherwise an exception is thrown.
    :param content: Content to load.
    :param base_uri: Base URI for resolving links. Default is "".
    """
    try:
        gui.load_html(_make_unicode(content), base_uri)
    except NameError:
        raise Exception("Create a web view window first, before invoking this function")


def create_window(title, url=None, width=800, height=600, resizable=True, fullscreen=False, min_size=(200, 100)):
    """
    Create a web view window using a native GUI. The execution blocks after this function is invoked, so other
    program logic must be executed in a separate thread.
    :param title: Window title
    :param url: URL to load
    :param width: Optional window width (default: 800px)
    :param height: Optional window height (default: 600px)
    :param resizable True if window can be resized, False otherwise. Default is True.
    :return:
    """
    _initialize_imports()
    gui.create_window(_make_unicode(title), _transform_url(url), width, height, resizable, fullscreen, min_size)


def destroy_window():
    """
    Destroy a web view window
    """
    try:
        gui.destroy_window()
    except NameError:
        raise Exception("Create a web view window first, before invoking this function")

def _make_unicode(string):
    """
    Python 2 and 3 compatibility function that converts a string to Unicode. In case of Unicode, the string is returned
    unchanged
    :param string: input string
    :return: Unicode string
    """
    if sys.version < '3' and isinstance(string, str):
        return unicode(string.decode('utf-8'))

    return string


def _transform_url(url):
    if url == None:
        return url
    if url.find(":") == -1:
        return 'file://' + os.path.abspath(url)
    else:
        return url
