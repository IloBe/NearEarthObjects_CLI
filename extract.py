"""
Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""

###############
# Imports
###############
import csv
import json

from models import NearEarthObject, CloseApproach
from helpers import cd_to_datetime

# own created files
import config as cfg

###############
# Constants
###############

# set logging
cfg.config_basic_root_logger()
LOGGER = cfg.get_logger()


###############
# Coding
###############

def load_neos(neo_csv_path):
    """
    Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # Load NEO data from the given CSV file. We use the DictReader class.
    LOGGER.info(
        "extract: load_neos: read .csv file via DictReader to get NEO attributes ...")

    neos_in = []

    with open(neo_csv_path, 'r') as infile:
        reader = csv.DictReader(infile)

        for elem in reader:
            #LOGGER.info(f"NEO csv file elem:\n{elem}")

            if (elem['pdes'] is not None) and len(elem['pdes'].strip()) > 0:
                elem['pdes'] = str(elem['pdes'])

            if (elem['name'] is not None) and len(elem['pdes'].strip()) > 0:
                elem['name'] = str(elem['name'])
            else:
                elem['name'] = None

            if (elem['diameter'] is not None) and len(
                    elem['diameter'].strip()) > 0:
                elem['diameter'] = float(elem['diameter'])
            else:
                elem['diameter'] = float('nan')

            if (elem['pha'] is not None) and \
                    len(elem['pha'].strip()) > 0 and elem['pha'] in ('Y', 'y'):
                elem['pha'] = True
            else:
                elem['pha'] = False

            neo = NearEarthObject(
                designation=elem['pdes'],
                name=elem['name'],
                diameter=elem['diameter'],
                hazardous=elem['pha'],
            )

            neos_in.append(neo)

    return neos_in


def load_approaches(cad_json_path):
    """
    Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # Load close approach data from the given JSON file.
    LOGGER.info(
        "extract: load_approaches: read .json file to get close approach attributes ...")

    cads_in = []

    with open(cad_json_path, 'r') as infile:
        contents = json.load(infile)  # Parse JSON data into a Python object
        contents_data = contents['data']
        contents_fields = contents['fields']

        # info:
        # .json data collection items include values only, no direct readable keys;
        # the attribute keys are stored in the fields collection and according position inside
        # that fields collection delivering attribute value position info of data items;
        # implementation: using enumerate, if the key appears more than once -
        # which is a mistake => we use the first index of position 0
        des_indexes = [i for i, x in enumerate(contents_fields) if x == 'des']
        cd_indexes = [i for i, x in enumerate(contents_fields) if x == 'cd']
        dist_indexes = [i for i, x in enumerate(
            contents_fields) if x == 'dist']
        v_rel_indexes = [i for i, x in enumerate(
            contents_fields) if x == 'v_rel']
        LOGGER.info(
            "Found indexes in fields collection of close approach .json cad file:")
        LOGGER.info(
            f"des: {des_indexes}, cd: {cd_indexes}, dist: {dist_indexes}, v_rel: {v_rel_indexes}")

        for data in contents_data:
            #LOGGER.info(f"CA json file data:\n{data}")

            # remember: designation shall be a mandatory attribute,
            # nevertheless we check if none
            if data[des_indexes[0]] is not None:
                data[des_indexes[0]] = data[des_indexes[0]]

            # date time handling (formatted calendar date/time, in UTC);
            # valid is eg "YYYY-bb-DD hh:mm")
            # see: https://docs.python.org/3/library/datetime.html
            if data[cd_indexes[0]] is None or len(
                    data[cd_indexes[0]].strip()) == 0:
                data[cd_indexes[0]] = "Date time string not available"
            else:
                data[cd_indexes[0]] = cd_to_datetime(data[cd_indexes[0]])

            # distance handling
            if data[dist_indexes[0]] is None or len(
                    data[dist_indexes[0]].strip()) == 0:
                data[dist_indexes[0]] = float('nan')
            else:
                data[dist_indexes[0]] = float(data[dist_indexes[0]])

            # velocity handling
            if data[v_rel_indexes[0]] is None or len(
                    data[v_rel_indexes[0]].strip()) == 0:
                data[v_rel_indexes[0]] = float('nan')
            else:
                data[v_rel_indexes[0]] = float(data[v_rel_indexes[0]])

            cad = CloseApproach(
                des=data[des_indexes[0]],         # for _designation
                cd=data[cd_indexes[0]],           # for time
                dist=data[dist_indexes[0]],       # for distance
                v_rel=data[v_rel_indexes[0]],     # for relative velocity
                neo=None,                         # for associated neo object
            )

            cads_in.append(cad)

    return cads_in
