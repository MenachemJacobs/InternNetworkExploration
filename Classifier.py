def calculate_secondary_score(feature_list):
    accumulator = 0.0

    for feature in feature_list:
        accumulator += feature

    return accumulator
