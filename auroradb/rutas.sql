-- Estructura de la tabla
CREATE TABLE rutas (
  id int(5) AUTO_INCREMENT,
  ciudad_orig varchar(45) DEFAULT NULL,
  ciudad_dest varchar(45) DEFAULT NULL,
  estado_orig varchar(45) DEFAULT NULL,
  estado_dest varchar(45) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Datos Semilla
INSERT INTO rutas VALUES
  (1, 'CDMX', 'OAX', 'MEX', 'OAX'),
  (2, 'CDMX', 'QRT', 'MEX', 'QRT'),
  (3, 'QRT', 'MTR', 'QRT', 'NLN');
  
