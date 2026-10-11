"""
High-EQ Conversational Reasoning Engine.
Generates context-aware, witty, casual Hinglish dialogue with:
- Dynamic intent and topic recognition
- Anti-repetition state machine (tracks asked topics to prevent circular conversation)
- Subject profile adaptation (college, gaming, food, regional references)
- Fallback escalation to maintain conversational momentum
"""

import re
import random

class ConversationalEngine:
    def __init__(self, target_name="Krupali", profile=None):
        self.target_name = target_name
        self.profile = profile
        self.asked_topics = set()
        self.turn_count = 0

    def generate_reply(self, latest_message, history=None):
        """
        Generates a witty, empathetic, and natural Hinglish reply.
        Ensures questions are not repeated and flow matches the target's tone.
        """
        t = latest_message.lower().strip()
        self.turn_count += 1

        # 1. City / Hometown / Travel
        if any(w in t for w in ["surat"]):
            if "surat_food" not in self.asked_topics:
                self.asked_topics.add("surat_food")
                return "Surat! Locho aur cold coco capital haha. Waise hostel mess me survive kaise kar rahi ho fir? Weekend pe seedha ghar bhagti ho kya?"
            elif "surat_travel" not in self.asked_topics:
                self.asked_topics.add("surat_travel")
                return "Surat to Changa travel me hi thakan ho jaati hogi! Vande Bharat ya normal train se travel karti ho?"

        if any(w in t for w in ["ahmedabad", "amdavad"]):
            if "amdavad_commute" not in self.asked_topics:
                self.asked_topics.add("amdavad_commute")
                return "Amdavad! Riverfront aur Manek Chowk vibes haha. Waise daily express se up-down karti ho ya hostel me hi rehti ho?"

        if any(w in t for w in ["vadodara", "baroda"]):
            if "baroda_commute" not in self.asked_topics:
                self.asked_topics.add("baroda_commute")
                return "Baroda to ekdum pass me hai! Fir to aana jana easy rehta hoga ya hostel life chill lag rahi hai abhi?"

        if any(w in t for w in ["gujarat", "gujrat"]):
            if "gujarat_city" not in self.asked_topics:
                self.asked_topics.add("gujarat_city")
                return "Arre sahi hai! Gujarat me konsi city se waise? Ahmedabad, Surat ya Vadodara side?"

        # 2. Hostel Life / Maggi / Roommates
        if any(w in t for w in ["hostel", "room", "bed", "soti"]):
            if "roommate_vibe" not in self.asked_topics:
                self.asked_topics.add("roommate_vibe")
                return "Hostel bed se na uthna is universal student rule haha! Waise roommates kaise mile hain? Chill hain ya study nerd types jo lights off nahi karne dete?"
            elif "hostel_mess" not in self.asked_topics:
                self.asked_topics.add("hostel_mess")
                return "Hostel life me mess ka khana kitne din jhel paayi? Roz bahar se order chal raha hai ya mess pe survive kar rahi ho haha?"

        if any(w in t for w in ["maggie", "maggi", "roommate", "roommates"]):
            if "maggi_chef" not in self.asked_topics:
                self.asked_topics.add("maggi_chef")
                return "Hann Maggi is official student fuel haha! Waise kettle me banati ho ya induction rakha hua hai chupke se?"

        if any(w in t for w in ["cold coco", "coco", "locho"]):
            if "coco_debate" not in self.asked_topics:
                self.asked_topics.add("coco_debate")
                return "Cold coco to pure bliss hai! A.One wala ya koi specific cafe pasand hai Surat me?"

        # 3. Free Fire / Gaming Modes & Weapons
        if any(w in t for w in ["clash squad", "cs"]):
            if "cs_weapons" not in self.asked_topics:
                self.asked_topics.add("cs_weapons")
                return "Clash Squad me to short-range rush karne me hi maza hai! MP40 use karti ho ya shotgun?"
            elif "cs_rank" not in self.asked_topics:
                self.asked_topics.add("cs_rank")
                return "Clash Squad me Heroic pahuchna asaan hota hai Battle Royale ke comparison me! Squad me tumhara kya role hota hai?"

        if any(w in t for w in ["battle royale", "br"]):
            if "br_tactics" not in self.asked_topics:
                self.asked_topics.add("br_tactics")
                return "BR me survival pro max! Aakhri circle tak camping karti ho ya pehle hi rush karke knock ho jaati ho haha?"

        if any(w in t for w in ["mp40", "shotgun", "sniper", "awm"]):
            if "gun_choice" not in self.asked_topics:
                self.asked_topics.add("gun_choice")
                return "Arre lethal choice haha! Headshot lagte hain ya bas spray and pray chalta hai?"

        if any(w in t for w in ["rank", "heroic", "platinum", "gold", "diamond"]):
            if "rank_rant" not in self.asked_topics:
                self.asked_topics.add("rank_rant")
                return "Haha rank push me sabse dukh tab hota hai jab minus 40 lagta hai! Squad me carry kon karta hai waise?"

        if any(w in t for w in ["free fire", "ff", "game", "khel"]):
            if "ff_routine" not in self.asked_topics:
                self.asked_topics.add("ff_routine")
                return "Free Fire me rank kya chal raha hai waise abhi? Platinum ya Heroic pahuch gayi squad ke sath?"

        # 4. Web Series / Entertainment / Chill
        if any(w in t for w in ["thriller", "comedy", "suspense"]):
            if "show_recs" not in self.asked_topics:
                self.asked_topics.add("show_recs")
                return "Thriller + Comedy is elite taste haha! Stree 2 dekhi ya koi mystery series like Stranger Things ya Asur?"
            elif "hindi_vs_eng" not in self.asked_topics:
                self.asked_topics.add("hindi_vs_eng")
                return "Bollywood/desi thrillers pasand hain ya Korean/English shows?"

        if any(w in t for w in ["series", "netflix", "web series", "movie"]):
            if "series_binge" not in self.asked_topics:
                self.asked_topics.add("series_binge")
                return "Binge watch karne baitho toh subah kab ho jaati hai pata hi nahi chalta haha! Last time konsa show pura khatam kiya tha?"

        if any(w in t for w in ["sona", "sleep", "so jati", "neend"]):
            if "sleep_schedule" not in self.asked_topics:
                self.asked_topics.add("sleep_schedule")
                return "Sona to birthright hai student ka haha! Weekend pe 12 baje se pehle uthne ka record hai kabhi?"

        # 5. Studies / CSE / Coding
        if any(w in t for w in ["pointer", "c++", "cpp", "javascript", "coding", "code", "dsa"]):
            if "coding_rant" not in self.asked_topics:
                self.asked_topics.add("coding_rant")
                return "Pointers to teachers ko bhi dhang se samjhate nahi banta haha! Lab practicals me side wale ka code dekh ke submit karne ka scene hai kya?"

        if any(w in t for w in ["exam", "practical", "hackerrank", "assignment"]):
            if "exam_struggle" not in self.asked_topics:
                self.asked_topics.add("exam_struggle")
                return "College practicals me aadhe time compiler hi dhoka deta hai haha! Teachers bohot strict hain kya CHARUSAT me?"

        # 6. Uncertain / Minimal Answers ("Pata nhi", "Hnn", "Haan", "Kuch nhi")
        if any(w in t for w in ["pata nhi", "pata nahi", "dont know", "dk"]):
            options = [
                ("confused_mood", "Haha relatable mood! Kabhi kabhi dimaag blank ho jaata hai. Waise abhi game chal raha hai ya bas screen scroll kar rahi ho?"),
                ("college_fest", "Haha koi na! Waise college me fest ya events kab hain CHARUSAT me? Garba ke alawa kuch exciting hota hai campus me?"),
                ("weekend_vibe", "Haha no stress! Waise weekend pe kya plan rehta hai hostel me? Full bed rot ya friends ke sath outing?")
            ]
            for tag, reply in options:
                if tag not in self.asked_topics:
                    self.asked_topics.add(tag)
                    return reply

        if t in ["hnn", "haan", "ha", "han", "yes", "hmm", "hmmm"]:
            options = [
                ("short_reply_cs", "Haha short reply pro max! Waise Clash Squad me booyah hua abhi ya squad pehle hi nipat gayi?"),
                ("short_reply_music", "Waise background me gaane sunte sunte game khelti ho ya squad ka voice chat full on chalta hai?"),
                ("short_reply_sleep", "Sone ka time ho raha hai ya raat 2-3 baje tak jaagne ka regular schedule hai?")
            ]
            for tag, reply in options:
                if tag not in self.asked_topics:
                    self.asked_topics.add(tag)
                    return reply

        # 7. Dynamic Fresh Topic Pool (Guaranteed Zero Repetition)
        fallback_pool = [
            ("campus_exploration", "Waise CHARUSAT ka campus kaisa lag raha hai? Bohot bada hai bolte hain, classes ke beech me chal chal ke cardio ho jata hoga haha?"),
            ("music_taste", "Waise gaming ke time background me music sunna pasand hai ya squad ka voice chat hi chal raha hota hai?"),
            ("fest_discussion", "College me Spoural ya annual sports fest kab hota hai CHARUSAT me? Participate karne ka plan hai ya bas audience me enjoy?"),
            ("night_owl", "Waise tum morning person ho ya proper night owl jo 3-4 baje sota hai?"),
            ("food_craving", "Hostel me aadhi raat ko sabse zyada kis cheez ki craving hoti hai? Maggie ya kuch spicy junk food?")
        ]

        for tag, reply in fallback_pool:
            if tag not in self.asked_topics:
                self.asked_topics.add(tag)
                return reply

        # Extreme fallback
        return "Haha sahi baat hai! Waise aur batao, college life expectation jaisi hi nikli ya reality thodi alag hai?"
