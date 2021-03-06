"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup, find_packages

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)


APP = ['NeQtPy3']
DATA_FILES = []
OPTIONS = {}

setup(
    name="NeQtPy3",
    version="0.1",    
    author = "Jonathan Morgan",
    author_email = "jonathandm93@gmail.com",
    # url = "https://github.com/j-morgan93/matplot_gui", 
    app=APP,
    data_files=DATA_FILES, 
    packages=find_packages(),
    scripts=['NeQtPy3_l.py','specfit.py'],
    install_requires=['regex','numpy','matplotlib','scipy'],  
)
