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


def create_zone(conn, zone_string):
    """
    Create a new zone in the zones table
    :param conn:
    :param zone_string:
    :return: project id
    """
    insert_query = f''' INSERT INTO {table_zone}(zid, num_chars, num_creatures, z_level_range, difficulty)
              VALUES(?,?,?,?,?) '''

    cur = conn.cursor()
    cur.execute(insert_query, zone_string)


def create_character(conn, char_string):
    """
    Create a new character in the character table
    :param conn:
    :param char_string:
    :return: project id
    """
    insert_query = f''' INSERT INTO {table_character}(cid, c_name, time_played, char_level, char_kills, eWid)
              VALUES(?,?,?,?,?,?) '''

    cur = conn.cursor()
    cur.execute(insert_query, char_string)


def create_weapon(conn, weapon_string):
    """
    Create a new weapon in the weapons table
    :param conn:
    :param weapon_string:
    :return: project id
    """
    insert_query = f''' INSERT INTO {table_e_weapon}(eWid, damage, w_name, w_level, w_type, rarity, zid)
              VALUES(?,?,?,?,?,?,?) '''

    cur = conn.cursor()
    cur.execute(insert_query, weapon_string)


# Connecting to the database file
connection = create_connection(sqlite_file)
c = connection.cursor()

# Zone table
c.execute(f'CREATE TABLE {table_zone} ('
          'zid              INTEGER     PRIMARY KEY,'
          'num_chars        INTEGER,'
          'num_creatures    INTEGER,'
          'z_level_range    VARCHAR(20),'
          'difficulty       VARCHAR(20)'
          ');')

# Equipped Weapon table
c.execute(f'CREATE TABLE {table_e_weapon} ('
          'eWid             INTEGER      PRIMARY KEY,'
          'damage           REAL,'
          'w_name           VARCHAR(20),'
          'w_level          INTEGER,'
          'w_type           VARCHAR(20),'
          'rarity           VARCHAR(20),'
          'zid              INTEGER,'
          f'FOREIGN KEY(zid) REFERENCES {table_zone}(zid)'
          ');')

# Character table
c.execute(f'CREATE TABLE {table_character} ('
          'cid             INTEGER      PRIMARY KEY,'
          'c_name          VARCHAR(20),'
          'time_played     REAL,'
          'char_level      INTEGER,'
          'char_kills      INTEGER,'
          'eWid            INTEGER,'
          f'FOREIGN KEY(eWid) REFERENCES {table_e_weapon}(eWid)'
          ');')

# Insert some initial zone data
zone_0 = ('0', '60', '20', '10-20', 'Easy')
zone_1 = ('1', '55', '85', '30-40', 'Medium')
zone_2 = ('2', '20', '102', '50-60', 'Medium')
zone_3 = ('3', '10', '115', '70-80', 'Hard')
zone_4 = ('4', '5', '300', '90-100', 'Very Hard')

create_zone(connection, zone_0)
create_zone(connection, zone_1)
create_zone(connection, zone_2)
create_zone(connection, zone_3)
create_zone(connection, zone_4)

# Insert some initial character data
char_0 = ('0', 'KingPrateek', '30', '20', '150', '0')
char_1 = ('1', 'AKTheSlayer', '1000', '80', '550', '3')
char_2 = ('2', 'TheRoachMan', '40', '30', '200', '1')
char_3 = ('3', 'StephenDOTnET', '30', '60', '20', '2')
char_4 = ('4', 'ChihTinggggg', '100', '100', '5', '2')

create_character(connection, char_0)
create_character(connection, char_1)
create_character(connection, char_2)
create_character(connection, char_3)
create_character(connection, char_4)

# Insert some initial weapon data
weapon_0 = ('0', '10.5', 'Prateek''s Hammer', '20', 'Hammer', 'Super Rare', '5')
weapon_1 = ('1', '6', 'Sword of Strength', '20', 'Sword', 'Super Rare', '5')
weapon_2 = ('2', '7.5', 'Axe of Doom', '10', 'Axe', 'Rare', '2')
weapon_3 = ('3', '9.7', 'The Boomstick', '80', 'Gun', 'Ultra Rare', '9')
weapon_4 = ('4', '14.7', 'The Staff of Wisdom', '40', 'Staff', 'Epic', '7')

create_weapon(connection, weapon_0)
create_weapon(connection, weapon_1)
create_weapon(connection, weapon_2)
create_weapon(connection, weapon_3)
create_weapon(connection, weapon_4)

# Committing changes and closing the connection to the database file
connection.commit()
connection.close()
