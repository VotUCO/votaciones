def mayority_with_direct_points(votes, candidates):
    scores = {candidate: 0 for candidate in candidates}
    blancos = 0
    validos = 0
    for vote in votes:
        if vote:
            for candidate in vote:
                scores[candidate] += 1
                validos = validos +1
        else:
            blancos = blancos + 1

    return sorted(scores.items(), key=lambda item: item[1], reverse=True), validos, blancos