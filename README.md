portablizer
===========

Make a web app portable.

Build
-----

You can run ``./configure`` to download stable node binary for your system. In Ubuntu, it will also help you install dependencies.

### Ubuntu Linux

It is recommended to build on system with lower version of glibc (for better compatibility) and can download Qt4 binaries (for faster building process), for example, Ubuntu 10.04.

    $ sudo apt-get update
    $ sudo apt-get install build-essential python-dev python-pip pyqt4-dev-tools git-core
    $ sudo pip install pyinstaller
    $ sudo easy_install psutil
    $ git clone https://github.com/caiguanhao/portablizer.git
    $ cd portablizer
    $ make

### Mac OS X

For retina support, you'll need to install Qt5 and PyQt5. Building PyQt5 with Homebrew may fail because of a [problem](https://github.com/Homebrew/homebrew/wiki/C---standard-libraries), so it is recommended to build PyQt5 from source. You'll need to download [Qt 5 for Mac](http://qt-project.org/downloads) package. And download the source of [SIP](http://www.riverbankcomputing.co.uk/software/sip/download) and [PyQt5](http://www.riverbankcomputing.co.uk/software/pyqt/download5).

You may need to use python2.7 to compile both SIP and PyQt5, because PyInstaller supports only Python 2.4-2.7. qmake can be found in Qt 5 packages. sip is installed somewhere inside python directory. You may provide -qmake, -sip-incdir, -sip when you build PyQt5, for example:

    python2.7 ./configure.py –qmake /.../Qt5.2.0/5.2.0/clang_64/bin/qmake
        –sip-incdir /usr/local/Cellar/python/2.7.5/Frameworks/Python.framework/Versions/2.7/include/python2.7/
        –sip /usr/local/Cellar/python/2.7.5/Frameworks/Python.framework/Versions/2.7/bin/sip

App built with PyInstaller may have some little problems, you can use my [fork of PyInstaller](https://github.com/caiguanhao/pyinstaller). You may need to install other packages via pip or easy_install, please refer to the Ubuntu/Linux section.

### Windows

* Download [msysgit (PortableGit)](https://code.google.com/p/msysgit/downloads/list) and extract it to C:\\msys.
* Download [mintty (msys)](https://code.google.com/p/mintty/downloads/list) and put mintty.exe to C:\\msys\\bin folder and create a shortcut of it to Desktop.
* Right click the shortcut file, select Properties. Chagne Target to C:\\msys\\bin\\mintty.exe -c C:\\msys\\.minttyrc "C:\\msys\\bin\\sh.exe" --login. Change Start in to your home folder, for example, C:\\home. Change locale settings if necessary.
* Download [make.exe](https://msysgit.googlecode.com/git/bin/make.exe) and [zip binaries](http://sourceforge.net/projects/mingw/files/MSYS/Extension/zip/zip-3.0-1/) to C:\\msys\\bin.
* Download and install [Python 2.7.6](http://www.python.org/download/releases/2.7.6/) to C:\\Python27.
* Right click My Computer, select Properties. In the Advanced tab, click Environment Variables button. Double click the Path item in System variables. Append C:\\Python27\\;C:\\Python27\\Scripts\\ and click OKs to save it.
* Download and install [setuptools for Py2.7](http://www.lfd.uci.edu/~gohlke/pythonlibs/#setuptools).
* Download and install [pywin32 for Py2.7](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pywin32)
* Download [PyInstaller](http://www.pyinstaller.org/) and extract it to C:\\. Use mintty to install: cd to that folder and run *python setup.py install*.
* If you are using Windows XP, an error occurs and you may need to uncomment several lines (248~251) in C:\\Python27\\Lib\\mimetypes.py. You can search Google for this error.
* Download and install [PyQt4 binary package for Windows Py2.7](http://www.riverbankcomputing.co.uk/software/pyqt/download)
* You may need to install other packages via pip or easy_install, please refer to the Ubuntu/Linux section.
* You may now able to make: *cd /c/home*, *git clone https://github.com/caiguanhao/portablizer.git*, *cd portablizer*, *make*.
