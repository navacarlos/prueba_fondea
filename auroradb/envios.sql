-- Estructura de la tabla
CREATE TABLE envios (
  id int(11) AUTO_INCREMENT,
  cargo_code  varchar(45) DEFAULT NULL,
  ciudad_orig varchar(45) DEFAULT NULL,
  fecha_rec   DATE,
  ciudad_dest varchar(45) DEFAULT NULL,
  fecha_ent   DATE,
  peso_gram   float(5) DEFAULT NULL,
  paq_tipo    varchar(2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Datos Semilla
INSERT INTO envios VALUES
  (1, 'FIRMS-W183', 'CDMX', '2020-10-20', 'QRT', '2020-10-23', 1100, 'A2'),
  (2, 'FIRMS-U278', 'CDMX', '2020-10-22', 'OAX', '2020-10-23', 1100, 'A1'),
  (3, 'FIRMS-X771', 'QRT', '2020-10-22', 'MTR', '2020-10-24', 1100, 'B2'),
  (4, 'FIRMS-W187', 'CDMX', '2020-10-22', 'OAX', '2020-10-25', 1100, 'B1'),
  (5, 'FIRMS-X278', 'QRT', '2020-10-23', 'MTR', '2020-10-26', 1100, 'A2');