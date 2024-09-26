CREATE TABLE matches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    league VARCHAR(255) NOT NULL,
    hour_match VARCHAR(255) NOT NULL,
    date_match VARCHAR(255) NOT NULL,
    match_datetime DATETIME NOT NULL,
    team_home VARCHAR(50) NOT NULL,
    team_visitor VARCHAR(50) NOT NULL,
    scoreboard VARCHAR(20) NOT NULL,
    hora INT NOT NULL,
    minuto INT NOT NULL
);