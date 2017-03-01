# September 2013, Glenn F. Matthews
# Copyright (c) 2013-2017 the COT project developers.
# See the COPYRIGHT.txt file at the top-level directory of this distribution
# and at https://github.com/glennmatthews/cot/blob/master/COPYRIGHT.txt.
#
# This file is part of the Common OVF Tool (COT) project.
# It is subject to the license terms in the LICENSE.txt file found in the
# top-level directory of this distribution and at
# https://github.com/glennmatthews/cot/blob/master/LICENSE.txt. No part
# of COT, including this file, may be copied, modified, propagated, or
# distributed except according to the terms contained in the LICENSE.txt file.

"""
Package implementing the Common OVF Tool.

Utility modules
---------------
.. autosummary::
  :toctree:

  COT.data_validation
  COT.file_reference
  COT.logging_
  COT.utilities
  COT.xml_file

Sub-packages
------------
.. autosummary::
  :toctree:

  COT.commands
  COT.disks
  COT.helpers
  COT.platforms
  COT.ui
  COT.vm_description
"""

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

__version_long__ = (
    """Common OVF Tool (COT), version """ + __version__ +
    """\nCopyright (C) 2013-2017 the COT project developers."""
)
