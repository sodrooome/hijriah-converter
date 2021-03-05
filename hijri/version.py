__version__ = '0.1.0'


def get_version():
    return __version__


def get_version_as_tuple():
    return tuple(map(int, __version__.split('.')))
