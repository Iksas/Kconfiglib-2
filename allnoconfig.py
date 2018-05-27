#!/usr/bin/env python

# Works like 'make allnoconfig'. Verified by the test suite to generate
# identical output to 'make allnoconfig' for all ARCHes.
#
# See the examples/allnoconfig_walk.py example script for another variant.
#
# Usage for the Linux kernel:
#
#   $ make [ARCH=<arch>] scriptconfig SCRIPT=Kconfiglib/allnoconfig.py

import os
import sys

import kconfiglib

def main():
    if len(sys.argv) > 2:
        sys.exit("usage: {} [Kconfig]".format(sys.argv[0]))

    kconf = kconfiglib.Kconfig("Kconfig" if len(sys.argv) < 2 else sys.argv[1])

    # Avoid warnings printed by Kconfiglib when assigning a value to a symbol that
    # has no prompt. Such assignments never have an effect.
    kconf.disable_warnings()

    # Small optimization
    BOOL_TRI = (kconfiglib.BOOL, kconfiglib.TRISTATE)

    for sym in kconf.defined_syms:
        if sym.orig_type in BOOL_TRI:
            sym.set_value(2 if sym.is_allnoconfig_y else 0)

    config_filename = os.environ.get("KCONFIG_CONFIG")
    if config_filename is None:
        config_filename = ".config"

    kconf.write_config(config_filename)

if __name__ == "__main__":
    main()