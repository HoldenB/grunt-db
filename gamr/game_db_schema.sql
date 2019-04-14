DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS zone;
DROP TABLE IF EXISTS equipped_weapon;
DROP TABLE IF EXISTS character;

-- User table
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Zone table
CREATE TABLE zone (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    num_characters INTEGER NOT NULL,
    num_creatures INTEGER NOT NULL,
    zone_name TEXT UNIQUE NOT NULL,
    zone_level_range TEXT NOT NULL,
    difficulty TEXT NOT NULL
);

-- User "Equipped Weapon Slot" table
CREATE TABLE equipped_weapon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    zone_id INTEGER NOT NULL,
    weapon_name TEXT UNIQUE NOT NULL,
    weapon_level INTEGER NOT NULL,
    weapon_type TEXT NOT NULL,
    rarity TEXT NOT NULL,
    FOREIGN KEY (zone_id) REFERENCES zone (id)
);

-- Character table
CREATE TABLE character (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    e_wep_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    hours_played REAL NOT NULL,
    character_name TEXT UNIQUE NOT NULL,
    character_level INTEGER NOT NULL,
    character_kills INTEGER NOT NULL,
    FOREIGN KEY (e_wep_id) REFERENCES equipped_weapon (id),
    FOREIGN KEY (user_id) REFERENCES user (id)
);

------------------------------------------------------------------------------------------
-- ZONES
-- Premade zone 1
INSERT INTO zone (num_characters, num_creatures, zone_name, zone_level_range, difficulty)
VALUES ('300', '300', 'Elwynn Forest', '1-20', 'Easy');

-- Premade zone 2
INSERT INTO zone (num_characters, num_creatures, zone_name, zone_level_range, difficulty)
VALUES ('100', '100', 'Prateek''s Valley', '90-100', 'Very Hard');

-- Premade zone 3
INSERT INTO zone (num_characters, num_creatures, zone_name, zone_level_range, difficulty)
VALUES ('40', '250', 'The Green Hills', '50-60', 'Moderately Hard');

------------------------------------------------------------------------------------------
-- WEAPONS
-- Premade wep 1
INSERT INTO equipped_weapon (zone_id, weapon_name, weapon_level, weapon_type, rarity)
VALUES ('1', 'Crude sword', '1', 'One-Hand Sword', 'Common');

-- Premade wep 2
INSERT INTO equipped_weapon (zone_id, weapon_name, weapon_level, weapon_type, rarity)
VALUES ('2', 'Prateek''s Mighty Hammer', '100', 'Hammer', 'Epic');

-- Premade wep 3
INSERT INTO equipped_weapon (zone_id, weapon_name, weapon_level, weapon_type, rarity)
VALUES ('3', ' Dank-A-Lank MayMays', '80', 'Sword', 'Legendary');

-- Premade wep 4
INSERT INTO equipped_weapon (zone_id, weapon_name, weapon_level, weapon_type, rarity)
VALUES ('3', 'Finger Gun', '20', 'Gun', 'Common');

------------------------------------------------------------------------------------------
-- Demo user 1
INSERT INTO user (username, password)
VALUES ('Jack', 'Jack');
-- Demo character 1
INSERT INTO character (e_wep_id, user_id, hours_played, character_name, character_level, character_kills)
VALUES ('2', '1', '10', 'BWWorBBW', '100', '200');

-- Demo user 2
INSERT INTO user (username, password)
VALUES ('SBAV', 'SBAV');
-- Demo character 2
INSERT INTO character (e_wep_id, user_id, hours_played, character_name, character_level, character_kills)
VALUES ('3', '2', '60', 'AKTheMemeLord', '80', '1000');

-- Demo user 3
INSERT INTO user (username, password)
VALUES ('T8', 'T8');
-- Demo character 3
INSERT INTO character (e_wep_id, user_id, hours_played, character_name, character_level, character_kills)
VALUES ('4', '3', '90', 'BarryMcKokinner', '90', '850');
