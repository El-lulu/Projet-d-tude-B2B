CREATE TABLE parcelles (
    id INT PRIMARY KEY,
    nom VARCHAR(255),
    localisation VARCHAR(255),
    surface_ha FLOAT
);

CREATE TABLE cultures (
    id INT PRIMARY KEY,
    type VARCHAR(255),
    date_semis DATE,
    parcelle_id INT,
    FOREIGN KEY (parcelle_id) REFERENCES parcelles(id)
);

CREATE TABLE meteo (
    date DATE PRIMARY KEY,
    temperature INT,
    humidite INT,
    pluie_mm INT
);

CREATE TABLE observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    etat VARCHAR(255),
    parcelle_id INT,
    commentaire TEXT,
    FOREIGN KEY (parcelle_id) REFERENCES parcelles(id)
);

CREATE TABLE alertes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    type VARCHAR(255),
    parcelle_id INT,
    niveau INT,
    FOREIGN KEY (parcelle_id) REFERENCES parcelles(id)
);

INSERT INTO parcelles (id, nom, localisation, surface_ha) VALUES 
(1, 'Parcelle 1', 'Zone A', 2.45),
(2, 'Parcelle 2', 'Zone B', 4.49),
(3, 'Parcelle 3', 'Zone C', 2.15),
(4, 'Parcelle 4', 'Zone D', 2.49),
(5, 'Parcelle 5', 'Zone E', 3.2),
(6, 'Parcelle 6', 'Zone A', 4.06),
(7, 'Parcelle 7', 'Zone B', 2.45),
(8, 'Parcelle 8', 'Zone C', 3.88),
(9, 'Parcelle 9', 'Zone D', 4.07),
(10, 'Parcelle 10', 'Zone E', 2.37);

INSERT INTO cultures (id, type, date_semis, parcelle_id) VALUES 
(1, 'Orge', '2026-03-15', 1),
(2, 'Tournesol', '2026-03-20', 2),
(3, 'Blé', '2026-03-19', 3),
(4, 'Maïs', '2026-03-21', 4),
(5, 'Blé', '2026-03-16', 5),
(6, 'Tournesol', '2026-03-03', 6),
(7, 'Orge', '2026-03-19', 7),
(8, 'Tournesol', '2026-03-11', 8),
(9, 'Colza', '2026-03-12', 9),
(10, 'Colza', '2026-03-17', 10);

INSERT INTO meteo (date, temperature, humidite, pluie_mm) VALUES 
('2026-03-01', 17, 47, 0), ('2026-03-02', 14, 74, 5), ('2026-03-03', 29, 39, 30), ('2026-03-04', 17, 38, 5),
('2026-03-05', 18, 39, 10), ('2026-03-06', 9, 94, 0), ('2026-03-07', 16, 44, 20), ('2026-03-08', 17, 51, 0),
('2026-03-09', 22, 94, 0), ('2026-03-10', 20, 91, 30), ('2026-03-11', 17, 60, 0), ('2026-03-12', 20, 95, 5),
('2026-03-13', 12, 30, 10), ('2026-03-14', 14, 76, 5), ('2026-03-15', 9, 63, 0), ('2026-03-16', 25, 60, 20),
('2026-03-17', 9, 33, 0), ('2026-03-18', 17, 69, 30), ('2026-03-19', 16, 86, 30), ('2026-03-20', 25, 44, 0),
('2026-03-21', 15, 74, 10), ('2026-03-22', 17, 83, 10), ('2026-03-23', 10, 56, 0), ('2026-03-24', 22, 72, 0),
('2026-03-25', 6, 70, 0), ('2026-03-26', 21, 49, 30), ('2026-03-27', 25, 37, 5), ('2026-03-28', 7, 41, 5),
('2026-03-29', 22, 59, 10), ('2026-03-30', 22, 90, 20), ('2026-03-31', 27, 69, 0), ('2026-04-01', 7, 38, 0),
('2026-04-02', 6, 77, 0), ('2026-04-03', 23, 35, 10), ('2026-04-04', 20, 88, 5), ('2026-04-05', 17, 45, 30),
('2026-04-06', 20, 80, 0), ('2026-04-07', 21, 42, 30), ('2026-04-08', 18, 51, 5), ('2026-04-09', 17, 85, 20),
('2026-04-10', 20, 72, 10), ('2026-04-11', 24, 47, 10), ('2026-04-12', 20, 93, 0), ('2026-04-13', 17, 69, 30),
('2026-04-14', 15, 73, 20), ('2026-04-15', 10, 71, 0), ('2026-04-16', 13, 71, 5), ('2026-04-17', 30, 44, 0),
('2026-04-18', 17, 81, 20), ('2026-04-19', 17, 83, 10), ('2026-04-20', 21, 93, 5), ('2026-04-21', 13, 85, 10),
('2026-04-22', 5, 50, 0), ('2026-04-23', 6, 89, 5), ('2026-04-24', 13, 92, 20), ('2026-04-25', 14, 91, 30),
('2026-04-26', 19, 42, 0), ('2026-04-27', 15, 65, 0), ('2026-04-28', 27, 89, 0), ('2026-04-29', 23, 56, 20);

INSERT INTO observations (date, etat, parcelle_id, commentaire) VALUES 
('2026-03-02', 'OK', 2, 'Sol sec'), ('2026-03-15', 'Risque maladie', 3, 'Sol sec'), ('2026-04-17', 'OK', 8, 'Sol sec'),
('2026-03-02', 'Stress hydrique', 8, 'Sol sec'), ('2026-03-30', 'Stress hydrique', 9, 'Sol sec'), ('2026-03-11', 'OK', 3, 'Humidité'),
('2026-03-09', 'Maladie détectée', 2, 'Humidité'), ('2026-04-28', 'OK', 10, 'Humidité'), ('2026-03-08', 'Stress hydrique', 9, 'Feuilles jaunies'),
('2026-03-20', 'Stress hydrique', 8, 'Humidité'), ('2026-04-19', 'Risque maladie', 4, 'Sol sec'), ('2026-03-02', 'Stress hydrique', 8, 'Feuilles jaunies'),
('2026-03-02', 'Maladie détectée', 5, 'Feuilles jaunies'), ('2026-03-01', 'OK', 7, 'Humidité'), ('2026-03-17', 'Stress hydrique', 2, 'Humidité'),
('2026-04-06', 'Maladie détectée', 7, 'Feuilles jaunies'), ('2026-03-23', 'Risque maladie', 9, 'Sol sec'), ('2026-03-28', 'OK', 4, 'Humidité'),
('2026-03-05', 'Stress hydrique', 5, 'Rien à signaler'), ('2026-03-16', 'Risque maladie', 8, 'Rien à signaler'), ('2026-03-22', 'OK', 2, 'Humidité'),
('2026-04-20', 'OK', 3, 'Feuilles jaunies'), ('2026-03-05', 'Maladie détectée', 10, 'Rien à signaler'), ('2026-04-13', 'OK', 10, 'Rien à signaler'),
('2026-04-21', 'OK', 7, 'Sol sec'), ('2026-04-18', 'Maladie détectée', 10, 'Humidité'), ('2026-03-04', 'OK', 10, 'Rien à signaler'),
('2026-04-18', 'OK', 7, 'Feuilles jaunies'), ('2026-03-09', 'Risque maladie', 6, 'Sol sec'), ('2026-04-19', 'Maladie détectée', 9, 'Humidité'),
('2026-04-19', 'Stress hydrique', 7, 'Feuilles jaunies'), ('2026-04-27', 'Maladie détectée', 1, 'Humidité'), ('2026-03-31', 'Risque maladie', 4, 'Sol sec'),
('2026-04-07', 'OK', 7, 'Sol sec'), ('2026-03-22', 'Stress hydrique', 8, 'Feuilles jaunies'), ('2026-03-29', 'Risque maladie', 7, 'Rien à signaler'),
('2026-04-07', 'Maladie détectée', 3, 'Feuilles jaunies'), ('2026-04-06', 'Risque maladie', 3, 'Feuilles jaunies'), ('2026-03-01', 'Maladie détectée', 8, 'Feuilles jaunies'),
('2026-03-07', 'Maladie détectée', 10, 'Feuilles jaunies'), ('2026-03-14', 'Risque maladie', 1, 'Humidité'), ('2026-04-15', 'Stress hydrique', 6, 'Humidité'),
('2026-04-23', 'OK', 10, 'Humidité'), ('2026-04-17', 'Risque maladie', 3, 'Feuilles jaunies'), ('2026-03-07', 'Risque maladie', 8, 'Humidité'),
('2026-03-16', 'Risque maladie', 8, 'Feuilles jaunies'), ('2026-03-19', 'Stress hydrique', 6, 'Humidité'), ('2026-03-14', 'Maladie détectée', 4, 'Rien à signaler'),
('2026-04-28', 'Stress hydrique', 5, 'Humidité'), ('2026-03-21', 'Stress hydrique', 3, 'Feuilles jaunies'), ('2026-03-05', 'Risque maladie', 2, 'Humidité'),
('2026-04-17', 'Risque maladie', 10, 'Humidité'), ('2026-03-22', 'Risque maladie', 7, 'Rien à signaler'), ('2026-04-27', 'Stress hydrique', 4, 'Rien à signaler'),
('2026-04-14', 'OK', 8, 'Humidité'), ('2026-04-22', 'Stress hydrique', 7, 'Rien à signaler'), ('2026-04-03', 'Stress hydrique', 3, 'Sol sec'),
('2026-03-12', 'Stress hydrique', 7, 'Humidité'), ('2026-03-26', 'Risque maladie', 7, 'Feuilles jaunies'), ('2026-03-29', 'OK', 8, 'Feuilles jaunies'),
('2026-04-13', 'OK', 9, 'Feuilles jaunies'), ('2026-04-19', 'Maladie détectée', 2, 'Rien à signaler'), ('2026-04-27', 'Stress hydrique', 4, 'Rien à signaler'),
('2026-04-13', 'Risque maladie', 6, 'Feuilles jaunies'), ('2026-03-29', 'OK', 2, 'Sol sec'), ('2026-04-23', 'Risque maladie', 4, 'Feuilles jaunies'),
('2026-03-30', 'Stress hydrique', 6, 'Sol sec'), ('2026-04-17', 'Risque maladie', 9, 'Humidité'), ('2026-03-16', 'OK', 1, 'Feuilles jaunies'),
('2026-03-20', 'Risque maladie', 9, 'Humidité'), ('2026-04-12', 'OK', 6, 'Humidité'), ('2026-03-06', 'Maladie détectée', 7, 'Rien à signaler'),
('2026-03-13', 'OK', 8, 'Humidité'), ('2026-04-24', 'Maladie détectée', 10, 'Sol sec'), ('2026-03-02', 'Stress hydrique', 10, 'Feuilles jaunies'),
('2026-04-12', 'Stress hydrique', 2, 'Rien à signaler'), ('2026-04-28', 'Maladie détectée', 3, 'Sol sec'), ('2026-04-08', 'Stress hydrique', 9, 'Humidité'),
('2026-03-04', 'Stress hydrique', 10, 'Humidité'), ('2026-04-28', 'OK', 1, 'Sol sec'), ('2026-03-27', 'Maladie détectée', 9, 'Rien à signaler'),
('2026-04-24', 'Maladie détectée', 3, 'Rien à signaler'), ('2026-03-07', 'Risque maladie', 8, 'Feuilles jaunies'), ('2026-04-13', 'Maladie détectée', 3, 'Sol sec'),
('2026-03-09', 'Maladie détectée', 10, 'Rien à signaler'), ('2026-03-31', 'Risque maladie', 9, 'Sol sec'), ('2026-03-28', 'Maladie détectée', 3, 'Feuilles jaunies'),
('2026-03-28', 'Maladie détectée', 8, 'Feuilles jaunies'), ('2026-03-02', 'Maladie détectée', 6, 'Rien à signaler'), ('2026-04-11', 'Risque maladie', 4, 'Rien à signaler'),
('2026-03-03', 'Risque maladie', 5, 'Sol sec'), ('2026-03-05', 'OK', 6, 'Rien à signaler'), ('2026-03-23', 'OK', 3, 'Feuilles jaunies'),
('2026-03-01', 'Stress hydrique', 3, 'Sol sec'), ('2026-04-27', 'OK', 3, 'Rien à signaler'), ('2026-04-13', 'Maladie détectée', 5, 'Sol sec'),
('2026-03-17', 'OK', 2, 'Humidité'), ('2026-04-01', 'Maladie détectée', 9, 'Feuilles jaunies'), ('2026-03-15', 'Risque maladie', 7, 'Rien à signaler'),
('2026-03-06', 'Maladie détectée', 3, 'Rien à signaler');

INSERT INTO alertes (date, type, parcelle_id, niveau) VALUES 
('2026-04-11', 'Stress hydrique', 3, 2), ('2026-03-04', 'Stress hydrique', 8, 1), ('2026-03-29', 'Stress hydrique', 4, 1),
('2026-04-07', 'Stress hydrique', 10, 2), ('2026-03-05', 'Risque maladie', 4, 2), ('2026-04-12', 'Stress hydrique', 1, 2),
('2026-03-23', 'Stress hydrique', 2, 3), ('2026-03-29', 'Stress hydrique', 1, 2), ('2026-03-25', 'Risque maladie', 4, 1),
('2026-04-14', 'Stress hydrique', 4, 3), ('2026-03-10', 'Risque maladie', 5, 2), ('2026-03-05', 'Risque maladie', 4, 2),
('2026-04-10', 'Risque maladie', 7, 1), ('2026-04-19', 'Stress hydrique', 9, 2), ('2026-04-02', 'Stress hydrique', 9, 2),
('2026-04-02', 'Stress hydrique', 9, 3), ('2026-04-28', 'Stress hydrique', 7, 2), ('2026-04-12', 'Stress hydrique', 10, 2),
('2026-03-14', 'Risque maladie', 5, 2), ('2026-03-21', 'Stress hydrique', 9, 3), ('2026-03-25', 'Risque maladie', 3, 1),
('2026-04-14', 'Risque maladie', 7, 3), ('2026-04-13', 'Risque maladie', 1, 1), ('2026-03-10', 'Risque maladie', 2, 2),
('2026-03-03', 'Risque maladie', 10, 1), ('2026-04-14', 'Stress hydrique', 1, 1), ('2026-03-27', 'Risque maladie', 7, 1),
('2026-03-12', 'Risque maladie', 3, 3), ('2026-04-17', 'Stress hydrique', 3, 2), ('2026-04-08', 'Risque maladie', 10, 1),
('2026-04-23', 'Stress hydrique', 8, 2), ('2026-04-15', 'Stress hydrique', 6, 2), ('2026-04-02', 'Stress hydrique', 8, 1),
('2026-03-14', 'Risque maladie', 3, 1), ('2026-04-12', 'Risque maladie', 2, 2), ('2026-04-18', 'Stress hydrique', 2, 1),
('2026-03-20', 'Risque maladie', 1, 2), ('2026-04-19', 'Stress hydrique', 6, 1), ('2026-04-09', 'Risque maladie', 7, 3),
('2026-04-19', 'Risque maladie', 7, 1), ('2026-04-21', 'Risque maladie', 3, 3), ('2026-03-16', 'Risque maladie', 3, 3),
('2026-04-07', 'Risque maladie', 7, 2), ('2026-03-08', 'Risque maladie', 4, 2), ('2026-04-21', 'Risque maladie', 9, 3),
('2026-03-23', 'Stress hydrique', 9, 3), ('2026-04-09', 'Risque maladie', 7, 2), ('2026-03-16', 'Stress hydrique', 3, 3),
('2026-03-22', 'Risque maladie', 5, 2), ('2026-03-14', 'Risque maladie', 10, 2);