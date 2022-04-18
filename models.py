"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
For the NearEarthObject class I use the dictionary parameter concept using **info.
For the CloseApproach class I use the parameter list concept of the attributes of
interest. The attribute keys are from the readme file.
"""

###############
# Imports
###############
import math
import traceback

from helpers import datetime_to_str

# import own files
import config as cfg


###############
# Coding
###############

# set logging (simple root logger)
cfg.config_basic_root_logger()
LOGGER = cfg.get_logger()

#
# projects class objects
#


class NearEarthObject:
    """
    A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """
        Create a new `NearEarthObject`.

        :param info: (dictionary) A dictionary of excess keyword arguments supplied to
                the constructor.

        We are interested in the following key-value pairs of the dictionary input:
        - designation: (key label: pdes) The primary designation for this NEO,
                mandatory string which shall not be empty or whitespaces
        - name: (key label: name) The IAU name for this NEO (default: None)
        - diameter: (key label: diameter) The diameter, in kilometers, of this NEO
                (default: float('nan'))
        - hazardous: (key label: pha) Whether or not this NEO is potentially hazardous
                (default: False)
        """
        # Assign information from the arguments passed to the constructor
        # onto attributes named `designation`, `name`, `diameter`, and `hazardous`.
        # You should coerce these values to their appropriate data type and
        # handle any edge cases, such as a empty name being represented by `None`
        # and a missing diameter being represented by `float('nan')`.

        LOGGER.info("NearEarthObject init: info dict items initialisation...")

        # set default initialisation
        self.designation = 'designation unknown'
        self.name = None
        self.diameter = float('nan')
        self.hazardous = False

        # with info dictionary: have a look to the items of interest
        for key, value in info.items():
            try:
                if key == 'designation':  # mandatory attribute
                    LOGGER.info(f"mandatory designation as string: {value}")
                    self.designation = str(value)

                if key.lower() == 'name':
                    self.name = None if value is None or len(
                        value.strip()) == 0 else str(value)

                if key.lower() == 'diameter':
                    self.diameter = float(
                        'nan') if value is None else float(value)

                if key.lower() == 'hazardous':
                    self.hazardous = False if (value in [None, False]) else True
            except ValueError as err:
                print(
                    "NearEarthObject init: ValueError: designation, name, diameter or hazardous:")
                traceback.print_tb(err.__traceback__)
                LOGGER.error(
                    f"NearEarthObject init: ValueError:\n{err}",
                    exc_info=True)
            except NameError as err:
                print(
                    "NearEarthObject init: NameError: designation, name, diameter or hazardous:")
                traceback.print_tb(err.__traceback__)
                LOGGER.error(
                    f"NearEarthObject init: NameError:\n{err}",
                    exc_info=True)

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """ Return a representation of the full name of this NEO. """
        # Use self.designation and self.name to build a fullname for this
        # object.
        return f"{self.designation} ("\
            f"{'no IAU name' if ((self.name is None) or len(self.name.strip())==0) else self.name})"

    def __str__(self):
        """ Return `str(self)`. """
        # Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.

        # take care if the diameter attribute value exists or not (can be
        # float('nan'))

        str_result = ""
        if not self.diameter or math.isnan(self.diameter):
            str_result = f"NEO {self.fullname} " \
                f"{'is' if self.hazardous else 'is not'} potentially hazardous."
        else:
            str_result = f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km and " \
                f"{'is' if self.hazardous else 'is not'} potentially hazardous."
        return str_result

    def __repr__(self):
        """ Return `repr(self)`, a computer-readable string representation of this object. """
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"

    def serialize(self):
        """
        Serializes the NearEarthObject instance.

        :return: A dictionary containing relevant attributes for CSV or JSON serialization
        """
        return {
            'designation': self.designation,
            'name': "" if (
                (self.name is None) or len(
                    self.name.strip()) == 0) else self.name,
            'diameter': self.diameter,
            'hazardous': self.hazardous,
        }


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.

    Parameter key labels are presented in the projects readme file.
    """

    def __init__(
            self,
            des,
            cd,
            dist=float('nan'),
            v_rel=float('nan'),
            neo=None):
        """
        Create a new `CloseApproach` about the attributes of interest.

        :param des: (string) The primary designation of the asteroid or comet
                (e.g., 443, 2000 SG344).
        :param cd: (datetime) The time of closest approach (formatted calendar date/time, in UTC);
                            "YYYY-bb-DD hh:mm" format shall be used as argument;
                            according https://docs.python.org/3/library/datetime.html
                            %b means: Month as locale’s abbreviated name, but in this case we use:
                            Jan, Feb, …, Dec (en_US) as values for month information.
        :param dist: (float) The nominal approach distance (in au - astronomical unit) of the NEO.
        :param v_rel: (float) The velocity relative to approach body at close approach (in km/s).
        :param neo: (NearEarthObject) The `NearEarthObject` making a close approach to Earth.

        Regarding the associated NEO: The `NearEarthObject` making a close approach to Earth
        is referenced via private attriute _designation.
        Have in mind, the NEO may change or be replaced in the database.
        """

        # Assign information from the arguments passed to the constructor
        # onto attributes named `_designation`, `time`, `distance`, and `velocity`.
        # You should coerce these values to their appropriate data type and handle any edge cases.
        # The `cd_to_datetime` function will be useful.

        # private designation attribute
        try:
            self._designation = des
        except ValueError as err:
            print("CloseApproach init: ValueError regarding _designation (des)")
            traceback.print_tb(err.__traceback__)
            LOGGER.error(
                f"CloseApproach init: Designation:\n{err}",
                exc_info=True)

        # time handling
        # specific format is expected at the end: %Y-%b-%m %H:%M; is already
        # formated before
        try:
            if cd is not None:
                self.time = cd
            else:
                self.time = None
        except ValueError as err:
            traceback.print_tb(err.__traceback__)
            LOGGER.error(f"CloseApproach init: Time:\n{err}", exc_info=True)

        # distance handling, default is float('nan')
        try:
            self.distance = float(dist)
        except ValueError as err:
            print("CloseApproach init: ValueError regarding distance (dist)")
            traceback.print_tb(err.__traceback__)
            LOGGER.error(
                f"CloseApproach init: Distance:\n{err}",
                exc_info=True)

        # velocity handling, default is float('nan')
        try:
            self.velocity = float(v_rel)
        except ValueError as err:
            print("CloseApproach init: ValueError regarding relative velocity (v_rel)")
            traceback.print_tb(err.__traceback__)
            LOGGER.error(
                f"CloseApproach init: Velocity:\n{err}",
                exc_info=True)

        # Create an attribute for the referenced NEO
        self.neo = neo

    @property
    def time_str(self):
        """
        Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        # Use this object's `.time` attribute and the `datetime_to_str` function to
        # build a formatted representation of the approach time.
        return f"Approach time of this close object: " \
               f"{datetime_to_str(self.time) if self.time else 'unknown'}"

    @property
    def designation(self):
        """
        Returns the self._designation (private attribute) of the associated NEO.

        :return: self._designation
        """
        return self._designation

    def __str__(self):
        """ Return `str(self)`. """
        # Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.

        str_result = ""
        if (not self.distance or math.isnan(self.distance)) and \
                (not self.velocity or math.isnan(self.velocity)):
            str_result = f"{self.time_str}; NEO '{self.neo.fullname}' approaches Earth " \
                f"with unknown distance and velocity."
        elif not self.velocity or math.isnan(self.velocity):
            str_result = f"{self.time_str}; NEO '{self.neo.fullname}'" \
                f" approaches Earth at a distance of " \
                f"{self.distance: .2f} au and an unknown velocity."
        elif not self.distance or math.isnan(self.distance):
            str_result = f"{self.time_str}; NEO '{self.neo.fullname}'" \
                f" approaches Earth at an unknown " \
                f"distance and a velocity of {self.velocity: .2f} km / s."
        else:
            str_result = f"{self.time_str}; NEO '{self.neo.fullname}'" \
                f" approaches Earth at a distance of " \
                f"{self.distance: .2f} au and a velocity of {self.velocity: .2f} km / s."
        return str_result

    def __repr__(self):
        """ Return `repr(self)`, a computer-readable string representation of this object. """
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"

    def serialize(self):
        """
        Serializes the CloseApproach instance.

        :return: A dictionary containing relevant attributes for CSV or JSON serialization
        """
        return {
            'designation': self.designation,
            'time': self.time,
            'distance': self.distance,
            'velocity': self.velocity,
            'neo': self.neo,
        }
