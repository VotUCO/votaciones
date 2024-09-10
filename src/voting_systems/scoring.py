def scoring_with_direct_points(votes, candidates):
    scores = {candidate: 0 for candidate in candidates}
    print(scores)
    validos = 0
    blancos = 0
    for vote in votes:
        if vote:
            validos = validos +1
            for candidate, points in vote.items():
                scores[candidate] += points
        else:
            blancos = blancos +1
            

    return sorted(scores.items(), key=lambda item: item[1], reverse=True), validos, blancos