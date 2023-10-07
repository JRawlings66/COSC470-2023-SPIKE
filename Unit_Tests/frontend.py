# choose a database and connect
# might not use this but it's here

import sys

class Invalid_Arg(Exception):
    def __init__(self):
        message = "Please select a valid option (1-4):\n" + \
                  "  1.  \n" + \
                  "  2.  ()\n" + \
                  "  3.  ()\n" + \
                  "  4.  ()\n"
        super().__init__(message)

args = sys.argv
valid_args = [1, 2, 3, 4]
databases = {
    1: ["", ""]
    # TODO; include other database names in dict
}

if len(sys.argv) != 2:
    # proper args not included
    raise Invalid_Arg

if sys.argv[1] not in valid_args:
    # invalid database selection
    raise Invalid_Arg

# dbname
db = databases[1]