# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

When I looked into how Spotify or YouTube actually decide what to show you next, it comes down to two different tricks, usually mixed together. One is collaborative filtering which is basically using songs that other users with similar tastes played/skiped/saved in their playlistand and recommends them for you. It's how you end up finding a song you'd never have picked yourself. The problem is that it falls apart for brand-new songs or new users, since there's no history to compare yet. The other is content-based filtering which basically matches a song's own attributes (things such as genre, tempo, energy) against what one person tends to like. 

**`Song` uses:** `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness` which is pulled straight from `data/songs.csv`.

**`UserProfile` stores:** `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`.

**How I'm scoring a song:** genre and mood matches each add points, with mood weighted at least as much as genre — in my own experience two songs can share a genre tag and still feel nothing alike, but "chill" usually means chill. Energy isn't a "bigger is better" thing though, so instead of rewarding high energy I reward *closeness* to what the user actually wants:

```
energy_score = 1 - abs(song.energy - user.target_energy)
score = 2*genre_match + 2*mood_match + 1.5*energy_score + 1*acoustic_match
```
---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

(Fill this in after you've actually built and played with the recommender — see [`model_card.md`](model_card.md) for the fuller writeup.)

Once you've run it a bit, jot down a paragraph or two here in your own words: what actually surprised you about how a handful of numbers turns into a "recommendation," and where you can imagine this kind of scoring quietly going wrong for someone — like always favoring the loudest genre in the catalog, or never surfacing anything outside a user's stated taste even if they'd probably like it.



