CREATE TABLE users (
    login   VARCHAR(50),
    mdp     VARCHAR(255) NOT NULL,
    id_auth VARCHAR(50) NOT NULL,
    role    VARCHAR(50),
    PRIMARY KEY (login),
    UNIQUE (id_auth)
);

# Insert user admin/password
INSERT INTO users (login, mdp, id_auth, role)
VALUES ('admin', '$2b$12$.ry7msXUwOYCUUsblmEaCOvNDFAMuIUZluAI3dYd09BN9B/xWzwXS', '1', 'admin');