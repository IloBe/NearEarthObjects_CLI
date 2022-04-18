"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""

###############
# Imports
###############

# import own files
import config as cfg


###############
# Coding
###############

# set logging (simple root logger)
cfg.config_basic_root_logger()
LOGGER = cfg.get_logger()


class NEODatabase:
    """
    A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos, approaches):
        """
        Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        LOGGER.info(
            "NEODatabase init: initialise and fill neos and approaches dicts...")

        self._neos = neos
        self._approaches = approaches

        # What additional auxiliary data structures will be useful?
        # Link together the NEOs and their close approaches.
        # =>
        # we need all designations and names of NEO's for dict comprehension
        # and to append associated designation CAD object to neo.approaches list
        # and adding neo to it; additionally to use getter functions of this
        # class

        self._designation_dict = {}
        self._name_dict = {}

        for neo in self._neos:
            # designation is a mandatory attribute
            self._designation_dict[neo.designation] = neo
            # name is an optional attribute
            if neo.name:
                self._name_dict[neo.name] = neo

        for cad in self._approaches:
            # designation is added to approach with @property decorator
            try:
                neo = self._designation_dict[cad.designation]
                if neo:
                    neo.approaches.append(cad)
                    cad.neo = neo
            except KeyError as err:
                # if designation key does not exist: log it and
                LOGGER.error(f"NEODatabase init: KeyError:\n{err}", exc_info=True)


    def get_neo_by_designation(self, designation):
        """
        Find and return an NEO by its primary designation.
        If no match is found in the associated database dictionary, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.
        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """

        # Fetch an NEO by its primary designation; upper works best
        return self._designation_dict.get(designation.upper(), None)


    def get_neo_by_name(self, name):
        """
        Find and return an NEO by its name.
        If no match is found in the associated database dictionary, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.
        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """

        # Fetch an NEO by its name, capitalize works best, not upper or lower
        return self._name_dict.get(name.capitalize(), None)


    def query(self, filters=()):
        """
        Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaningfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """

        # Generate `CloseApproach` objects that match all of the filters.
        # Don't use 'filter' because it is a specific function, call it
        # 'marker'
        for approach in self._approaches:
            flag = True
            for marker in filters:
                if not marker(approach):
                    flag = False
                    break

            if flag:
                yield approach
