CREATE TABLE user_auth_v2 (
    login   VARCHAR(50),
    mdp     VARCHAR(255) NOT NULL,
    id_auth VARCHAR(50) NOT NULL,
    role    VARCHAR(50),
    PRIMARY KEY (login),
    UNIQUE (id_auth)
);

INSERT INTO user_auth_v2 (login, mdp, id_auth, role)
VALUES ('johndoe', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', '1', 'user');