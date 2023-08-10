from cx_Freeze import setup, Executable
import sys

sys.setrecursionlimit(3000)

build_exe_options = {
    'optimize': 2,  # 0=none, 1=bytecode, 2=docstrings
    'packages': ['pygame'],
    'includes': [],
    'include_files': ['res'],
    'zip_includes': [],
    'zip_include_packages': [],
    'excludes': [
        #'abc',          # Required for console
        'argparse',
        'ast',
        'asyncio',
        'atexit',
        'base64',
        'bdb',
        'binascii',
        # 'bisect',
        'bz2',
        'calendar',
        'cmd',
        'code',
        #'codecs',       # Required for console
        'codeop',
        # 'collections',  
        # 'collections.abc',
        'concurrent',
        # 'contextlib',
        'copy',
        #'copyreg',      # Required for console
        'csv',
        'ctypes',
        'dataclasses',
        'datetime',
        'decimal',
        'difflib',
        'dis',
        'distutils',
        'doctest',
        'email', 
        #'encodings',    # Required package
        #'enum',         # Required for console
        'errno',
        'fnmatch',       # Required for pathlib
        'fractions',
        #'functools',    # Required for console
        'gc',
        #'genericpath',  # Required for console
        'getopt',
        'gettext',
        'glob',
        'heapq',
        'hashlib',
        'html', 
        'http', 
        #'importlib',   # Required package
        'inspect',
        'io',
        'itertools',
        #'keyword',     # Required for console
        'lib2to3',
        'linecache',    # Required for pathlib
        'locale',
        'logging',
        'lzma',
        'marshal',
        # 'math',        #required 
        'msvcrt',
        'multiprocessing',
        'nt',
        #'ntpath',    # Required for console
        'numbers',
        'opcode',
        #'operator',  # Required for console
        'os',
        'os.path',
        'path',
        'pathlib',    # Required for pathlib
        'pdb',
        # 'pickle',   # Required for saving
        'pkgutil',
        'platform',
        'plistlib',
        'posixpath',  # Required for pathlib
        'pprint',
        'pydoc',
        'pydoc_data',
        'quopri',
        # 'random',
        #'re',       # Required for console
        #'reprlib',  # Required for console
        'runpy',
        'select',
        'selectors',
        'shlex',
        'shutil',
        # 'signal',
        'socket',
        #'sre_compile',    # Required for console
        #'sre_constants',  # Required for console
        #'sre_parse',      # Required for console
        #'stat',           # Required for console
        'statistics',
        #'string',         # Required for console
        'stringprep',
        # 'struct',
        # 'subprocess',
        # 'sys',  #include
        # 'sysconfig',
        'tarfile',
        'tempfile',
        'test',
        'textwrap',
        # 'threading',
        'time',
        'tkinter',
        'token',      # Required for pathlib
        'tokenize',   # Required for pathlib
        'traceback',
        'tracemalloc',
        'tty',
        #'types',     # Required for console
        'typing',
        'unicodedata',
        'unittest', 
        'urllib',     # Required for pathlib
        'warnings',
        # 'weakref',
        'webbrowser',
        'winreg',
        'xml', 
        'xmlrpc',
        'zipfile',
        'zipimport',
        'zlib'
    ]
}

setup(
    name="Automata Osmosis",
    version="0.1",
    description="Game innit",
    options={"build_exe": build_exe_options},
    executables=[Executable("game.py", base="Win32GUI", icon="res/icon.ico")],
)