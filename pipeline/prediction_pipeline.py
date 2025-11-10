from config.paths_config import *
from utils.helpers import *


def hybrid_recommendation(user_id, user_weight=0.5, content_weight=0.5):
    # User recommendation
    similar_users = find_similar_users(
        user_id, USER_WEIGHTS_PATH, USER2USER_ENCODED, USER2USER_DECODED
    )

    user_pref = get_user_preferences(user_id, RATING_DF, ANIME_DF)
    user_recommended_animes = get_user_recommendations(
        similar_users, user_pref, ANIME_DF, SYNOPSIS_DF, RATING_DF
    )

    # Get the list of names of recommended animes
    user_recommended_anime_list = user_recommended_animes["anime_name"].tolist()

    # Content-based recommendation
    content_recommended_animes = []

    for anime in user_recommended_anime_list:
        similar_animes = find_similar_animes(
            anime,
            ANIME_WEIGHTS_PATH,
            ANIME2ANIME_ENCODED,
            ANIME2ANIME_DECODED,
            ANIME_DF,
        )

        if similar_animes is not None and not similar_animes.empty:
            content_recommended_animes.extend(similar_animes["name"].tolist())
        else:
            print(f"No similar anime found {anime}")

    # Combine the scores of the user-based and content-based recommendations
    combined_scores = {}

    # Collect all anime recommendations from both user-based and content-based recommendations assigning weights to each
    # Changing the weights will change the importance of each recommendation type (as they get sorted by score)
    for anime in user_recommended_anime_list:
        combined_scores[anime] = combined_scores.get(anime, 0) + user_weight

    for anime in content_recommended_animes:
        combined_scores[anime] = combined_scores.get(anime, 0) + content_weight

    # print(combined_scores.items()[0][1]) -> score
    sorted_animes = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

    return [anime for anime, score in sorted_animes[:10]]
