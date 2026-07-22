"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs

# Stress-test profiles for Phase 4 evaluation.
PROFILES = {
    "Default (pop/happy)": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9, "acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "acoustic": False},
    "Adversarial (energetic but sad)": {"genre": "metal", "mood": "sad", "energy": 0.9},
}


def print_recommendations(label: str, user_prefs: dict, songs: list) -> None:
    """Prints the top-5 ranked recommendations for one named profile."""
    print(f"=== {label} ===")
    print(f"User profile: {user_prefs}")
    recommendations = recommend_songs(user_prefs, songs, k=5)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} - Score: {score:.2f}")
        print(f"   Because: {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for label, user_prefs in PROFILES.items():
        print_recommendations(label, user_prefs, songs)


if __name__ == "__main__":
    main()
