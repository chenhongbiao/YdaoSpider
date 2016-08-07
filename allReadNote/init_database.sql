CREATE DATABASE readnote;
USE readnote;

CREATE TABLE sharers (
				id  INT NOT NULL AUTO_INCREMENT,
				name VARCHAR(255) NOT NULL,
                photo VARCHAR(255) NOT NULL,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id));

CREATE TABLE notes (
				id  INT NOT NULL AUTO_INCREMENT,
				title VARCHAR(1023) NOT NULL,
                content MEDIUMTEXT NOT NULL,
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

CREATE TABLE noteurl (
				id  INT NOT NULL AUTO_INCREMENT,
				url VARCHAR(255) NOT NULL,
				PRIMARY KEY (id)
				);



# For each database:
ALTER DATABASE readnote CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;
# For each table:
ALTER TABLE notes CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
# For each column:
ALTER TABLE notes CHANGE content content MEDIUMTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

#Since utf8mb4 is fully backwards compatible with utf8, no mojibake or other forms of data loss should occur. 