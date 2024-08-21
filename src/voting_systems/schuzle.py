import itertools

def schulze_method(votes, candidates):
    # Paso 1: Contar preferencias directas
    preferences = { (i, j): 0 for i in candidates for j in candidates if i != j }
    for vote in votes:
        for i, j in itertools.combinations(vote, 2):
            if vote.index(i) < vote.index(j):
                preferences[(i, j)] += 1
            else:
                preferences[(j, i)] += 1

    # Paso 2: Determinar la fuerza de la ruta más fuerte
    strength = { (i, j): 0 for i in candidates for j in candidates if i != j }
    for i, j in preferences:
        if preferences[(i, j)] > preferences[(j, i)]:
            strength[(i, j)] = preferences[(i, j)]
    
    for i, j, k in itertools.permutations(candidates, 3):
        if strength[(i, j)] > 0 and strength[(j, k)] > 0:
            strength[(i, k)] = max(strength[(i, k)], min(strength[(i, j)], strength[(j, k)]))

    # Paso 3: Determinar el orden de los candidatos
    ranking = { candidate: 0 for candidate in candidates }
    for i, j in strength:
        if strength[(i, j)] > strength[(j, i)]:
            ranking[i] += 1

    return sorted(ranking.items(), key=lambda item: item[1], reverse=True)