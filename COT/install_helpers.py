#!/usr/bin/env python
#
# install_helpers.py - Implements "cot install-helpers" command
#
# February 2015, Glenn F. Matthews
# Copyright (c) 2014-2015 the COT project developers.
# See the COPYRIGHT.txt file at the top-level directory of this distribution
# and at https://github.com/glennmatthews/cot/blob/master/COPYRIGHT.txt.
#
# This file is part of the Common OVF Tool (COT) project.
# It is subject to the license terms in the LICENSE.txt file found in the
# top-level directory of this distribution and at
# https://github.com/glennmatthews/cot/blob/master/LICENSE.txt. No part
# of COT, including this file, may be copied, modified, propagated, or
# distributed except according to the terms contained in the LICENSE.txt file.

"""Implements "install-helpers" command."""

import argparse
import logging
import textwrap

from .submodule import COTGenericSubmodule

logger = logging.getLogger(__name__)


class COTInstallHelpers(COTGenericSubmodule):

    """Install all helper tools that COT requires."""

    def __init__(self, UI):
        """Instantiate this submodule with the given UI."""
        super(COTInstallHelpers, self).__init__(UI)
        self.ignore_errors = False
        self.verify_only = False

    def run(self):
        """Verify all helper tools and install any that are missing."""
        from COT.helpers.fatdisk import FatDisk
        from COT.helpers.mkisofs import MkIsoFS
        from COT.helpers.ovftool import OVFTool
        from COT.helpers.qemu_img import QEMUImg
        from COT.helpers.vmdktool import VmdkTool
        from COT.helpers import HelperError, HelperNotFoundError
        result = True
        results = {}
        for cls in [FatDisk, MkIsoFS, OVFTool, QEMUImg, VmdkTool]:
            helper = cls()
            if helper.path:
                results[helper.name] = ("version {0}, present at {1}"
                                        .format(helper.version,
                                                str(helper.path)))
            elif self.verify_only:
                results[helper.name] = "NOT FOUND"
            else:
                try:
                    helper.install_helper()
                    results[helper.name] = (
                        "successfully installed to {0}, version {1}"
                        .format(str(helper.path), helper.version))
                except (NotImplementedError,
                        HelperError,
                        HelperNotFoundError) as e:
                    results[helper.name] = "INSTALLATION FAILED: " + str(e)
                    result = False

        print("Results:")
        print("-------------")
        wrapper = textwrap.TextWrapper(width=self.UI.terminal_width(),
                                       initial_indent="",
                                       subsequent_indent=(" " * 14))
        for k in sorted(results.keys()):
            print(wrapper.fill("{0:13} {1}".format(k + ":", results[k])))
        print("")
        if not result and not self.ignore_errors:
            raise EnvironmentError(1, "Unable to install some helpers")

    def create_subparser(self, parent):
        """Add subparser for the CLI of this submodule.

        :param object parent: Subparser grouping object returned by
            :func:`ArgumentParser.add_subparsers`

        :returns: ``('install-helpers', subparser)``
        """
        p = parent.add_parser(
            'install-helpers',
            help="Install third-party helper programs that COT may require",
            usage=self.UI.fill_usage('install-helpers',
                                     ["--verify-only",
                                      "[--ignore-errors]"]),
            description="""
Install third-party helper programs for COT.

* qemu-img (http://www.qemu.org/)
* mkisofs  (http://cdrecord.org/)
* ovftool  (https://www.vmware.com/support/developer/ovf/)
* fatdisk  (http://github.com/goblinhack/fatdisk)
* vmdktool (http://www.freshports.org/sysutils/vmdktool/)""",
            epilog=self.UI.fill_examples([
                ("Verify whether COT can find all expected helper programs",
                 """
> cot install-helpers --verify-only
Results:
-------------
fatdisk:      present at /opt/local/bin/fatdisk
mkisofs:      present at /opt/local/bin/mkisofs
ovftool:      present at /usr/local/bin/ovftool
qemu-img:     present at /opt/local/bin/qemu-img
vmdktool:     NOT FOUND""".strip()),
                ("Have COT attempt to install missing helpers for you. "
                 "Note that most helpers require administrator / ``sudo`` "
                 "privileges to install. If any installation fails, "
                 "COT will exit with an error, unless you pass "
                 "``--ignore-errors``.",
                 """
> cot install-helpers
    INFO: Installing 'fatdisk'...
    INFO: Compiling 'fatdisk'
    INFO: Calling './RUNME'...
(...)
    INFO: ...done
    INFO: Compilation complete, installing now
    INFO: Calling 'sudo cp fatdisk /usr/local/bin/fatdisk'...
    INFO: ...done
    INFO: Successfully installed 'fatdisk'
    INFO: Installing 'vmdktool'...
    INFO: vmdktool requires 'zlib'... installing 'zlib'
    INFO: Calling 'sudo apt-get -q install zlib1g-dev'...
(...)
    INFO: ...done
    INFO: Compiling 'vmdktool'
    INFO: Calling 'make CFLAGS="-D_GNU_SOURCE -g -O -pipe"'...
(...)
    INFO: ...done
    INFO: Compilation complete, installing now.
    INFO: Calling 'sudo mkdir -p --mode=755 /usr/local/man/man8'...
    INFO: ...done
    INFO: Calling 'sudo make install'...
install -s vmdktool /usr/local/bin/
install vmdktool.8 /usr/local/man/man8/
    INFO: ...done
    INFO: Successfully installed 'vmdktool'
Results:
-------------
fatdisk:      successfully installed to /usr/local/bin/fatdisk
mkisofs:      present at /usr/bin/mkisofs
ovftool:      INSTALLATION FAILED: No support for automated
              installation of ovftool, as VMware requires a site
              login to download it. See
              https://www.vmware.com/support/developer/ovf/
qemu-img:     present at /usr/bin/qemu-img
vmdktool:     successfully installed to /usr/local/bin/vmdktool

Unable to install some helpers""".strip())]),
            formatter_class=argparse.RawDescriptionHelpFormatter)

        group = p.add_mutually_exclusive_group()

        # TODO - nice to have!
        # p.add_argument('--dry-run', action='store_true',
        #              help="Report the commands that would be run to install "
        #             "any helper programs, but do not actually run them.")

        group.add_argument('--verify-only', action='store_true',
                           help="Only verify helpers -- do not attempt to "
                           "install any missing helpers.")

        group.add_argument('-i', '--ignore-errors', action='store_true',
                           help="Do not fail even if helper installation "
                           "fails.")

        p.set_defaults(instance=self)

        return 'install-helpers', p
