from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

# Algorithm recipe (see README "How The System Works")
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 2.0
ENERGY_WEIGHT = 1.5
ACOUSTIC_WEIGHT = 1.0
ACOUSTIC_THRESHOLD = 0.5


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _score_and_reasons(
    genre: str,
    mood: str,
    energy: float,
    acousticness: float,
    fav_genre: Optional[str],
    fav_mood: Optional[str],
    target_energy: float,
    likes_acoustic: Optional[bool],
) -> Tuple[float, List[str]]:
    """Scores one song's attributes against one user's preferences, returning (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    if fav_genre is not None and genre == fav_genre:
        score += GENRE_WEIGHT
        reasons.append(f"genre match (+{GENRE_WEIGHT:.1f})")

    if fav_mood is not None and mood == fav_mood:
        score += MOOD_WEIGHT
        reasons.append(f"mood match (+{MOOD_WEIGHT:.1f})")

    energy_closeness = 1 - abs(energy - target_energy)
    energy_points = ENERGY_WEIGHT * energy_closeness
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    if likes_acoustic is not None:
        is_acoustic = acousticness > ACOUSTIC_THRESHOLD
        if is_acoustic == likes_acoustic:
            score += ACOUSTIC_WEIGHT
            reasons.append(f"acoustic preference match (+{ACOUSTIC_WEIGHT:.1f})")

    return score, reasons


class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Scores every song for this user and returns the top-k, highest score first."""
        scored = [
            (song, self._score(user, song))
            for song in self.songs
        ]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable breakdown of why a song scored the way it did for this user."""
        score, reasons = self._score_with_reasons(user, song)
        if not reasons:
            return f"No strong matches (score: {score:.2f})"
        return f"{', '.join(reasons)} - total score: {score:.2f}"

    def _score(self, user: UserProfile, song: Song) -> float:
        """Returns just the numeric score for one song and one user."""
        return self._score_with_reasons(user, song)[0]

    def _score_with_reasons(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Runs the shared scoring rule for one song and one user."""
        return _score_and_reasons(
            song.genre,
            song.mood,
            song.energy,
            song.acousticness,
            user.favorite_genre,
            user.favorite_mood,
            user.target_energy,
            user.likes_acoustic,
        )


def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file into a list of dicts with numeric fields converted."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song dict against a user preference dict, returning (score, reasons)."""
    return _score_and_reasons(
        song["genre"],
        song["mood"],
        song["energy"],
        song["acousticness"],
        user_prefs.get("genre"),
        user_prefs.get("mood"),
        user_prefs.get("energy", 0.5),
        user_prefs.get("acoustic"),
    )


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song, ranks them, and returns the top-k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no strong matches"
        scored.append((song, score, explanation))

    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
