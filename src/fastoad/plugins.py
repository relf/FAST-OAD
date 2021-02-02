"""
Plugin system for module declaration.
"""
#  This file is part of FAST-OAD : A framework for rapid Overall Aircraft Design
#  Copyright (C) 2021 ONERA & ISAE-SUPAERO
#  FAST is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from importlib.resources import open_text, contents

import numpy as np
from pkg_resources import iter_entry_points

from fastoad.openmdao.variables import DESCRIPTION_FILENAME, Variable

_LOGGER = logging.getLogger(__name__)  # Logger for this module


def load_plugins():
    """
    Loads declared plugins.
    """
    # Loading plugins
    discovered_plugins = {
        entry_point.name: entry_point.load() for entry_point in iter_entry_points("fastoad.models")
    }
    for plugin_name, package in discovered_plugins.items():
        _LOGGER.info("Loaded FAST-OAD plugin %s", plugin_name)
        if DESCRIPTION_FILENAME in contents(package):
            try:
                with open_text(package, DESCRIPTION_FILENAME) as desc_io:
                    vars_descs = np.genfromtxt(desc_io, delimiter="\t", dtype=str)
                Variable.update_variable_descriptions(vars_descs)
                _LOGGER.info("Loaded variable descriptions from plugin %s", plugin_name)
            except Exception as exc:
                _LOGGER.error(
                    "Could not read variable description for plugin %s. Error log is:\n%s",
                    plugin_name,
                    exc,
                )
        else:
            _LOGGER.info("No variable description in plugin %s", plugin_name)
