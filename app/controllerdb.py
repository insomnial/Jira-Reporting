import sqlite3, os
import resources


###############################################################################
##  CONSTANTS
###############################################################################
DB_FOLDER = 'db'


###############################################################################
##  PRIVATE
###############################################################################


# create in DB_FOLDER
def _connectDbLocal(aUri) -> sqlite3:
    print(f"> Connect to db `{aUri}` in folder `{DB_FOLDER}`")
    with sqlite3.connect(DB_FOLDER + os.path.sep + aUri) as conn:
        return conn


# create in memory
def _connectDbMem() -> sqlite3:
    print(f"> Connect to `memory` db")
    with sqlite3.connect(':memory:') as conn:
        # TODO build db structure
        return conn


# make sure DB_FOLDER folder exists
def _checkForDbFolder() -> bool:
    return os.path.exists(DB_FOLDER)


# create DB_FOLDER folder
def _createFolderDb():
    print(f"> Create new folder {DB_FOLDER}")
    os.mkdir(DB_FOLDER)


def _buildSqlFromTemplate(aConn : sqlite3.Cursor):
    print(f"> Build database from template")
    # Open the external sql file.
    script_dir = os.path.dirname(__file__)
    file = open(os.path.join(script_dir, 'resources', 'jira_reporting.sql'), 'r')
    # Read out the sql script text in the file.
    sql_script_string = file.read()
    # Close the sql file object.
    file.close()
    # Execute the read out sql script string.
    cursor = aConn.cursor()
    cursor.executescript(sql_script_string)
    aConn.commit()
    cursor.close()


def _updateOpenTimestamp(aConn : sqlite3.Cursor):
    print(f"> Update open timestamp")
    cursor = aConn.cursor()
    cursor.execute("INSERT INTO metadata (id, open_timestamp) VALUES (Null, datetime('now'))")
    aConn.commit()
    cursor.close()


def _loadFromDb(aConn : sqlite3.Cursor):
    cursor = aConn.cursor()


def init(aUri = None):
    conn = None
    if aUri != None:
        print(f"> Check for db folder")
        if _checkForDbFolder():
            print(f" # PASS")
        else:
            print(f" ! Db folder does not exist")
            _createFolderDb()

        conn = _connectDbLocal(aUri)
    else:
        conn = _connectDbMem()

    assert conn != None

    print(f"> Check for db structure")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT open_timestamp FROM `metadata` ORDER BY open_timestamp DESC LIMIT 1")
        print(f" # PASS {cursor.fetchone()}")
    except sqlite3.OperationalError:
        print(f" ! No metadata table found")
        _buildSqlFromTemplate(conn)
    finally:
        cursor.close()

    _updateOpenTimestamp(conn)

    return conn
