-- Conectarse a la base de datos 'votaciones'
\connect votaciones

-- Crear la tabla 'Voting'
CREATE TABLE public.Voting (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    state VARCHAR(50),
    winners INTEGER,
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
    PRIMARY KEY (voting_id, user_email),
    FOREIGN KEY (voting_id) REFERENCES public.Voting(id)
);

-- Crear la tabla 'UserVote'
CREATE TABLE public.UserVote (
    voteToken UUID PRIMARY KEY,
    voteDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    votingId UUID NOT NULL,
    userId UUID NOT NULL,
    hasVoted BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (votingId) REFERENCES public.voting(id)
);

-- Asignar todos los privilegios en la base de datos 'votaciones' al rol 'example'
GRANT ALL PRIVILEGES ON DATABASE votaciones TO example;

-- Asignar todos los privilegios en todas las tablas actuales y futuras al rol 'example'
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO example;

INSERT INTO public.Voting (id, name, state, winners, voting_system, privacy, start_date, end_date, voting_creator)
VALUES 
('e29f0c6b-1d6b-4f08-9306-f42e5b34789f', 'Election 2024', 'published', 1, 'scoring', 'False', '2024-08-01 08:00:00', '2024-12-10 17:00:00', 'a45f9a2e-b0c3-4c1a-a0c9-63446d99e784'),
('d13f0765-5c0b-4fc8-9adf-0d3d7b4ec501', 'Best Movie of 2023', 'published', 3, 'scoring', 'True', '2024-08-01 08:00:00', '2023-12-31 23:59:00', 'b342f1da-2291-41b3-bf2a-c16c421e9a1b'),
('fc7be718-5db2-4b7b-b00d-3e7a6d7e8b16', 'Company Board Election', 'published', 5, 'schuzle', 'False', '2024-03-01 09:00:00', '2024-09-07 18:00:00', 'c24b4f95-d29b-42c7-82e9-0135a4e3b8b2');

INSERT INTO public.Options (option, voting_id)
VALUES 
('Candidate A', 'e29f0c6b-1d6b-4f08-9306-f42e5b34789f'),
('Candidate B', 'e29f0c6b-1d6b-4f08-9306-f42e5b34789f'),
('Movie 1', 'd13f0765-5c0b-4fc8-9adf-0d3d7b4ec501'),
('Movie 2', 'd13f0765-5c0b-4fc8-9adf-0d3d7b4ec501'),
('Movie 3', 'd13f0765-5c0b-4fc8-9adf-0d3d7b4ec501'),
('Nominee X', 'fc7be718-5db2-4b7b-b00d-3e7a6d7e8b16'),
('Nominee Y', 'fc7be718-5db2-4b7b-b00d-3e7a6d7e8b16'),
('Nominee Z', 'fc7be718-5db2-4b7b-b00d-3e7a6d7e8b16');

INSERT INTO public.AuthorizedUsers (voting_id, user_email)
VALUES 
('d13f0765-5c0b-4fc8-9adf-0d3d7b4ec501', 'i02essej@uco.es');

