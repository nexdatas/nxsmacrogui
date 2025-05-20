#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2012-2018 DESY, Jan Kotanski <jkotan@mail.desy.de>
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
# \package test nexdatas
# \file XMLConfiguratorTest.py
# unittests for field Tags running Tango Server
#
import unittest
import os
import sys
import random
import struct
import binascii
import nxsselector
from nxstaurusgui import NXSMacroGUI

import taurus.qt.qtgui.application

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO


if sys.version_info > (3,):
    unicode = str
    long = int


# if 64-bit machione
IS64BIT = (struct.calcsize("P") == 8)

# from nxsconfigserver.XMLConfigurator  import XMLConfigurator
# from nxsconfigserver.Merger import Merger
# from nxsconfigserver.Errors import (
# NonregisteredDBRecordError, UndefinedTagError,
#                                    IncompatibleNodeError)
# import nxsconfigserver


def myinput(w, text):
    myio = os.fdopen(w, 'w')
    myio.write(text)

    # myio.close()


# test fixture
class NXSMacroGUITest(unittest.TestCase):

    # constructor
    # \param methodName name of the test method
    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)

        self.helperror = "Error: too few arguments\n"

        self.helpinfo = """usage: nxsmacrogui [-h] [-s SERVER] """ \
            """[-d DOOR] [--log LOG]

NeXus Macro GUI

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        selector server
  -d DOOR, --door DOOR  door device name
  --log LOG             logging level, i.e. debug, info, warning, """ \
      """error, critical
"""
        self.helpinfo2 = """usage: nxsmacrogui [-h] [-s SERVER] """ \
            """[-d DOOR] [--log LOG]

NeXus Macro GUI

options:
  -h, --help           show this help message and exit
  -s, --server SERVER  selector server
  -d, --door DOOR      door device name
  --log LOG            logging level, i.e. debug, info, warning, """ \
      """error, critical
"""
        try:
            # random seed
            self.seed = long(binascii.hexlify(os.urandom(16)), 16)
        except NotImplementedError:
            import time
            # random seed
            self.seed = long(time.time() * 256)  # use fractional seconds

        self.__rnd = random.Random(self.seed)

        self._bint = "int64" if IS64BIT else "int32"
        self._buint = "uint64" if IS64BIT else "uint32"
        self._bfloat = "float64" if IS64BIT else "float32"

        self.__args = '{"db":"nxsconfig", ' \
                      '"read_default_file":"/etc/my.cnf", "use_unicode":true}'
        self.__cmps = []
        self.__ds = []
        self.__man = []
        self.children = ("record", "doc", "device", "database", "query",
                         "datasource", "result")

        from os.path import expanduser
        home = expanduser("~")
        self.__args2 = '{"db":"nxsconfig", ' \
                       '"read_default_file":"%s/.my.cnf", ' \
                       '"use_unicode":true}' % home

    # test starter
    # \brief Common set up
    def setUp(self):
        print("\nsetting up...")
        print("SEED = %s" % self.seed)

    # test closer
    # \brief Common tear down
    def tearDown(self):
        print("tearing down ...")

    # Exception tester
    # \param exception expected exception
    # \param method called method
    # \param args list with method arguments
    # \param kwargs dictionary with method arguments
    def myAssertRaise(self, exception, method, *args, **kwargs):
        try:
            error = False
            method(*args, **kwargs)
        except Exception:
            error = True
        self.assertEqual(error, True)

    # comp_available test
    # \brief It tests Nxsmacrogui
    def mtest_default(self):
        fun = sys._getframe().f_code.co_name
        print("Run: %s.%s() " % (self.__class__.__name__, fun))

        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = mystdout = StringIO()
        sys.stderr = mystderr = StringIO()
        old_argv = sys.argv
        sys.argv = ['nxsmacrogui']
        try:
            with self.assertRaises(SystemExit):
                NXSMacroGUI.main()
        except Exception:
            NXSMacroGUI.main()

        sys.argv = old_argv
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        vl = mystdout.getvalue()
        er = mystderr.getvalue()
        print(vl)
        print(er)
        # self.assertEqual(self.helpinfo, vl)
        # self.assertEqual(self.helperror, er)

    # comp_available test
    # \brief It tests Nxsmacrogui
    def test_version(self):
        fun = sys._getframe().f_code.co_name
        print("Run: %s.%s() " % (self.__class__.__name__, fun))

        ver = nxsselector.__version__
        self.assertTrue(ver)
        self.assertTrue("." in ver)

    # comp_available tesQt
    # \brief It tests XMLConfigurator
    def test_help(self):
        fun = sys._getframe().f_code.co_name
        print("Run: %s.%s() " % (self.__class__.__name__, fun))

        helps = ['--help', '-h']
        Application = taurus.qt.qtgui.application.TaurusApplication
        for hl in helps:
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = mystdout = StringIO()
            sys.stderr = mystderr = StringIO()
            old_argv = sys.argv
            sys.argv = ['nxsmacrogui', hl]
            if Application.instance() is None:
                with self.assertRaises(SystemExit):
                    NXSMacroGUI.main()
            sys.argv = old_argv
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            vl = mystdout.getvalue()
            er = mystderr.getvalue()
            # print(vl)
            # print(er)
            if Application.instance() is None:
                vt = "".join(vl.split()).replace(
                    "optionalarguments:", "options:")
                if sys.version_info >= (3, 13):
                    helpinfo = "".join(self.helpinfo2.split()).replace(
                        "optionalarguments:", "options:")
                    self.assertTrue(
                        vt.endswith(helpinfo))
                else:
                    helpinfo = "".join(self.helpinfo.split()).replace(
                        "optionalarguments:", "options:")
                    self.assertTrue(
                        vt.endswith(helpinfo))
                self.assertEqual('', er)


if __name__ == '__main__':
    unittest.main()
