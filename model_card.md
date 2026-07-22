# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

I tested a profile for `metal, sad, energy 0.9`. No song is tagged both metal and sad, so the system just used genre + energy and recommended a metal song tagged **angry** — a mood miss doesn't stop a high score. The acoustic check also only adds points, never subtracts, so it can't really tell songs apart on that alone. And pop/lofi are the biggest genres in my 18-song catalog, so those profiles get strong lists while rarer genres (classical, reggae) fall back on energy matching alone.

---

## 7. Evaluation  

I ran five profiles through `src/main.py`: default pop/happy, High-Energy Pop, Chill Lofi, Deep Intense Rock, and an adversarial one (`metal/sad/energy=0.9`) meant to test a contradiction.

```
=== Default (pop/happy) ===
User profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}
1. Sunrise City - Score: 5.47 (genre match +2.0, mood match +2.0, energy closeness +1.47)
2. Rooftop Lights - Score: 3.44 (mood match +2.0, energy closeness +1.44)
3. Gym Hero - Score: 3.30 (genre match +2.0, energy closeness +1.30)
4. Concrete Anthem - Score: 1.47 (energy closeness +1.47)
5. Night Drive Loop - Score: 1.42 (energy closeness +1.42)

=== High-Energy Pop ===
User profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9, 'acoustic': False}
1. Sunrise City - Score: 6.38 (genre match +2.0, mood match +2.0, energy closeness +1.38, acoustic match +1.0)
2. Gym Hero - Score: 4.46 (genre match +2.0, energy closeness +1.46, acoustic match +1.0)
3. Rooftop Lights - Score: 4.29 (mood match +2.0, energy closeness +1.29, acoustic match +1.0)
4. Storm Runner - Score: 2.48 (energy closeness +1.48, acoustic match +1.0)
5. Neon Static - Score: 2.42 (energy closeness +1.43, acoustic match +1.0)

=== Chill Lofi ===
User profile: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'acoustic': True}
1. Library Rain - Score: 6.50 (genre match +2.0, mood match +2.0, energy closeness +1.50, acoustic match +1.0)
2. Midnight Coding - Score: 6.39 (genre match +2.0, mood match +2.0, energy closeness +1.40, acoustic match +1.0)
3. Focus Flow - Score: 4.42 (genre match +2.0, energy closeness +1.42, acoustic match +1.0)
4. Spacewalk Thoughts - Score: 4.39 (mood match +2.0, energy closeness +1.40, acoustic match +1.0)
5. Coffee Shop Stories - Score: 2.47 (energy closeness +1.47, acoustic match +1.0)

=== Deep Intense Rock ===
User profile: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'acoustic': False}
1. Storm Runner - Score: 6.48 (genre match +2.0, mood match +2.0, energy closeness +1.48, acoustic match +1.0)
2. Gym Hero - Score: 4.46 (mood match +2.0, energy closeness +1.46, acoustic match +1.0)
3. Neon Static - Score: 2.42 (energy closeness +1.43, acoustic match +1.0)
4. Broken Glass - Score: 2.40 (energy closeness +1.40, acoustic match +1.0)
5. Sunrise City - Score: 2.38 (energy closeness +1.38, acoustic match +1.0)

=== Adversarial (metal / sad / energy=0.9) ===
User profile: {'genre': 'metal', 'mood': 'sad', 'energy': 0.9}
1. Broken Glass - Score: 3.40 (genre match +2.0, energy closeness +1.40)   <- actually tagged "angry," not sad
2. Storm Runner - Score: 1.48 (energy closeness +1.48)
3. Gym Hero - Score: 1.46 (energy closeness +1.46)
4. Neon Static - Score: 1.43 (energy closeness +1.43)
5. Sunrise City - Score: 1.38 (energy closeness +1.38)
```

**Comparisons:**

- **Default vs. High-Energy Pop:** raising the energy target moves Gym Hero (pop, but mood *intense*) up to #2, since its energy is now a closer match. Makes sense.
- **High-Energy Pop vs. Deep Intense Rock:** same energy target, different genre/mood — the #1 pick flips from Sunrise City to Storm Runner as expected, and Gym Hero lands at #2 in both since it's a genuine crossover (pop-tagged, intense mood).
- **Deep Intense Rock vs. Adversarial:** the surprise. Swap "intense" for "sad" and the #1 song barely changes — Broken Glass still wins on genre + energy, even though it's tagged "angry," not sad. The scoring can't tell when a mood mismatch should really matter.

**Plain-language version:** ask for "happy pop" and you might still get "Gym Hero," a pump-up gym anthem, because it's tagged pop and has very high energy — the system can't tell "happy energetic" apart from "aggressive energetic."

**Weight-shift experiment:** I temporarily halved the genre weight and doubled the energy weight, then reran all five profiles. The #1 song barely changed, but #2–#4 shuffled — songs that only matched on mood moved ahead of songs that only matched on genre. A real, explainable shift, but not clearly "more accurate," just a different call on what matters more. Reverted after.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
