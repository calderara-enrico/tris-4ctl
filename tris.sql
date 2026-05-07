CREATE TABLE players (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(34) NOT NULL UNIQUE
);

CREATE TABLE games (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_x_id INT NOT NULL,
    player_o_id INT NOT NULL,
    winner_id INT NULL,
    date_played DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (player_x_id) REFERENCES players(id),
    FOREIGN KEY (player_o_id) REFERENCES players(id),
    FOREIGN KEY (winner_id) REFERENCES players(id),
    CHECK (player_x_id <> player_o_id)
);
