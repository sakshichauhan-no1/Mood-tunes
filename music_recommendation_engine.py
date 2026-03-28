"""
AI-Powered Music Recommendation Engine
=======================================
Understands human emotions and creates personalized playlists
"""

import json
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class Mood(Enum):
    SAD = "sad"
    HAPPY = "happy"
    STRESSED = "stressed"
    ROMANTIC = "romantic"
    ENERGETIC = "energetic"
    LONELY = "lonely"
    ANXIOUS = "anxious"
    GRATEFUL = "grateful"
    HEARTBROKEN = "heartbroken"
    EXCITED = "excited"


class EnergyLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Song:
    name: str
    artist: str
    mood: Mood
    energy: EnergyLevel
    language: str
    reason: str
    search_query: str


class EmotionAnalyzer:
    def __init__(self):
        self.mood_keywords = {
            Mood.SAD: ['sad', 'unhappy', 'down', 'depressed', 'blue', 'melancholy', 'tears', 'crying'],
            Mood.HAPPY: ['happy', 'joy', 'cheerful', 'delighted', 'glad', 'pleased', 'wonderful', 'great'],
            Mood.STRESSED: ['stressed', 'anxious', 'worried', 'overwhelmed', 'tense', 'pressure', 'burnout'],
            Mood.ROMANTIC: ['love', 'romantic', 'crush', 'heart', 'feelings', 'missing', 'together', 'lover'],
            Mood.ENERGETIC: ['energetic', 'pumped', 'hyped', 'excited', 'powerful', 'strong', 'invincible'],
            Mood.LONELY: ['lonely', 'alone', 'isolated', 'missing', 'nobody', 'empty', 'isolated', 'abandoned'],
            Mood.ANXIOUS: ['anxious', 'nervous', 'scared', 'fear', 'panic', 'worried', 'uncertain'],
            Mood.HEARTBROKEN: ['heartbroken', 'breakup', 'lost love', 'betrayed', 'cheated', 'love hurts'],
            Mood.EXCITED: ['excited', 'thrilled', 'pumped', 'can\'t wait', 'amazing', 'awesome'],
            Mood.GRATEFUL: ['grateful', 'thankful', 'blessed', 'appreciate', 'lucky']
        }
        
        self.energy_keywords = {
            EnergyLevel.LOW: ['tired', 'exhausted', 'drained', 'weak', 'sleepy', 'low energy'],
            EnergyLevel.MEDIUM: ['okay', 'fine', 'moderate', 'normal', 'average'],
            EnergyLevel.HIGH: ['high energy', 'pumped', 'hyped', 'full of energy', 'strong']
        }
    
    def analyze(self, user_input: str) -> Tuple[Mood, EnergyLevel]:
        user_input_lower = user_input.lower()
        
        mood_scores = {}
        for mood, keywords in self.mood_keywords.items():
            score = sum(1 for keyword in keywords if keyword in user_input_lower)
            mood_scores[mood] = score
        
        primary_mood = max(mood_scores, key=mood_scores.get)
        if mood_scores[primary_mood] == 0:
            primary_mood = Mood.SAD
        
        energy_scores = {}
        for energy, keywords in self.energy_keywords.items():
            score = sum(1 for keyword in keywords if keyword in user_input_lower)
            energy_scores[energy] = score
        
        if energy_scores[EnergyLevel.HIGH] > 0:
            energy_level = EnergyLevel.HIGH
        elif energy_scores[EnergyLevel.LOW] > 0:
            energy_level = EnergyLevel.LOW
        else:
            energy_level = EnergyLevel.MEDIUM
        
        if primary_mood in [Mood.HAPPY, Mood.EXCITED, Mood.ENERGETIC]:
            energy_level = EnergyLevel.HIGH
        elif primary_mood in [Mood.SAD, Mood.LONELY, Mood.HEARTBROKEN]:
            energy_level = EnergyLevel.LOW
        
        return primary_mood, energy_level


class SongDatabase:
    def __init__(self):
        self.songs = self._build_song_database()
    
    def _build_song_database(self) -> List[Song]:
        return [
            # SAD SONGS
            Song("Tum Hi Ho", "Aashiqui 2", Mood.SAD, EnergyLevel.LOW, "Hindi", 
                 "Perfect for drowning in emotions", "tum hi ho aashiqui 2"),
            Song("Channa Mereya", "Ae Dil Hai Mushkil", Mood.SAD, EnergyLevel.LOW, "Hindi",
                 "Heart-wrenching farewell feelings", "channa mereya"),
            Song("Someone Like You", "Adele", Mood.SAD, EnergyLevel.LOW, "English",
                 "Bittersweet memories of lost love", "adele someone like you"),
            Song("Agar Tum Saath Ho", "Tamasha", Mood.SAD, EnergyLevel.LOW, "Hindi",
                 "Letting go is hard to do", "agar tum saath ho"),
            Song("The Night We Met", "Lord Huron", Mood.SAD, EnergyLevel.LOW, "English",
                 "Wish we could go back in time", "lord huron the night we met"),
            
            # HEARTBROKEN SONGS
            Song("Tera Chehra", "Adnan Sami", Mood.HEARTBROKEN, EnergyLevel.LOW, "Hindi",
                 "Your face haunts me still", "tera chehra adnan sami"),
            Song("Let Her Go", "Passenger", Mood.HEARTBROKEN, EnergyLevel.LOW, "English",
                 "Only realize value when it's gone", "passenger let her go"),
            Song("Khamosiyan", "Ahmed Ali", Mood.HEARTBROKEN, EnergyLevel.LOW, "Hindi",
                 "Singing in the silence of loss", "khamosiyan"),
            Song("All I Want", "Kodaline", Mood.HEARTBROKEN, EnergyLevel.LOW, "English",
                 "Just want you back", "kodaline all i want"),
            Song("Mere Rashke Qamar", "Nusrat Fateh Ali Khan", Mood.HEARTBROKEN, EnergyLevel.LOW, "Hindi",
                 "Bless my jealousy for you", "mere rashke qamar"),
            
            # LONELY SONGS
            Song("Tere Bina", "Guru", Mood.LONELY, EnergyLevel.LOW, "Hindi",
                 "Can't imagine life without you", "tere bina guru"),
            Song("Fix You", "Coldplay", Mood.LONELY, EnergyLevel.LOW, "English",
                 "Hold onto hope when darkness comes", "coldplay fix you"),
            Song("Agar Kyun Na", "Mithoon", Mood.LONELY, EnergyLevel.LOW, "Hindi",
                 "Why did this have to happen", "agar kyun na mithoon"),
            Song("Skinny Love", "Bon Iver", Mood.LONELY, EnergyLevel.LOW, "English",
                 "Trying to make you love me", "bon iver skinny love"),
            Song("Tum Jo Aaye", "Once Upon Time", Mood.LONELY, EnergyLevel.LOW, "Hindi",
                 "When you came into my life", "tum jo aaye"),
            
            # STRESSED SONGS
            Song("Khwabon Ka Jahan", "Aashiqui 2", Mood.STRESSED, EnergyLevel.MEDIUM, "Hindi",
                 "Lost in dreams of escape", "khwabon ka jahan"),
            Song("Breathe", "Faith Hill", Mood.STRESSED, EnergyLevel.LOW, "English",
                 "Take a moment to breathe", "faith hill breathe"),
            Song("Kuch Is Tara", "Tashan", Mood.STRESSED, EnergyLevel.MEDIUM, "Hindi",
                 "Searching for something special", "kuch is tara"),
            Song("Weightless", "Marconi Union", Mood.STRESSED, EnergyLevel.LOW, "English",
                 "Scientifically proven to reduce anxiety", "marconi union weightless"),
            Song("Phir Le Aaya Dil", "Barfi", Mood.STRESSED, EnergyLevel.MEDIUM, "Hindi",
                 "Heart skips a beat again", "phir le aaya dil"),
            
            # ANXIOUS SONGS
            Song("Raat Rani", "Love Aaj Kal", Mood.ANXIOUS, EnergyLevel.LOW, "Hindi",
                 "Night creature of worry", "raat rani love aaj kal"),
            Song("Breathe Easy", "James Bay", Mood.ANXIOUS, EnergyLevel.LOW, "English",
                 "Take it easy, everything's fine", "james bay breathe easy"),
            Song("Mere Haath Mein", "Fanaa", Mood.ANXIOUS, EnergyLevel.MEDIUM, "Hindi",
                 "Feel my heartbeat with you", "mere haath mein fanaa"),
            Song("Thunder", "Roy Orbison", Mood.ANXIOUS, EnergyLevel.MEDIUM, "English",
                 "Lightning strikes suddenly", "roy orbison thunder"),
            Song("Shukran Allah", "Luck By Chance", Mood.ANXIOUS, EnergyLevel.MEDIUM, "Hindi",
                 "Thank you God for everything", "shukran allah"),
            
            # HAPPY SONGS
            Song("Good Time", "Owl City ft Carly Rae", Mood.HAPPY, EnergyLevel.HIGH, "English",
                 "Always a good time ahead", "owl city good time"),
            Song("Kala Chashma", "Baar Baar Dekho", Mood.HAPPY, EnergyLevel.HIGH, "Hindi",
                 "Total beach vibes and fun", "kala chashma"),
            Song("Happy", "Pharrell Williams", Mood.HAPPY, EnergyLevel.HIGH, "English",
                 "Clap along if you feel happiness", "pharrell williams happy"),
            Song("Ghungroo", "War", Mood.HAPPY, EnergyLevel.HIGH, "Hindi",
                 "Dance to the beat", "ghungroo war"),
            Song("Can't Stop the Feeling", "Justin Timberlake", Mood.HAPPY, EnergyLevel.HIGH, "English",
                 "Dance moves come naturally", "justin timberlake cant stop"),
            
            # EXCITED SONGS
            Song("Believer", "Imagine Dragons", Mood.EXCITED, EnergyLevel.HIGH, "English",
                 "Pain becomes my power", "imagine dragons believer"),
            Song("Kar Gayi Chull", "Kapoor & Sons", Mood.EXCITED, EnergyLevel.HIGH, "Hindi",
                 "Party anthem of the year", "kar gayi chull"),
            Song("Uptown Funk", "Bruno Mars", Mood.EXCITED, EnergyLevel.HIGH, "English",
                 "Ultimate dance floor filler", "bruno mars uptown funk"),
            Song("Morni", "Lahore 2", Mood.EXCITED, EnergyLevel.HIGH, "Hindi",
                 "Get lost in the music", "morni lahore 2"),
            Song("Shake It Off", "Taylor Swift", Mood.EXCITED, EnergyLevel.HIGH, "English",
                 "Let go of all negativity", "taylor swift shake it off"),
            
            # ENERGETIC SONGS
            Song("Zinda", "Bhaag Milkha Bhaag", Mood.ENERGETIC, EnergyLevel.HIGH, "Hindi",
                 "I'm alive and unstoppable", "zinda bhaag milkha"),
            Song("Eye of the Tiger", "Survivor", Mood.ENERGETIC, EnergyLevel.HIGH, "English",
                 "Rise up and fight harder", "survivor eye of the tiger"),
            Song("Sultan", "Sultan", Mood.ENERGETIC, EnergyLevel.HIGH, "Hindi",
                 "Champion of destiny", "sultan title song"),
            Song("Stronger", "Kanye West", Mood.ENERGETIC, EnergyLevel.HIGH, "English",
                 "What doesn't kill makes you stronger", "kanye west stronger"),
            Song("Dhoom Machale", "Dhoom", Mood.ENERGETIC, EnergyLevel.HIGH, "Hindi",
                 "Ride the wave of excitement", "dhoom machale"),
            
            # ROMANTIC SONGS
            Song("Tum Se Hi", "Jab We Met", Mood.ROMANTIC, EnergyLevel.MEDIUM, "Hindi",
                 "Everything revolves around you", "tum se hi jab we met"),
            Song("Perfect", "Ed Sheeran", Mood.ROMANTIC, EnergyLevel.MEDIUM, "English",
                 "Dance with me under the stars", "ed sheeran perfect"),
            Song("Mere Rashke Qamar", "One Night", Mood.ROMANTIC, EnergyLevel.MEDIUM, "Hindi",
                 "My jealousy praises you", "mere rashke qamar one night"),
            Song("All of Me", "John Legend", Mood.ROMANTIC, EnergyLevel.LOW, "English",
                 "Love every inch of you", "john legend all of me"),
            Song("Gerua", "Dilwale", Mood.ROMANTIC, EnergyLevel.MEDIUM, "Hindi",
                 "Colors of our love story", "gerua dilwale"),
            
            # GRATEFUL SONGS
            Song("Tere Bina", "A.R. Rahman", Mood.GRATEFUL, EnergyLevel.MEDIUM, "Hindi",
                 "Life without you is nothing", "tere bina a r rahman"),
            Song("Count on Me", "Bruno Mars", Mood.GRATEFUL, EnergyLevel.MEDIUM, "English",
                 "You can count on me", "bruno mars count on me"),
            Song("Suno Na Sangemarmar", "Young", Mood.GRATEFUL, EnergyLevel.MEDIUM, "Hindi",
                 "Listen to my heartbeat", "suno na sangemarmar"),
            Song("Better Together", "Jack Johnson", Mood.GRATEFUL, EnergyLevel.LOW, "English",
                 "But not always", "jack johnson better together"),
            Song("Dil Dhadakne Do", "Zoya Akhtar", Mood.GRATEFUL, EnergyLevel.HIGH, "Hindi",
                 "Let the heart beat loud", "dil dhadakne do"),
        ]
    
    def get_songs_by_mood(self, mood: Mood, count: int = 10) -> List[Song]:
        mood_songs = [song for song in self.songs if song.mood == mood]
        return mood_songs[:count]
    
    def get_transition_songs(self, from_mood: Mood, to_mood: Mood) -> List[Song]:
        transition_songs = [
            Song("Raabta", "Agent Vinod", Mood.EXCITED, EnergyLevel.MEDIUM, "Hindi",
                 "There's a connection between us", "raabta agent vinod"),
            Song("Ho Hey", "The Lumineers", Mood.HAPPY, EnergyLevel.MEDIUM, "English",
                 "Simple joys of togetherness", "the lumineers ho hey"),
            Song("Jeene Ke Liye", "Humsafar", Mood.HAPPY, EnergyLevel.MEDIUM, "Hindi",
                 "For the sake of living", "jeene ke liye humsafar"),
            Song("Counting Stars", "OneRepublic", Mood.EXCITED, EnergyLevel.MEDIUM, "English",
                 "Possibilities are endless", "onerepublic counting stars"),
            Song("Kuch Toh Log Kahenge", "Remote", Mood.HAPPY, EnergyLevel.MEDIUM, "Hindi",
                 "People will talk", "kuch toh log kahenge"),
        ]
        return transition_songs


class PlaylistGenerator:
    def __init__(self):
        self.song_db = SongDatabase()
        self.activity_suggestions = {
            Mood.SAD: "Take a warm bath and write your feelings in a journal",
            Mood.HEARTBROKEN: "Watch a comfort movie and cuddle with a blanket",
            Mood.LONELY: "Call an old friend you haven't spoken to in a while",
            Mood.STRESSED: "Do a 5-minute breathing exercise while listening",
            Mood.ANXIOUS: "Take a walk outside or do light stretching",
            Mood.HAPPY: "Share your happiness by messaging someone you love",
            Mood.EXCITED: "Channel that energy into a creative project",
            Mood.ENERGETIC: "Go for a run or do a quick workout",
            Mood.ROMANTIC: "Plan a surprise for someone special",
            Mood.GRATEFUL: "Write a thank you note to someone who helped you"
        }
    
    def generate_playlist(self, mood: Mood, energy: EnergyLevel, num_songs: int = 5) -> Dict:
        if num_songs != 5:
            raise ValueError("Playlist must contain exactly 5 songs")
        
        start_songs = self.song_db.get_songs_by_mood(mood, 2)
        
        if mood in [Mood.SAD, Mood.HEARTBROKEN, Mood.LONELY]:
            transition_mood = Mood.EXCITED
        elif mood in [Mood.STRESSED, Mood.ANXIOUS]:
            transition_mood = Mood.HAPPY
        elif mood in [Mood.HAPPY, Mood.EXCITED, Mood.ENERGETIC]:
            transition_mood = Mood.ROMANTIC
        else:
            transition_mood = Mood.HAPPY
        
        transition_songs = self.song_db.get_transition_songs(mood, transition_mood)
        transition_song = transition_songs[0] if transition_songs else None
        
        uplift_songs = []
        if mood in [Mood.SAD, Mood.HEARTBROKEN, Mood.LONELY]:
            uplift_moods = [Mood.HAPPY, Mood.EXCITED, Mood.GRATEFUL]
        elif mood in [Mood.STRESSED, Mood.ANXIOUS]:
            uplift_moods = [Mood.HAPPY, Mood.GRATEFUL]
        else:
            uplift_moods = [Mood.EXCITED, Mood.ENERGETIC]
        
        for uplift_mood in uplift_moods:
            songs = self.song_db.get_songs_by_mood(uplift_mood, 2)
            uplift_songs.extend(songs)
            if len(uplift_songs) >= 2:
                break
        
        uplift_songs = uplift_songs[:2]
        
        playlist = []
        
        if len(start_songs) >= 1:
            playlist.append({
                "stage": "start",
                "song": start_songs[0].name,
                "artist": start_songs[0].artist,
                "reason": start_songs[0].reason,
                "search_query": start_songs[0].search_query
            })
        
        if len(start_songs) >= 2:
            playlist.append({
                "stage": "start",
                "song": start_songs[1].name,
                "artist": start_songs[1].artist,
                "reason": start_songs[1].reason,
                "search_query": start_songs[1].search_query
            })
        
        if transition_song:
            playlist.append({
                "stage": "transition",
                "song": transition_song.name,
                "artist": transition_song.artist,
                "reason": transition_song.reason,
                "search_query": transition_song.search_query
            })
        
        if len(uplift_songs) >= 1:
            playlist.append({
                "stage": "uplift",
                "song": uplift_songs[0].name,
                "artist": uplift_songs[0].artist,
                "reason": uplift_songs[0].reason,
                "search_query": uplift_songs[0].search_query
            })
        
        if len(uplift_songs) >= 2:
            playlist.append({
                "stage": "uplift",
                "song": uplift_songs[1].name,
                "artist": uplift_songs[1].artist,
                "reason": uplift_songs[1].reason,
                "search_query": uplift_songs[1].search_query
            })
        
        while len(playlist) < 5:
            fallback_song = self.song_db.get_songs_by_mood(Mood.HAPPY, 1)
            if fallback_song:
                playlist.append({
                    "stage": "uplift",
                    "song": fallback_song[0].name,
                    "artist": fallback_song[0].artist,
                    "reason": fallback_song[0].reason,
                    "search_query": fallback_song[0].search_query
                })
        
        activity = self.activity_suggestions.get(mood, "Take deep breaths and focus on the music")
        
        return {
            "mood": mood.value,
            "energy_level": energy.value,
            "playlist": playlist,
            "activity_suggestion": activity
        }


def get_music_recommendation(user_input: str) -> str:
    analyzer = EmotionAnalyzer()
    generator = PlaylistGenerator()
    
    mood, energy = analyzer.analyze(user_input)
    recommendation = generator.generate_playlist(mood, energy, num_songs=5)
    
    return json.dumps(recommendation, indent=2)


def interactive_mode():
    print("🎵 AI Music Recommendation Engine 🎵")
    print("=" * 50)
    print("\nTell me how you're feeling...")
    print("(Type 'quit' to exit)\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nTake care! 🎶")
                break
            
            if not user_input:
                print("Please share your feelings...\n")
                continue
            
            recommendation = get_music_recommendation(user_input)
            print("\n" + recommendation + "\n")
            
        except KeyboardInterrupt:
            print("\n\nSession ended. See you next time! 🎵")
            break
        except Exception as e:
            print(f"An error occurred: {e}\n")


def main():
    import sys
    
    if len(sys.argv) > 1:
        user_input = ' '.join(sys.argv[1:])
        print(get_music_recommendation(user_input))
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
