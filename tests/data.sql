INSERT INTO user (username, password)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');
INSERT INTO zone (num_characters, num_creatures, zone_name, zone_level_range, difficulty)
VALUES ('300', '300', 'testZone', '1-20', 'Easy');
INSERT INTO equipped_weapon (zone_id, weapon_name, weapon_level, weapon_type, rarity)
VALUES ('1', 'testWeapon', '100', 'Hammer', 'Epic');
INSERT INTO character (e_wep_id, user_id, hours_played, character_name, character_level, character_kills)
VALUES ('2', '1', '10', 'testCharacter', '100', '200');
