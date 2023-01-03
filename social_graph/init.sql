CREATE DATABASE social_graph;
USE social_graph;

CREATE TABLE relationship (
  id INT NOT NULL AUTO_INCREMENT,
  destination_id INT NOT NULL,
  source_id INT NOT NULL,
  PRIMARY KEY (id),
  INDEX (destination_id)
);

