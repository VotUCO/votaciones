def scoring_with_direct_points(votes, candidates):
    scores = {candidate: 0 for candidate in candidates}
    
    for vote in votes:
        for candidate, points in vote.items():
            scores[candidate] += points

    return sorted(scores.items(), key=lambda item: item[1], reverse=True)