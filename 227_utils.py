import pickle

ranks = pickle.load(open("227_ranks.pickle", "rb"))
num_of_speakers = 227


def get_ranking_distance(rating):
    rank_a = ranks[rating[0]]
    rank_b = ranks[rating[1]]
    return abs(rank_a - rank_b) / num_of_speakers


def has_ranking_distance(rating, distance):
    return get_ranking_distance(rating) >= distance


def predict_based_on_ranking(rating, external_speakers=[]):
    if not external_speakers:
        return int(ranks[rating[1]] > ranks[rating[0]])
    forbidden, index = includes_external_speakers(rating, external_speakers, return_index=True)
    if not forbidden:
        return int(ranks[rating[1]] > ranks[rating[0]])
    else:
        if index == 0:
            return int(ranks[rating[1]] > num_of_speakers/2)
        if index == 1:
            return int(ranks[rating[0]] < num_of_speakers / 2)


def includes_external_speakers(rating, speakers, return_index=False):
    common_speakers_a = set(speakers).intersection(set(rating[:1]))
    common_speakers_b = set(speakers).intersection(set(rating[1:2]))
    if return_index:
        return bool(common_speakers_a.union(common_speakers_b)), int(bool(common_speakers_b))
    else:
        return bool(common_speakers_a.union(common_speakers_b))


