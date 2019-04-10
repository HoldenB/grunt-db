import sqlite3

sqlite_file = 'game_db.sqlite'

table_zone = 'zone'
table_character = 'character'
table_e_weapon = 'equipped_weapon'


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None


def select_all_zones(conn):
    """
    Query all rows in the zone table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_zone}")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_all_characters(conn):
    """
    Query all rows in the character table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_character}")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_all_weapons(conn):
    """
    Query all rows in the weapons table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_e_weapon}")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_zone_by_id(conn, zid):
    """
    Query zones by id
    :param conn: the Connection object
    :param zid:
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_zone} WHERE zid={zid}")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_wep_rarity_from_char_name(conn, c_name):
    """
    Select weapon rarity from a character name
    :param conn:
    :param c_name:
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"SELECT rarity FROM {table_e_weapon}, {table_character}"
                f" WHERE c_name='{c_name}' AND {table_character}.eWid={table_e_weapon}.eWid")

    rows = cur.fetchall()

    for row in rows:
        print(row)


connection = create_connection(sqlite_file)
c = connection.cursor()

# Example display all rows in each of our tables
select_all_zones(connection)
print()
select_all_characters(connection)
print()
select_all_weapons(connection)
print()

# Select zones by zid
select_zone_by_id(connection, 0)
print()
select_zone_by_id(connection, 4)
print()

# Select the weapon rarity of a characters weapon based on their name
select_wep_rarity_from_char_name(connection, 'KingPrateek')
print()
select_wep_rarity_from_char_name(connection, 'AKTheSlayer')
print()

