CREATE DATABASE readnote;

CREATE TABLE sharers (
				id  INT NOT NULL AUTO_INCREMENT,
				name VARCHAR(255) NOT NULL,
                photo VARCHAR(255) NOT NULL,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id));

CREATE TABLE notes (
				id  INT NOT NULL AUTO_INCREMENT,
				title VARCHAR(255) NOT NULL,
                content VARCHAR(10000) NOT NULL,
                readtimes INT NOT NULL DEFAULT 1,
                praises INT NOT NULL DEFAULT 0,
                updatetime VARCHAR(15) NOT NULL,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id));

CREATE TABLE links (
				id  INT NOT NULL AUTO_INCREMENT,
				shr_Id INT NOT NULL,
                note_Id INT NOT NULL,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id),
                FOREIGN KEY (shr_Id) REFERENCES sharers(id),
                FOREIGN KEY (note_Id) REFERENCES notes(id)
);