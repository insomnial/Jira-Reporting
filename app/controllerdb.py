import sqlite3, os


###############################################################################
##  CONSTANTS
###############################################################################
DB_FOLDER = 'db'


###############################################################################
##  PRIVATE
###############################################################################

# create DB structure
def _createDbStructure(aConn):
    pass


# create in DB_FOLDER
def _connectDbLocal(aUri) -> sqlite3:
    print(f"> Connect to db `{aUri}` in folder `{DB_FOLDER}`")
    with sqlite3.connect(DB_FOLDER + os.path.sep + aUri) as conn:
        # TODO build db structure
        _createDbStructure(conn)
        return conn

# create in memory
def _connectDbMem() -> sqlite3:
    print(f"> Connect to `memory` db")
    with sqlite3.connect(':memory:') as conn:
        # TODO build db structure
        _createDbStructure(conn)
        return conn


# make sure DB_FOLDER folder exists
def _checkForDbFolder() -> bool:
    return os.path.exists(DB_FOLDER)


# create DB_FOLDER folder
def _createFolderDb():
    print(f"> Create new folder {DB_FOLDER}")
    os.mkdir(DB_FOLDER)


def init(aUri = None):

    if aUri != None:
        print(f"> Check for db folder")
        if _checkForDbFolder():
            print(f" # PASS")
        else:
            print(f" ! Db folder does not exist")
            _createFolderDb()

        conn = _connectDbLocal(aUri)
        return conn
    else:
        conn = _connectDbMem()
        return conn
