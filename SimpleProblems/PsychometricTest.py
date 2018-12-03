
scores0 = [1,3,5,6,8]
lowerLimits0 = [2]
upperLimits0 = [6]

scores1 = [4,8,7]
lowerLimits1 = [2, 4]
upperLimits1 = [8,4]

def jobOffers(scores, lowerLimits, upperLimits):
    results = []

    for q, x in enumerate(list(zip(lowerLimits, upperLimits))):
        print(q, x)
        a = sum(i >= x[0] and i <= x[1] for i in scores)
        results.append(a)

    return results

print(jobOffers(scores0, lowerLimits0, upperLimits0))
print(jobOffers(scores1, lowerLimits1, upperLimits1))
