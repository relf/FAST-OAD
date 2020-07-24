"""Structure for managing flight point data."""
#  This file is part of FAST : A framework for rapid Overall Aircraft Design
#  Copyright (C) 2020  ONERA & ISAE-SUPAERO
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

from fastoad.base.dict import DynamicAttributeDict


class FlightPoint(DynamicAttributeDict):
    """
    Class for storing data for one flight point.

    An instance is a simple dict, but for convenience, each item can be accessed
    as an attribute (inspired by pandas DataFrames). Hence, one can write::

        >>> fp = FlightPoint(speed=250., altitude=10000.)
        >>> fp["speed"]
        250.0
        >>> fp2 = FlightPoint({"speed":150., "altitude":5000.})
        >>> fp2.speed
        250.0
        >>> fp["mass"] = 70000.
        >>> fp.mass
        70000.0
        >>> fp.mass = 50000.
        >>> fp["mass"]
        50000.0

    Note: constructor will forbid usage of unknown keys, but other methods will
    allow them, while not making the matching between dict keys and attributes,
    hence::

        >>> fp["foo"] = 42  # Ok
        >>> bar = fp.foo  # raises exception !!!!
        >>> fp.foo = 50  # allowed by Python
        >>> # But inner dict is not affected:
        >>> fp.foo
        50
        >>> fp["foo"]
        42

    This class is especially useful for generating pandas DataFrame: a pandas
    DataFrame can be generated from a list of dict... or a list of FlightPoint
    instances.

    The set of dictionary keys that are mapped to instance attributes is given by
    the :attr:`labels` class attribute. Though it looks useful to limit the
    authorized fields to avoid bugs from typos, you may modify this class
    attribute to suit your needs.
    """

    # Set of dictionary keys that are mapped to instance attributes.
    labels = {
        "time",  # in seconds
        "altitude",  # in meters
        "ground_distance",  # in m.
        "mass",  # in kg
        "true_airspeed",  # in m/s
        "equivalent_airspeed",  # in m/s
        "mach",
        "engine_setting",  # EngineSetting value
        "CL",
        "CD",
        "drag",  # in Newtons
        "thrust",  # in Newtons
        "thrust_rate",
        "sfc",  # in kg/N/s
        "slope_angle",  # in radians
        "acceleration",  # in m/s**2
        "name",
    }

    def __init__(self, *args, **kwargs):
        """

        :param args: a dict-like object where all keys are contained in :attr:`labels`
        :param kwargs: must be name contained in :attr:`labels`
        """

        self._set_attribute_defaults({name: None for name in self.labels})

        super().__init__(*args, **kwargs)
