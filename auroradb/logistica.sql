-- Estructura de la tabla
CREATE TABLE logistica (
  id int(11) AUTO_INCREMENT,
  ciudad_orig varchar(45) DEFAULT NULL,
  ciudad_dest varchar(45) DEFAULT NULL,
  tiempo_min  float(5) DEFAULT NULL,
  costo_peso  float(5) DEFAULT NULL,
  capac_cubft float(8) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Datos Semilla
INSERT INTO logistica VALUES
  (1, 'CDMX', 'QRT', 36, 250, 30),
  (2, 'CDMX', 'OAX', 48, 600, 20),
  (3, 'QRT', 'MTR', 42, 800, 30);