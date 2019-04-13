DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS zone;
DROP TABLE IF EXISTS equipped_weapon;
DROP TABLE IF EXISTS character;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE zone (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    num_characters INTEGER NOT NULL,
    num_creatures INTEGER NOT NULL,
    zone_name TEXT UNIQUE NOT NULL,
    zone_level_range TEXT NOT NULL,
    difficulty TEXT NOT NULL
);

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

INSERT INTO user (username, password)
VALUES ('Prateek', 'bbw');

INSERT INTO character (e_wep_id, user_id, hours_played, character_name, character_level, character_kills)
VALUES ('1', '1', '10', 'bbwLover', '100', '200');

INSERT INTO equipped_weapon (zone_id, weapon_name, weapon_level, weapon_type, rarity)
VALUES ('1', 'Prateek''s Mighty Hammer', '100', 'Hammer', 'Epic');

INSERT INTO zone (num_characters, num_creatures, zone_name, zone_level_range, difficulty)
VALUES ('100', '100', 'Prateek''s Valley', '90-100', 'Very Hard');
