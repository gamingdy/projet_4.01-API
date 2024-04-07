CREATE TABLE users (
    login VARCHAR(50),
    mdp   VARCHAR(255) NOT NULL,
    PRIMARY KEY (login)
);

# Insert user admin/password
INSERT INTO users (login, mdp)
VALUES ('admin', '$2b$12$.ry7msXUwOYCUUsblmEaCOvNDFAMuIUZluAI3dYd09BN9B/xWzwXS');