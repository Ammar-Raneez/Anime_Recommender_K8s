import joblib
import numpy as np
import pandas as pd

from config.paths_config import *


# Get the anime frame for a given anime id or name
def get_anime_frame(anime, path_df):
    df = pd.read_csv(path_df)
    if isinstance(anime, int):
        return df[df.anime_id == anime]

    if isinstance(anime, str):
        return df[df.eng_version == anime]


# Get the synopsis for a given anime id or name
def get_synopsis(anime, path_synopsis_df):
    synopsis_df = pd.read_csv(path_synopsis_df)
    if isinstance(anime, int):
        return synopsis_df[synopsis_df.MAL_ID == anime].sypnopsis.values[0]

    if isinstance(anime, str):
        return synopsis_df[synopsis_df.Name == anime].sypnopsis.values[0]


# Content-based recommendation
def find_similar_animes(
    name,
    path_anime_weights,
    path_anime2anime_encoded,
    path_anime2anime_decoded,
    path_anime_df,
    n=10,
    return_dist=False,
    neg=False,
):
    """
    Find similar animes to the given anime name using content-based filtering.

    Args:
        name: Name of the anime to find similar animes to
        path_anime_weights: Weights for the anime embeddings
        path_anime2anime_encoded: Encoded anime ids
        path_anime2anime_decoded: Decoded anime ids
        path_anime_df: DataFrame containing anime information
        n: Number of similar animes to return
        return_dist: Whether to return the distances
        neg: Whether to return the farthest animes
    """

    # Load weights and encoded-decoded mappings
    anime_weights = joblib.load(path_anime_weights)
    anime2anime_encoded = joblib.load(path_anime2anime_encoded)
    anime2anime_decoded = joblib.load(path_anime2anime_decoded)

    # Get the anime ID for the given name
    index = get_anime_frame(name, path_anime_df).anime_id.values[0]
    encoded_index = anime2anime_encoded.get(index)

    if encoded_index is None:
        raise ValueError(f"Encoded index not found for anime ID: {index}")

    weights = anime_weights

    # Compute the similarity distances between the anime and all other animes
    dists = np.dot(weights, weights[encoded_index])

    # Sort the distances to get the most similar animes
    sorted_dists = np.argsort(dists)

    # Add 1 to include this anime itself in the results
    n = n + 1

    # Select closest or farthest based on 'neg' flag
    if neg:
        closest = sorted_dists[:n]
    else:
        closest = sorted_dists[-n:]

    # Return distances and closest indices if requested
    if return_dist:
        return dists, closest

    # Build the similarity array
    SimilarityArr = []
    for close in closest:
        decoded_id = anime2anime_decoded.get(close)
        anime_frame = get_anime_frame(decoded_id, path_anime_df)
        anime_name = anime_frame.eng_version.values[0]
        genre = anime_frame.Genres.values[0]
        similarity = dists[close]

        SimilarityArr.append(
            {
                "anime_id": decoded_id,
                "name": anime_name,
                "similarity": similarity,
                "genre": genre,
            }
        )

    # Create a DataFrame with results and sort by similarity
    Frame = pd.DataFrame(SimilarityArr).sort_values(by="similarity", ascending=False)

    # Drop the anime itself from the results
    return Frame[Frame.anime_id != index].drop(["anime_id"], axis=1)


# User-based recommendation (collaborative filtering)
def find_similar_users(
    item_input,
    path_user_weights,
    path_user2user_encoded,
    path_user2user_decoded,
    n=10,
    return_dist=False,
    neg=False,
):
    """
    Find similar users to the given user id using collaborative filtering.
    Works the same as find_similar_animes, just for users instead of animes.

    Args:
        item_input: User id to find similar users to
        path_user_weights: Weights for the user embeddings
        path_user2user_encoded: Encoded user ids
        path_user2user_decoded: Decoded user ids
    """

    try:
        user_weights = joblib.load(path_user_weights)
        user2user_encoded = joblib.load(path_user2user_encoded)
        user2user_decoded = joblib.load(path_user2user_decoded)

        index = item_input
        encoded_index = user2user_encoded.get(index)

        weights = user_weights

        dists = np.dot(weights, weights[encoded_index])
        sorted_dists = np.argsort(dists)

        n = n + 1

        if neg:
            closest = sorted_dists[:n]
        else:
            closest = sorted_dists[-n:]

        if return_dist:
            return dists, closest

        SimilarityArr = []

        for close in closest:
            similarity = dists[close]

            if isinstance(item_input, int):
                decoded_id = user2user_decoded.get(close)
                SimilarityArr.append(
                    {"similar_users": decoded_id, "similarity": similarity}
                )

        similar_users = pd.DataFrame(SimilarityArr).sort_values(
            by="similarity", ascending=False
        )

        # Drop the user itself from the results
        similar_users = similar_users[similar_users.similar_users != item_input]
        return similar_users
    except Exception as e:
        print("Error Occured", e)


# Get user preferences
def get_user_preferences(user_id, path_rating_df, path_anime_df):
    rating_df = pd.read_csv(path_rating_df)
    df = pd.read_csv(path_anime_df)

    animes_watched_by_user = rating_df[rating_df.user_id == user_id]

    # Get the 75th percentile rating (top rated animes)
    user_rating_percentile = np.percentile(animes_watched_by_user.rating, 75)

    # Filter the animes watched by the user to only include those with a rating greater than or equal to the 75th percentile
    animes_watched_by_user = animes_watched_by_user[
        animes_watched_by_user.rating >= user_rating_percentile
    ]

    # Get the top rated animes watched by the user
    top_animes_user = animes_watched_by_user.sort_values(
        by="rating", ascending=False
    ).anime_id.values

    anime_df_rows = df[df["anime_id"].isin(top_animes_user)]
    anime_df_rows = anime_df_rows[["eng_version", "Genres"]]

    return anime_df_rows


# Get user recommendations
def get_user_recommendations(
    similar_users, user_pref, path_anime_df, path_synopsis_df, path_rating_df, n=10
):
    """
    Get user recommendations based on similar users and their preferences.

    Args:
        similar_users: DataFrame of similar users
        user_pref: DataFrame of this user's preferences
        path_anime_df: DataFrame of anime information
        path_synopsis_df: DataFrame of anime synopsis
        path_rating_df: DataFrame of ratings
        n: Number of recommendations to return
    """

    recommended_animes = []
    anime_list = []

    for user_id in similar_users.similar_users.values:
        # Get the preferences of the similar users
        pref_list = get_user_preferences(int(user_id), path_rating_df, path_anime_df)

        # Remove the animes that this user has already watched
        pref_list = pref_list[~pref_list.eng_version.isin(user_pref.eng_version.values)]

        if not pref_list.empty:
            anime_list.append(pref_list.eng_version.values)

    if anime_list:
        anime_list = pd.DataFrame(anime_list)

        # Get the top n anime
        sorted_list = pd.DataFrame(
            pd.Series(anime_list.values.ravel()).value_counts()
        ).head(n)

        for i, anime_name in enumerate(sorted_list.index):
            # Get the number of times the anime was recommended by the similar users
            n_user_pref = sorted_list[sorted_list.index == anime_name].values[0][0]

            if isinstance(anime_name, str):
                frame = get_anime_frame(anime_name, path_anime_df)
                anime_id = frame.anime_id.values[0]
                genre = frame.Genres.values[0]
                synopsis = get_synopsis(int(anime_id), path_synopsis_df)

                recommended_animes.append(
                    {
                        "n": n_user_pref,
                        "anime_name": anime_name,
                        "Genres": genre,
                        "Synopsis": synopsis,
                    }
                )

    return pd.DataFrame(recommended_animes).head(n)
