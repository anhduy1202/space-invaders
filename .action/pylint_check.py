#!/usr/bin/env python3
#
# Copyright 2021 Michael Shafae
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
""" Check the given files to see if they conform to good programming
    practices using clang-tidy. """

import sys
import logging
import os.path
from logger import setup_logger
from pysrcutilities import pylint_check, glob_py_src_files


def main():
    """Main function; process each file given through the linter."""
    status = 0
    setup_logger()
    logger = logging.getLogger("mshafae")
    if len(sys.argv) < 2:
        logger.warning("Only %s arguments provided.", len(sys.argv))
        logger.warning("Provide a target directory to search for .py files.")
    # src_files = []
    # for in_directory in sys.argv[1:]:
    #     src_files = src_files + glob_py_src_files(in_directory)
    # if len(src_files):
    #     logger.debug('Source files to be checked are %s', ', '.join(src_files))
    # else:
    #     logger.warning('No source files in the repository.')
    #     status = 1
    for in_file in sys.argv[1:]:
        logger.info("Linting file: %s", in_file)
        if not os.path.exists(in_file):
            logger.debug("File %s does not exist. Continuing.", in_file)
            continue
        lint_has_passed, lint_warnings = pylint_check(in_file)
        if not lint_has_passed:
            logger.error("Linter found improvements.")
            logger.warning("\n".join(lint_warnings))
            status = 1
        else:
            logger.info("Linting passed")
    sys.exit(status)


if __name__ == "__main__":
    main()
