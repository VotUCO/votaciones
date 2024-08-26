-- Conectarse a la base de datos 'votaciones'
\connect votaciones

-- Crear la tabla 'Voting'
CREATE TABLE public.Voting (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    state VARCHAR(50),
    wineers INTEGER,
    voting_system VARCHAR(50),
    privacy VARCHAR(50),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    voting_creator UUID NOT NULL
);

-- Crear la tabla 'Options'
CREATE TABLE public.Options (
    option VARCHAR(255) NOT NULL,
    voting_id UUID NOT NULL,
    PRIMARY KEY(option, voting_id),
    FOREIGN KEY (voting_id) REFERENCES public.Voting(id)
);

-- Crear la tabla 'AuthorizedUsers'
CREATE TABLE public.AuthorizedUsers (
    voting_id UUID NOT NULL,
    user_email VARCHAR(50) NOT NULL,
    PRIMARY KEY (voting_id, user_id),
    FOREIGN KEY (voting_id) REFERENCES public.Voting(id)
);

-- Crear la tabla 'UserVote'
CREATE TABLE public.UserVote (
    voteToken UUID PRIMARY KEY,
    voteDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    votationId UUID NOT NULL,
    userId UUID NOT NULL,
    hasVoted BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (votationId) REFERENCES public.Voting(id)
);

-- Asignar todos los privilegios en la base de datos 'votaciones' al rol 'example'
GRANT ALL PRIVILEGES ON DATABASE votaciones TO example;

-- Asignar todos los privilegios en todas las tablas actuales y futuras al rol 'example'
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO example;