# backport of importlib.metadata for python < 3.8
from importlib_metadata import PackageNotFoundError, version

## Setup logging now, so it's available if __version__ fails:
import logging
ASF_LOGGER = logging.getLogger(__name__)
# Add null handle so we do nothing by default. It's up to whatever
# imports us, if they want logging.
ASF_LOGGER.addHandler(logging.NullHandler())

try:
    __version__ = version(__name__)
except PackageNotFoundError as e:
    msg = str('package is not installed!\n'
          'Install in editable/develop mode via (from the top of this repo):\n'
          '   python3 -m pip install -e .\n'
          'Or, to just get the version number use:\n'
          '   python setup.py --version')
    print(msg)
    ASF_LOGGER.exception(msg)
    raise PackageNotFoundError("Install with 'python3 -m pip install -e .' to use") from e

from .ASFSession import ASFSession
from .ASFProduct import ASFProduct
from .ASFStackableProduct import ASFStackableProduct
from .ASFSearchResults import ASFSearchResults
from .ASFSearchOptions import ASFSearchOptions, validators, validator_map
from .Products import *
from .exceptions import *
from .constants import BEAMMODE, FLIGHT_DIRECTION, INSTRUMENT, PLATFORM, POLARIZATION, PRODUCT_TYPE, INTERNAL, DATASET
from .exceptions import *
from .health import *
from .search import *
from .download import *
from .CMR import *
from .baseline import *
from .WKT import validate_wkt, filesToWKT
from .export import *

REPORT_ERRORS=True
"""Enables automatic search error reporting to ASF, send any questions to uso@asf.alaska.edu"""
