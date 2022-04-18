# Extensions of the NEO Project

## Overview

Regarding the delivered files some changes are added to the README.md file to understand near-Earth objects a little bit more detailed (e.g. by ESA links and information), the aim of coding blocks are documented in each software file and technical changes are added as mentioned below.

Therefore nearly all delivered project files have been changed.


## Technical Changes
### Configuration
A specific configuration file `config.py` is added. This file is the central entry point for constants, like path information, which are in the original architecture are added directly in each file where they have been necessary. So, such information has been redundant and if constants values would change several files have to be modified. Therefore such behaviour has been changed, so, you can find all constants in only one file labelled config.py.

### Logging
A simple log behaviour using the `root logger` has been added as well. Its configuration is part of the **config.py** file and used for 2 use cases:
- exception handling with error logs
- workflow handling with information logs

Furthermore, logging simplifies debugging if issues would appear during usage of the project code and therefore modifications would be necessary. 

All log files are created for each day the Neo command line tool is used and such file is stored in the newly created logs directory.

Not having such kind of files in the GitHub repository, the `.gitignore` file is changed only having the directory available, but not the files.

## Deliverables
As mentioned in the 'rubric' part of the project, one goal is to follow "best practices" in Python as the [PEP 8](https://www.python.org/dev/peps/pep-0008/) and [PEP 257](https://www.python.org/dev/peps/pep-0257/) rules for style and docstring convention. So, all files are checked by using [autopep8](https://pypi.org/project/autopep8/) and [pylint](https://pylint.pycqa.org/en/latest/user_guide/run.html) tools. As a final result, all files reached a pylint score >=8/10.
