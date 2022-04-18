"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""

###############
# Imports
###############
import csv
import json
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


def write_to_csv(results, filename):
    """
    Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    Technically see:
    https://docs.python.org/3/library/csv.html#csv.DictWriter
    and for examples (e.g. number 3 of the following link):
    https://www.programcreek.com/python/example/3190/csv.DictWriter

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """

    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )

    # Write the results to a CSV file, following the specification in the
    # instructions.
    try:
        with open(filename, 'w') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            # iteration over close approach instances
            for close_approach in results:
                writer.writerow({
                    'datetime_utc': datetime_to_str(close_approach.time),
                    'distance_au': close_approach.distance,
                    'velocity_km_s': close_approach.velocity,
                    'designation': close_approach.neo.designation,
                    'name': close_approach.neo.name,
                    'diameter_km': close_approach.neo.diameter,
                    'potentially_hazardous': close_approach.neo.hazardous,
                })
    except ValueError as err:
        traceback.print_tb(err.__traceback__)
        LOGGER.error(f"write_to_csv:\n{err}", exc_info=True)


def write_to_json(results, filename):
    """
    Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    Technically see:
    https://docs.python.org/3/library/json.html

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """

    # Write the results to a JSON file, following the specification in the instructions.
    # Have in mind to use string representations for datetime attribute.
    json_list = []

    try:
        for approach in results:
            json_headers = {
                'datetime_utc': datetime_to_str(
                    approach.time),
                'distance_au': approach.distance,
                'velocity_km_s': approach.velocity,
                'neo': {
                    'designation': approach.designation,
                    'name': "" if (
                        (approach.neo.name is None) or len(
                            approach.neo.name.strip()) == 0) else approach.neo.name,
                    'diameter_km': approach.neo.diameter,
                    'potentially_hazardous': approach.neo.hazardous}}
            json_list.append(json_headers)

        with open(filename, "w") as outfile:
            json.dump(json_list, outfile, indent=2)
    except ValueError as err:
        traceback.print_tb(err.__traceback__)
        LOGGER.error(f"write_to_json:\n{err}", exc_info=True)
