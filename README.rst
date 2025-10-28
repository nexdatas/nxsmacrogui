Welcome to nxstaurusgui's documentation!
========================================


|github workflow|
|docs|
|Pypi Version|
|Python Versions|

.. |github workflow| image:: https://github.com/nexdatas/nxsmacrogui/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/nexdatas/nxsmacrogui/actions
   :alt:

.. |docs| image:: https://img.shields.io/badge/Documentation-webpages-ADD8E6.svg
   :target: https://nexdatas.github.io/nxsmacrogui/index.html
   :alt:

.. |Pypi Version| image:: https://img.shields.io/pypi/v/nxstaurusgui.svg
                  :target: https://pypi.python.org/pypi/nxstaurusgui
                  :alt:

.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/nxstaurusgui.svg
                     :target: https://pypi.python.org/pypi/nxstaurusgui/
                     :alt:



Authors: Jan Kotanski

NXS MacroGUI is taurus gui Configuration for Component Selector

.. figure:: png/nxstaurusgui.png
   :alt: NeXus Taurus GUI


| Source code: https://github.com/nexdatas/nxsmacrogui/
| Web page: https://nexdatas.github.io/nxsmacrogui/
| NexDaTaS Web page: https://nexdatas.github.io



------------
Installation
------------

Install the dependencies:

|    Sardana, PyTango, sphinx, Taurus, NXSRecSelector, Selector

From sources
^^^^^^^^^^^^

Download the latest version of NeXuS Configuration Server from

|    https://github.com/nexdatas/nxsmacrogui/

Extract the sources and run

.. code-block:: console

	  $ python3 setup.py install

Debian packages
^^^^^^^^^^^^^^^

Debian Trixie, Bookworm, Bullseye and  Ubuntu Questing, Noble, Jammy packages can be found in the HDRI repository.

To install the debian packages, add the PGP repository key

.. code-block:: console

	  $ sudo su
	  $ curl -s http://repos.pni-hdri.de/debian_repo.pub.gpg | gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/debian-hdri-repo.gpg --import
	  $ chmod 644 /etc/apt/trusted.gpg.d/debian-hdri-repo.gpg

and then download the corresponding source list

.. code-block:: console

	  $ cd /etc/apt/sources.list.d
	  $ wget http://repos.pni-hdri.de/trixie-pni-hdri.sources

Finally,

.. code-block:: console

	  $ apt-get update
	  $ apt-get install python3-nxsrecselector nxselector nxstaurusgui

To instal other NexDaTaS packages

.. code-block:: console

	  $ apt-get install python-nxswriter nxsconfigtool nxstools python-nxsconfigserver nxsconfigserver-db

and

.. code-block:: console

	  $ apt-get install python3-sardana-nxsrecorder

for NeXus recorder.

From pip
^^^^^^^^

To install it from pip you need also to install pyqt5, e.g.

.. code-block:: console

   $ python3 -m venv myvenv
   $ . myvenv/bin/activate

   $ pip install pyqt5

   $ pip install sardana-nxsrecorder

Moreover it is also good to install

.. code-block:: console

   $ pip install pytango
   $ pip install sardana
   $ pip install nxswriter
   $ pip install nxsrecselector
   $ pip install nxsconfigserver
   $ pip install nxstools
   $ pip install pymysqldb


-------------------
Setting environment
-------------------


Setting Saradna
^^^^^^^^^^^^^^^
If sardana is not yet set up run


.. code-block:: console

	  $ Pool

- enter a new instance name
- create the new instance

Then wait a while until Pool is started and in a new terminal run

.. code-block:: console

	  $ MacroServer

- enter a new instance name
- create the new instance
- connect pool

Next, run Astor and change start-up levels: for Pool to 2,
for MacroServer to 3 and restart servers.

Alternatively, terminate Pool and MacroServer in the terminals and run

.. code-block:: console

          $ nxsetup start Pool -l2

wait until Pool is started and run

.. code-block:: console

          $ nxsetup start MacroServer -l3


Additionally, one can create dummy devices by running `sar_demo` in

.. code-block:: console

	  $ spock



Setting NeXus Servers
^^^^^^^^^^^^^^^^^^^^^

To set up  NeXus Servers run

.. code-block:: console

	  $ nxsetup set

or

.. code-block:: console

          $ nxsetup set NXSDataWriter
          $ nxsetup set NXSConfigServer
	  $ nxsetup set NXSRecSelector

for specific servers.

If the `RecoderPath` property of MacroServer is not set one can do it by

.. code-block:: console

	  $ nxsetup add-recorder-path  /usr/lib/python3/dist-packages/sardananxsrecorder

where the path should point the `sardananxsrecorder` package.

