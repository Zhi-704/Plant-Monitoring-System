-- remove any existing tables
DROP TABLE IF EXISTS delta.reading;
DROP TABLE IF EXISTS delta.plant;
DROP TABLE IF EXISTS delta.location;
DROP TABLE IF EXISTS delta.botanist;
DROP TABLE IF EXISTS delta.town;
DROP TABLE IF EXISTS delta.timezone;
DROP TABLE IF EXISTS delta.country;

-- create country table
CREATE TABLE delta.country(
    country_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    country_code CHAR(2) NOT NULL UNIQUE
);

-- create timezone table
CREATE TABLE delta.timezone(
    timezone_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    tz_identifier VARCHAR(40) NOT NULL UNIQUE
);

-- create town table
CREATE TABLE delta.town(
    town_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    town_name VARCHAR(60) NOT NULL,
    country_id SMALLINT NOT NULL,
    timezone_id SMALLINT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES delta.country(country_id),
    FOREIGN KEY (timezone_id) REFERENCES delta.timezone(timezone_id)
);

-- create botanist table
CREATE TABLE delta.botanist(
    botanist_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(40) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(60) NOT NULL
);

-- create location table
CREATE TABLE delta.location(
    location_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    town_id SMALLINT NOT NULL,
    latitude DECIMAL(8, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,
    FOREIGN KEY (town_id) REFERENCES delta.town(town_id)
);

-- create plant table
CREATE TABLE delta.plant(
    plant_id SMALLINT NOT NULL PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    scientific_name VARCHAR(60),
    location_id SMALLINT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES delta.location(location_id)
);

-- create reading table
CREATE TABLE delta.reading(
    reading_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    soil_moisture FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    timestamp DATETIME2(0) NOT NULL,
    plant_id SMALLINT NOT NULL,
    botanist_id SMALLINT NOT NULL,
    last_watered DATETIME2(0) NOT NULL,
    FOREIGN KEY (plant_id) REFERENCES delta.plant(plant_id),
    FOREIGN KEY (botanist_id) REFERENCES delta.botanist(botanist_id)
);

-- seed data into country table
INSERT INTO delta.country(country_code)
VALUES
    ('BR'),
    ('US'),
    ('NG'),
    ('SV'),
    ('IN'),
    ('CA'),
    ('CI'),
    ('DE'),
    ('HR'),
    ('TN'),
    ('BW'),
    ('ES'),
    ('JP'),
    ('SD'),
    ('DZ'),
    ('UA'),
    ('LY'),
    ('TZ'),
    ('FR'),
    ('BG'),
    ('MX'),
    ('IT'),
    ('MW'),
    ('CL'),
    ('PH'),
    ('CN'),
    ('ID');

-- seed data into timezone table
INSERT INTO delta.timezone(tz_identifier)
VALUES
    ('Asia/Manila'),
    ('Africa/Gaborone'),
    ('Asia/Jakarta'),
    ('Europe/Madrid'),
    ('Africa/Dar_es_Salaam'),
    ('Europe/Rome'),
    ('Africa/Tunis'),
    ('America/El_Salvador'),
    ('America/New_York'),
    ('Africa/Algiers'),
    ('Europe/Berlin'),
    ('America/Chicago'),
    ('Europe/Zagreb'),
    ('Asia/Tokyo'),
    ('Asia/Kolkata'),
    ('Europe/Paris'),
    ('Africa/Blantyre'),
    ('Europe/Sofia'),
    ('Africa/Khartoum'),
    ('Europe/Kiev'),
    ('America/Toronto'),
    ('America/Los_Angeles'),
    ('Africa/Lagos'),
    ('Asia/Shanghai'),
    ('America/Santiago'),
    ('America/Mexico_City'),
    ('Pacific/Honolulu'),
    ('America/Sao_Paulo'),
    ('Africa/Abidjan'),
    ('Africa/Tripoli');

-- seed data into town table
INSERT INTO delta.town(town_name, country_id, timezone_id)
VALUES
    ('Friedberg', 8, 11),
    ('Carlos Barbosa', 1, 28),
    ('Hlukhiv', 16, 20),
    ('Ilopango', 4, 8),
    ('Bonoua', 7, 29),
    ('Ar Ruseris', 14, 19),
    ('Bachhraon', 5, 15),
    ('Charlottenburg-Nord', 8, 11),
    ('Valence', 19, 16),
    ('Calauan', 25, 1),
    ('Ueno-ebisumachi', 13, 14),
    ('Gainesville', 2, 9),
    ('Pujali', 5, 15),
    ('South Whittier', 2, 22),
    ('Jashpurnagar', 5, 15),
    ('Split', 9, 13),
    ('Malaut', 5, 15),
    ('Ajdabiya', 17, 30),
    ('Longview', 2, 12),
    ('Catania', 22, 6),
    ('El Achir', 15, 10),
    ('Magomeni', 18, 5),
    ('Motomachi', 13, 14),
    ('Smolyan', 20, 18),
    ('Dublin', 2, 9),
    ('Tonota', 11, 2),
    ('Licheng', 26, 24),
    ('Acayucan', 21, 26),
    ('Zacoalco de Torres', 21, 26),
    ('Brunswick', 2, 9),
    ('Weimar', 8, 11),
    ('Reus', 12, 4),
    ('Gifhorn', 8, 11),
    ('Salima', 23, 17),
    ('La Ligua', 24, 25),
    ('Markham', 6, 21),
    ('Resplendor', 1, 28),
    ('Wangon', 27, 3),
    ('Kahului', 2, 27),
    ('Siliana', 10, 7),
    ('Fujioka', 13, 14),
    ('Efon-Alaaye', 3, 23),
    ('Bensheim', 8, 11),
    ('Yonkers', 2, 9),
    ('Oschatz', 8, 11);

-- seed data into location table
INSERT INTO delta.location(town_id, latitude, longitude)
VALUES
    (1, 48.35693, 10.98461),
    (2, -29.2975, -51.50361),
    (3, 51.67822, 33.9162),
    (4, 13.70167, -89.10944),
    (5, 5.27247, -3.59625),
    (6, 11.8659, 34.3869),
    (7, 28.92694, 78.23456),
    (8, 52.53048, 13.29371),
    (9, 44.92801, 4.8951),
    (10, 14.14989, 121.3152),
    (11, 34.75856, 136.13108),
    (12, 29.65163, -82.32483),
    (13, 22.4711, 88.1453),
    (14, 33.95015, -118.03917),
    (15, 22.88783, 84.13864),
    (16, 43.50891, 16.43915),
    (17, 30.21121, 74.4818),
    (18, 30.75545, 20.22625),
    (19, 32.5007, -94.74049),
    (20, 37.49223, 15.07041),
    (21, 36.06386, 4.62744),
    (22, -6.8, 39.25),
    (23, 43.82634, 144.09638),
    (24, 41.57439, 24.71204),
    (25, 32.54044, -82.90375),
    (26, -21.44236, 27.46153),
    (27, 23.29549, 113.82465),
    (28, 17.94979, -94.91386),
    (29, 20.22816, -103.5687),
    (30, 43.91452, -69.96533),
    (31, 50.9803, 11.32903),
    (32, 41.15612, 1.10687),
    (33, 52.47774, 10.5511),
    (34, -13.7804, 34.4587),
    (35, -32.45242, -71.23106),
    (36, 43.86682, -79.2663),
    (37, -19.32556, -41.25528),
    (38, -7.51611, 109.05389),
    (39, 20.88953, -156.47432),
    (40, 36.08497, 9.37082),
    (41, 36.24624, 139.07204),
    (42, 7.65649, 4.92235),
    (43, 49.68369, 8.61839),
    (44, 40.93121, -73.89875),
    (45, 51.30001, 13.10984);

-- seed data into plant table
INSERT INTO delta.plant(plant_id, name, scientific_name, location_id)
VALUES
    (0, 'Epipremnum Aureum', 'Epipremnum aureum', 37),
    (1, 'Venus flytrap', NULL, 14),
    (2, 'Corpse flower', NULL, 42),
    (3, 'Rafflesia arnoldii', NULL, 37),
    (4, 'Black bat flower', NULL, 4),
    (5, 'Pitcher plant', 'Sarracenia catesbaei', 15),
    (6, 'Wollemi pine', 'Wollemia nobilis', 36),
    (8, 'Bird of paradise', 'Heliconia schiedeana "Fire and Ice"', 5),
    (9, 'Cactus', 'Pereskia grandifolia', 31),
    (10, 'Dragon tree', NULL, 16),
    (11, 'Asclepias Curassavica', 'Asclepias curassavica', 39),
    (12, 'Brugmansia X Candida', NULL, 19),
    (13, 'Canna ‘Striata’', NULL, 43),
    (14, 'Colocasia Esculenta', 'Colocasia esculenta', 12),
    (15, 'Cuphea ‘David Verity’', NULL, 40),
    (16, 'Euphorbia Cotinifolia', 'Euphorbia cotinifolia', 44),
    (17, 'Ipomoea Batatas', 'Ipomoea batatas', 38),
    (18, 'Manihot Esculenta ‘Variegata’', NULL, 45),
    (19, 'Musa Basjoo', 'Musa basjoo', 26),
    (20, 'Salvia Splendens', 'Salvia splendens', 32),
    (21, 'Anthurium', 'Anthurium andraeanum', 2),
    (22, 'Bird of Paradise', 'Heliconia schiedeana "Fire and Ice"', 1),
    (23, 'Cordyline Fruticosa', 'Cordyline fruticosa', 8),
    (24, 'Ficus', 'Ficus carica', 23),
    (25, 'Palm Trees', NULL, 6),
    (26, 'Dieffenbachia Seguine', 'Dieffenbachia seguine', 21),
    (27, 'Spathiphyllum', 'Spathiphyllum (group)', 3),
    (28, 'Croton', 'Codiaeum variegatum', 30),
    (29, 'Aloe Vera', 'Aloe vera', 11),
    (30, 'Ficus Elastica', 'Ficus elastica', 18),
    (31, 'Sansevieria Trifasciata', 'Sansevieria trifasciata', 27),
    (32, 'Philodendron Hederaceum', 'Philodendron hederaceum', 33),
    (33, 'Schefflera Arboricola', 'Schefflera arboricola', 7),
    (34, 'Aglaonema Commutatum', 'Aglaonema commutatum', 32),
    (35, 'Monstera Deliciosa', 'Monstera deliciosa', 35),
    (36, 'Tacca Integrifolia', 'Tacca integrifolia', 25),
    (37, 'Psychopsis Papilio', NULL, 17),
    (38, 'Saintpaulia Ionantha', 'Saintpaulia ionantha', 22),
    (39, 'Gaillardia', 'Gaillardia aestivalis', 41),
    (40, 'Amaryllis', 'Hippeastrum (group)', 9),
    (41, 'Caladium Bicolor', 'Caladium bicolor', 13),
    (42, 'Chlorophytum Comosum', 'Chlorophytum comosum "Vittatum"', 24),
    (44, 'Araucaria Heterophylla', 'Araucaria heterophylla', 29),
    (45, 'Begonia', 'Begonia "Art Hodes"', 14),
    (46, 'Medinilla Magnifica', 'Medinilla magnifica', 34),
    (47, 'Calliandra Haematocephala', 'Calliandra haematocephala', 20),
    (48, 'Zamioculcas Zamiifolia', 'Zamioculcas zamiifolia', 10),
    (49, 'Crassula Ovata', 'Crassula ovata', 28),
    (50, 'Epipremnum Aureum', 'Epipremnum aureum', 37);

-- seed data into botanist table
INSERT INTO delta.botanist(first_name, last_name, email, phone)
VALUES
    ('Carl', 'Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'),
    ('Gertrude', 'Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'),
    ('Eliza', 'Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948');
