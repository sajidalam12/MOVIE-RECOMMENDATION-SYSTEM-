import math
from collections import Counter

class Film:
    def __init__(self, name, summary, genre="general", education_note=""):
        self.name = name
        self.summary = summary.lower()
        self.genre = genre.lower()
        self.education_note = education_note.strip()

def find_similarity(text1, text2):
    wordsA = text1.split()
    wordsB = text2.split()
    all_words = set(wordsA + wordsB)

    word_freq1 = Counter({word: 0 for word in all_words})
    word_freq2 = Counter({word: 0 for word in all_words})

    for word in wordsA:
        word_freq1[word] += 1
    for word in wordsB:
        word_freq2[word] += 1

    dot = sum(word_freq1[word] * word_freq2[word] for word in all_words)
    norm1 = sum(count**2 for count in word_freq1.values())
    norm2 = sum(count**2 for count in word_freq2.values())

    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (math.sqrt(norm1) * math.sqrt(norm2))

def suggest_movies(films, input_title):
    input_lower = input_title.lower()

    # Suggest by genre first
    if "bollywood" in input_lower:
        bollywood = [f for f in films if f.genre == "bollywood"]
        print("\n🎬 Recommended Bollywood Movies:")
        for f in bollywood:
            print(f"👉 {f.name}")
        return

    elif "hollywood" in input_lower:
        hollywood = [f for f in films if f.genre == "hollywood"]
        print("\n🎬 Recommended Hollywood Movies (Educational):")
        for f in hollywood:
            print(f"\n👉 {f.name}\n📚 {f.education_note}")
        return

    # Otherwise do partial title match
    matched = [f for f in films if input_lower in f.name.lower()]
    if matched:
        print(f"\n📽 You searched for: {input_title}")
        print("🎬 Matching movies:")
        for f in matched:
            print("👉", f.name)
        return

    # Exact match for similarity fallback
    selected = next((f for f in films if f.name.lower() == input_lower), None)
    if not selected:
        print("❌ Movie not found.")
        return

    scores = {
        f.name: find_similarity(selected.summary, f.summary)
        for f in films if f.name.lower() != input_lower
    }

    top3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
    if top3:
        print("\n📽 You might also enjoy:")
        for title, _ in top3:
            print("👉", title)

def main():
    movie_list = [
        # Avengers Series
        Film("The Avengers (2012)", "Avengers unite to stop Loki from world domination"),
        Film("Avengers: Age of Ultron (2015)", "Avengers face a deadly AI named Ultron"),
        Film("Avengers: Infinity War (2018)", "Thanos collects all infinity stones"),
        Film("Avengers: Endgame (2019)", "Time travel mission to undo Thanos' snap"),

        # Iron Man Series
        Film("Iron Man (2008)", "Tony Stark builds a suit to escape captivity and becomes Iron Man"),
        Film("Iron Man 2 (2010)", "Tony battles government pressure and a new enemy"),
        Film("Iron Man 3 (2013)", "Tony struggles with PTSD and fights a mysterious terrorist"),

        # Bollywood
        Film("3 Idiots", "A tale of three engineering students and their journey of self-discovery", "bollywood"),
        Film("Dangal", "A father trains his daughters to become world-class wrestlers", "bollywood"),
        Film("Chhichhore", "A story about college life and suicide awareness", "bollywood"),
        Film("English Medium", "A father's struggle for his daughter's education", "bollywood"),
        Film("Tiger Zinda Hai", "An Indian spy action thriller", "bollywood"),
        Film("Dilwale Dulhania Le Jayenge (DDLJ)", "A romantic tale of Indian traditions", "bollywood"),

        # Hollywood Educational
        Film("The Pursuit of Happyness (2006)", "Perseverance and self-belief in financial struggle", "hollywood",
             "Teaches resilience, hard work, and how education and determination can change lives."),
        Film("Good Will Hunting (1997)", "Math prodigy with deep personal trauma", "hollywood",
             "Highlights the power of mentorship and untapped genius."),
        Film("A Beautiful Mind (2001)", "Genius mathematician John Nash and mental illness", "hollywood",
             "Explores schizophrenia and how Nash overcame adversity in academia."),
        Film("The Imitation Game (2014)", "Alan Turing cracking the Enigma code", "hollywood",
             "Introduces cryptography, computer science, and wartime ethics."),
        Film("Dead Poets Society (1989)", "English teacher inspires his students", "hollywood",
             "Encourages critical thinking, self-expression, and non-conformity."),
    ]

    fav = input("🎬 Enter a movie name or genre (e.g., Bollywood, Hollywood): ")
    suggest_movies(movie_list, fav)

if __name__ == "__main__":
    main()
