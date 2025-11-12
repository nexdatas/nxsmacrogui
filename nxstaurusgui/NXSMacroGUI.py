#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2014-2017 DESY, Jan Kotanski <jkotan@mail.desy.de>
#
#    nexdatas is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nexdatas is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with nexdatas.  If not, see <http://www.gnu.org/licenses/>.
#

""" NXS Scan - GUI for setting sardana scans with NeXus Recorder"""

import logging
import sys
import os
from . import serverinfo


logger = logging.getLogger(__name__)


def setLoggerLevel(logger, level):
    global _logginglevel
    """ sets logging level from string
    :param logger: logger
    :type logger: :obj:`logging.logger`
    :param level: logging level
    :type level: :obj:`str`
    """
    levels = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}
    _logginglevel = level if level in levels else "warning"
    dlevel = levels.get(level, logging.WARNING)
    logger.setLevel(dlevel)
    from taurus.core.util.log import Logger
    Logger.log_level = dlevel


# the main function
def remove_option(sopt, lopt):
    pos = None
    single = True
    for i, ar in enumerate(sys.argv):
        if ar.startswith(sopt):
            pos = i
            if ar == sopt:
                single = False
            break
        elif ar.startswith(lopt + '='):
            pos = i
            break
    if pos is not None:
        if not single and len(sys.argv) > pos:
            sys.argv.pop(pos + 1)
        sys.argv.pop(pos)


def main():

    # if "GNOME_DESKTOP_SESSION_ID" not in os.environ:
    #     os.environ["GNOME_DESKTOP_SESSION_ID"] = "qtconfig"
    # if os.path.isdir("/usr/lib/kde4/plugins/") and \
    #    "QT_PLUGIN_PATH" not in os.environ:
    #     os.environ["QT_PLUGIN_PATH"] = "/usr/lib/kde4/plugins/"

    import argparse
    parser = argparse.ArgumentParser(
        description="NeXus Macro GUI")

    parser.add_argument(
        "-s", "--server", dest="server",
        help="selector server")
    parser.add_argument(
        "-d", "--door", dest="door",
        help="door device name")
    parser.add_argument(
        "--log", dest="log",
        help="logging level, i.e. debug, info, warning, error, critical")

    options = parser.parse_args()
    if options.log:
        setLoggerLevel(logger, options.log)
        remove_option("", "--log")
    if options.door:
        serverinfo.DOOR_NAME = options.door
        remove_option("-d", "--door")
    if options.server:
        serverinfo.SELECTORSERVER_NAME = options.server
        remove_option("-s", "--server")
    try:
        from taurus.external.qt import Qt
    except Exception:
        from taurus.qt import Qt
    Qt.QCoreApplication.setAttribute(Qt.Qt.AA_X11InitThreads)
    import sys
    sys.argv.insert(1, str(os.path.dirname(__file__)))
    try:
        from taurus.qt.qtgui.taurusgui.taurusgui import main as tmain
    except Exception:
        from taurus.qt.qtgui.taurusgui.taurusgui import gui_cmd as tmain
    try:
        serverinfo.FIND = True
        tmain()
    finally:
        if serverinfo.TMPFILE and os.path.exists(serverinfo.TMPFILE):
            os.remove(serverinfo.TMPFILE)


if __name__ == "__main__":
    main()
