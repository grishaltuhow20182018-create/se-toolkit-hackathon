"""Seed database with 105 default tracks available to all users."""

import asyncio
from app.core.database import async_session_maker
from app.models.models import Track

DEFAULT_TRACKS = [
    {"title": "Strobe", "artist": "deadmau5", "bpm": 128.0, "key": "8A", "energy_level": 7, "genre": "Progressive House"},
    {"title": "Opus", "artist": "deadmau5", "bpm": 126.0, "key": "12B", "energy_level": 6, "genre": "Progressive House"},
    {"title": "Ghosts 'n' Stuff", "artist": "deadmau5", "bpm": 128.0, "key": "9A", "energy_level": 8, "genre": "Progressive House"},
    {"title": "Raise Your Weapon", "artist": "deadmau5", "bpm": 128.0, "key": "6A", "energy_level": 7, "genre": "Progressive House"},
    {"title": "I Remember", "artist": "deadmau5 & Kaskade", "bpm": 126.0, "key": "11B", "energy_level": 5, "genre": "Progressive House"},
    {"title": "Levels", "artist": "Avicii", "bpm": 126.0, "key": "7A", "energy_level": 8, "genre": "Electro House"},
    {"title": "Animals", "artist": "Martin Garrix", "bpm": 128.0, "key": "8B", "energy_level": 9, "genre": "Electro House"},
    {"title": "Tremor", "artist": "Dimitri Vegas & Like Mike", "bpm": 128.0, "key": "5A", "energy_level": 9, "genre": "Electro House"},
    {"title": "Tsunami", "artist": "DVBBS & Borgeous", "bpm": 128.0, "key": "10A", "energy_level": 9, "genre": "Electro House"},
    {"title": "Wizard", "artist": "Martin Garrix & Jay Hardway", "bpm": 128.0, "key": "11A", "energy_level": 8, "genre": "Electro House"},
    {"title": "Spaceman", "artist": "Hardwell", "bpm": 130.0, "key": "9B", "energy_level": 9, "genre": "Big Room"},
    {"title": "Apollo", "artist": "Hardwell", "bpm": 128.0, "key": "6B", "energy_level": 8, "genre": "Big Room"},
    {"title": "Arcadia", "artist": "Hardwell", "bpm": 128.0, "key": "12A", "energy_level": 9, "genre": "Big Room"},
    {"title": "The Universe", "artist": "W&W", "bpm": 128.0, "key": "7B", "energy_level": 9, "genre": "Big Room"},
    {"title": "Jumper", "artist": "Hardwell & W&W", "bpm": 128.0, "key": "8A", "energy_level": 8, "genre": "Big Room"},
    {"title": "Adagio for Strings", "artist": "Tiësto", "bpm": 138.0, "key": "3A", "energy_level": 7, "genre": "Trance"},
    {"title": "L'Académie", "artist": "Tiësto", "bpm": 136.0, "key": "4B", "energy_level": 6, "genre": "Trance"},
    {"title": "Suburban Train", "artist": "Tiësto", "bpm": 138.0, "key": "1A", "energy_level": 8, "genre": "Trance"},
    {"title": "Silence", "artist": "Delerium ft. Sarah McLachlan", "bpm": 136.0, "key": "5B", "energy_level": 6, "genre": "Trance"},
    {"title": "For an Angel", "artist": "Paul van Dyk", "bpm": 138.0, "key": "6A", "energy_level": 7, "genre": "Trance"},
    {"title": "Cola", "artist": "CamelPhat & Elderbrook", "bpm": 122.0, "key": "9A", "energy_level": 6, "genre": "Deep House"},
    {"title": "My Feelings for You", "artist": "Avicii", "bpm": 124.0, "key": "10B", "energy_level": 5, "genre": "Deep House"},
    {"title": "Needin' U", "artist": "David Morales", "bpm": 124.0, "key": "11A", "energy_level": 5, "genre": "Deep House"},
    {"title": "Show Me Love", "artist": "Robin S.", "bpm": 122.0, "key": "8B", "energy_level": 6, "genre": "Deep House"},
    {"title": "Finally", "artist": "CeCe Peniston", "bpm": 122.0, "key": "12A", "energy_level": 6, "genre": "Deep House"},
    {"title": "Losing It", "artist": "Fisher", "bpm": 125.0, "key": "7A", "energy_level": 8, "genre": "Tech House"},
    {"title": "It's a Killa", "artist": "Fisher", "bpm": 126.0, "key": "6B", "energy_level": 8, "genre": "Tech House"},
    {"title": "You Little Beauty", "artist": "Fisher", "bpm": 125.0, "key": "5A", "energy_level": 7, "genre": "Tech House"},
    {"title": "Pump It Up", "artist": "Endor", "bpm": 124.0, "key": "8A", "energy_level": 7, "genre": "Tech House"},
    {"title": "Body Moving", "artist": "Sonny Fodera", "bpm": 123.0, "key": "10A", "energy_level": 6, "genre": "Tech House"},
    {"title": "Spastik", "artist": "Plastikman", "bpm": 132.0, "key": "4A", "energy_level": 8, "genre": "Techno"},
    {"title": "Strings of Life", "artist": "Derrick May", "bpm": 130.0, "key": "6A", "energy_level": 7, "genre": "Techno"},
    {"title": "Energy Flash", "artist": "Joey Beltram", "bpm": 130.0, "key": "9B", "energy_level": 8, "genre": "Techno"},
    {"title": "The Bells", "artist": "Jeff Mills", "bpm": 135.0, "key": "11A", "energy_level": 9, "genre": "Techno"},
    {"title": "Acid Tracks", "artist": "Phuture", "bpm": 122.0, "key": "7A", "energy_level": 7, "genre": "Techno"},
    {"title": "Inner City Life", "artist": "Goldie", "bpm": 174.0, "key": "5A", "energy_level": 7, "genre": "Drum & Bass"},
    {"title": "Tarantula", "artist": "Pendulum", "bpm": 174.0, "key": "8A", "energy_level": 9, "genre": "Drum & Bass"},
    {"title": "Propane Nightmares", "artist": "Pendulum", "bpm": 174.0, "key": "6B", "energy_level": 9, "genre": "Drum & Bass"},
    {"title": "Witchcraft", "artist": "Pendulum", "bpm": 174.0, "key": "10A", "energy_level": 8, "genre": "Drum & Bass"},
    {"title": "Valley of the Shadows", "artist": "Origin Unknown", "bpm": 172.0, "key": "3A", "energy_level": 8, "genre": "Drum & Bass"},
    {"title": "Scary Monsters and Nice Sprites", "artist": "Skrillex", "bpm": 140.0, "key": "9A", "energy_level": 9, "genre": "Dubstep"},
    {"title": "Bangarang", "artist": "Skrillex", "bpm": 110.0, "key": "7B", "energy_level": 9, "genre": "Dubstep"},
    {"title": "Centipede", "artist": "Knife Party", "bpm": 140.0, "key": "5A", "energy_level": 10, "genre": "Dubstep"},
    {"title": "Internet Friends", "artist": "Knife Party", "bpm": 140.0, "key": "11A", "energy_level": 9, "genre": "Dubstep"},
    {"title": "Midnight City", "artist": "M83 (Skrillex Remix)", "bpm": 140.0, "key": "12B", "energy_level": 7, "genre": "Dubstep"},
    {"title": "Say My Name", "artist": "ODESZA", "bpm": 150.0, "key": "6B", "energy_level": 6, "genre": "Future Bass"},
    {"title": "Sun Models", "artist": "ODESZA", "bpm": 140.0, "key": "8B", "energy_level": 5, "genre": "Future Bass"},
    {"title": "A Moment Apart", "artist": "ODESZA", "bpm": 136.0, "key": "10B", "energy_level": 5, "genre": "Future Bass"},
    {"title": "Divinity", "artist": "Porter Robinson", "bpm": 145.0, "key": "4B", "energy_level": 6, "genre": "Future Bass"},
    {"title": "Language", "artist": "Porter Robinson", "bpm": 128.0, "key": "11B", "energy_level": 8, "genre": "Future Bass"},
    {"title": "Shelter", "artist": "Porter Robinson & Madeon", "bpm": 120.0, "key": "7B", "energy_level": 5, "genre": "Melodic Dubstep"},
    {"title": "All My Friends", "artist": "ODESZA", "bpm": 144.0, "key": "3B", "energy_level": 6, "genre": "Melodic Dubstep"},
    {"title": "Higher Ground", "artist": "ODESZA", "bpm": 140.0, "key": "9B", "energy_level": 7, "genre": "Melodic Dubstep"},
    {"title": "Bloom", "artist": "ODESZA", "bpm": 120.0, "key": "12B", "energy_level": 5, "genre": "Melodic Dubstep"},
    {"title": "Kusanagi", "artist": "San Holo", "bpm": 150.0, "key": "5B", "energy_level": 6, "genre": "Melodic Dubstep"},
    {"title": "Our Destiny", "artist": "Headhunterz", "bpm": 150.0, "key": "7A", "energy_level": 9, "genre": "Hardstyle"},
    {"title": "The Sacrifice", "artist": "Headhunterz", "bpm": 150.0, "key": "6A", "energy_level": 9, "genre": "Hardstyle"},
    {"title": "The Power of the Mind", "artist": "Headhunterz", "bpm": 150.0, "key": "10A", "energy_level": 9, "genre": "Hardstyle"},
    {"title": "D.I.S.C.O.", "artist": "Headhunterz", "bpm": 150.0, "key": "9B", "energy_level": 8, "genre": "Hardstyle"},
    {"title": "The Return", "artist": "Noisecontrollers", "bpm": 150.0, "key": "8A", "energy_level": 9, "genre": "Hardstyle"},
    {"title": "Rewind", "artist": "Craig David", "bpm": 134.0, "key": "4A", "energy_level": 5, "genre": "UK Garage"},
    {"title": "7 Days", "artist": "Craig David", "bpm": 132.0, "key": "8B", "energy_level": 5, "genre": "UK Garage"},
    {"title": "Fill Me In", "artist": "Craig David", "bpm": 134.0, "key": "6B", "energy_level": 6, "genre": "UK Garage"},
    {"title": "Flowers", "artist": "Sweet Female Attitude", "bpm": 134.0, "key": "10B", "energy_level": 6, "genre": "UK Garage"},
    {"title": "Sincerely", "artist": "MJ Cole", "bpm": 132.0, "key": "3A", "energy_level": 5, "genre": "UK Garage"},
    {"title": "Firestarter", "artist": "The Prodigy", "bpm": 135.0, "key": "9A", "energy_level": 9, "genre": "Breakbeat"},
    {"title": "Breathe", "artist": "The Prodigy", "bpm": 134.0, "key": "7A", "energy_level": 9, "genre": "Breakbeat"},
    {"title": "Smack My Bitch Up", "artist": "The Prodigy", "bpm": 136.0, "key": "5A", "energy_level": 10, "genre": "Breakbeat"},
    {"title": "Omen", "artist": "The Prodigy", "bpm": 138.0, "key": "11A", "energy_level": 9, "genre": "Breakbeat"},
    {"title": "Voodoo People", "artist": "The Prodigy", "bpm": 140.0, "key": "8A", "energy_level": 8, "genre": "Breakbeat"},
    {"title": "Move", "artist": "Black Coffee", "bpm": 120.0, "key": "6A", "energy_level": 5, "genre": "Afro House"},
    {"title": "Superman", "artist": "Black Coffee", "bpm": 122.0, "key": "9B", "energy_level": 6, "genre": "Afro House"},
    {"title": "Drive", "artist": "Black Coffee", "bpm": 118.0, "key": "11A", "energy_level": 5, "genre": "Afro House"},
    {"title": "We Dance Again", "artist": "Black Coffee", "bpm": 120.0, "key": "4A", "energy_level": 6, "genre": "Afro House"},
    {"title": "Your Eyes", "artist": "Black Coffee", "bpm": 122.0, "key": "8A", "energy_level": 5, "genre": "Afro House"},
    {"title": "Tongue", "artist": "Molchat Doma", "bpm": 130.0, "key": "7A", "energy_level": 6, "genre": "Indie Dance"},
    {"title": "Sudno", "artist": "Molchat Doma", "bpm": 128.0, "key": "5A", "energy_level": 6, "genre": "Indie Dance"},
    {"title": "Na Dne", "artist": "Molchat Doma", "bpm": 126.0, "key": "10A", "energy_level": 5, "genre": "Indie Dance"},
    {"title": "Let's Go Swimming", "artist": "Hot Since 82", "bpm": 124.0, "key": "8B", "energy_level": 7, "genre": "Indie Dance"},
    {"title": "In the Air", "artist": "Morgan Page", "bpm": 128.0, "key": "12B", "energy_level": 7, "genre": "Indie Dance"},
    {"title": "Weightless", "artist": "Marconi Union", "bpm": 60.0, "key": "3B", "energy_level": 1, "genre": "Ambient"},
    {"title": "An Ending (Ascent)", "artist": "Brian Eno", "bpm": 70.0, "key": "5B", "energy_level": 2, "genre": "Ambient"},
    {"title": "Selected Ambient Works", "artist": "Aphex Twin", "bpm": 110.0, "key": "7B", "energy_level": 3, "genre": "Ambient"},
    {"title": "Rhubarb", "artist": "Aphex Twin", "bpm": 90.0, "key": "9B", "energy_level": 2, "genre": "Ambient"},
    {"title": "Avril 14th", "artist": "Aphex Twin", "bpm": 94.0, "key": "11B", "energy_level": 2, "genre": "Ambient"},
    {"title": "On a Good Day", "artist": "Above & Beyond", "bpm": 132.0, "key": "4B", "energy_level": 7, "genre": "Vocal Trance"},
    {"title": "Sun & Moon", "artist": "Above & Beyond", "bpm": 132.0, "key": "6B", "energy_level": 8, "genre": "Vocal Trance"},
    {"title": "Thing Called Love", "artist": "Above & Beyond", "bpm": 132.0, "key": "8B", "energy_level": 7, "genre": "Vocal Trance"},
    {"title": "Concrete Angel", "artist": "Gareth Emery", "bpm": 132.0, "key": "10B", "energy_level": 7, "genre": "Vocal Trance"},
    {"title": "Eternal", "artist": "Gareth Emery", "bpm": 134.0, "key": "12A", "energy_level": 8, "genre": "Vocal Trance"},
    {"title": "Shpongle", "artist": "Shpongle", "bpm": 145.0, "key": "3A", "energy_level": 8, "genre": "Psytrance"},
    {"title": "Dorset Perception", "artist": "Shpongle", "bpm": 142.0, "key": "5A", "energy_level": 7, "genre": "Psytrance"},
    {"title": "Tales of the Inexpressible", "artist": "Shpongle", "bpm": 140.0, "key": "7A", "energy_level": 7, "genre": "Psytrance"},
    {"title": "Vicious Delicious", "artist": "Infected Mushroom", "bpm": 148.0, "key": "9A", "energy_level": 9, "genre": "Psytrance"},
    {"title": "Becoming Insane", "artist": "Infected Mushroom", "bpm": 142.0, "key": "11A", "energy_level": 8, "genre": "Psytrance"},
    {"title": "One More Time", "artist": "Daft Punk", "bpm": 123.0, "key": "11A", "energy_level": 7, "genre": "House"},
    {"title": "Around the World", "artist": "Daft Punk", "bpm": 121.0, "key": "6A", "energy_level": 6, "genre": "House"},
    {"title": "Harder Better Faster Stronger", "artist": "Daft Punk", "bpm": 123.0, "key": "9A", "energy_level": 7, "genre": "House"},
    {"title": "Music Sounds Better with You", "artist": "Stardust", "bpm": 123.0, "key": "7B", "energy_level": 7, "genre": "House"},
    {"title": "Gypsy Woman", "artist": "Crystal Waters", "bpm": 120.0, "key": "8B", "energy_level": 6, "genre": "House"},
    {"title": "Titanium", "artist": "David Guetta ft. Sia", "bpm": 126.0, "key": "10A", "energy_level": 8, "genre": "Dance"},
    {"title": "Where Them Girls At", "artist": "David Guetta", "bpm": 128.0, "key": "8A", "energy_level": 8, "genre": "Dance"},
    {"title": "Without You", "artist": "David Guetta ft. Usher", "bpm": 128.0, "key": "6B", "energy_level": 7, "genre": "Dance"},
    {"title": "Wake Me Up", "artist": "Avicii", "bpm": 124.0, "key": "11B", "energy_level": 7, "genre": "Dance"},
    {"title": "Hey Brother", "artist": "Avicii", "bpm": 125.0, "key": "4A", "energy_level": 6, "genre": "Dance"},
    {"title": "Waiting for Love", "artist": "Avicii", "bpm": 128.0, "key": "9A", "energy_level": 7, "genre": "Dance"},
    {"title": "The Nights", "artist": "Avicii", "bpm": 126.0, "key": "7B", "energy_level": 7, "genre": "Dance"},
    {"title": "Don't You Worry Child", "artist": "Swedish House Mafia", "bpm": 129.0, "key": "10A", "energy_level": 8, "genre": "Dance"},
    {"title": "Save the World", "artist": "Swedish House Mafia", "bpm": 128.0, "key": "6B", "energy_level": 8, "genre": "Dance"},
    {"title": "Greyhound", "artist": "Swedish House Mafia", "bpm": 128.0, "key": "5A", "energy_level": 9, "genre": "Dance"},
]

SYSTEM_USER_ID = "00000000-0000-0000-0000-000000000000"


async def seed_tracks():
    """Seed default tracks if the table is empty."""
    async with async_session_maker() as session:
        from sqlalchemy import select
        
        result = await session.execute(select(Track))
        existing = result.scalars().all()
        
        if len(existing) >= len(DEFAULT_TRACKS):
            print(f"[seed] Already have {len(existing)} tracks, skipping.")
            return
        
        for track_data in DEFAULT_TRACKS:
            track = Track(user_id=SYSTEM_USER_ID, **track_data)
            session.add(track)
        
        await session.commit()
        print(f"[seed] Added {len(DEFAULT_TRACKS)} tracks to the database.")


if __name__ == "__main__":
    asyncio.run(seed_tracks())
