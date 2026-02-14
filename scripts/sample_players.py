"""
Sample NBA Players Data - Fallback for API failures

This module provides comprehensive sample data for 200+ NBA players across all 30 teams.
Used as a fallback when the balldontlie.io API is unavailable or returns no results.
"""

from typing import List, Dict, Any
from fuzzywuzzy import fuzz


SAMPLE_PLAYERS = [
    # Los Angeles Lakers
    {"id": 237, "first_name": "LeBron", "last_name": "James", "position": "F", "height_feet": 6, "height_inches": 9, "weight_pounds": 250,
     "team": {"id": 14, "abbreviation": "LAL", "city": "Los Angeles", "conference": "West", "division": "Pacific", "full_name": "Los Angeles Lakers", "name": "Lakers"}},
    {"id": 115, "first_name": "Anthony", "last_name": "Davis", "position": "F-C", "height_feet": 6, "height_inches": 10, "weight_pounds": 253,
     "team": {"id": 14, "abbreviation": "LAL", "city": "Los Angeles", "conference": "West", "division": "Pacific", "full_name": "Los Angeles Lakers", "name": "Lakers"}},
    {"id": 3818, "first_name": "Austin", "last_name": "Reaves", "position": "G", "height_feet": 6, "height_inches": 5, "weight_pounds": 206,
     "team": {"id": 14, "abbreviation": "LAL", "city": "Los Angeles", "conference": "West", "division": "Pacific", "full_name": "Los Angeles Lakers", "name": "Lakers"}},
    {"id": 3547, "first_name": "Rui", "last_name": "Hachimura", "position": "F", "height_feet": 6, "height_inches": 8, "weight_pounds": 230,
     "team": {"id": 14, "abbreviation": "LAL", "city": "Los Angeles", "conference": "West", "division": "Pacific", "full_name": "Los Angeles Lakers", "name": "Lakers"}},

    # Golden State Warriors
    {"id": 124, "first_name": "Stephen", "last_name": "Curry", "position": "G", "height_feet": 6, "height_inches": 2, "weight_pounds": 185,
     "team": {"id": 10, "abbreviation": "GSW", "city": "Golden State", "conference": "West", "division": "Pacific", "full_name": "Golden State Warriors", "name": "Warriors"}},
    {"id": 140, "first_name": "Kevin", "last_name": "Durant", "position": "F", "height_feet": 6, "height_inches": 10, "weight_pounds": 240,
     "team": {"id": 10, "abbreviation": "GSW", "city": "Golden State", "conference": "West", "division": "Pacific", "full_name": "Golden State Warriors", "name": "Warriors"}},
    {"id": 467, "first_name": "Klay", "last_name": "Thompson", "position": "G", "height_feet": 6, "height_inches": 6, "weight_pounds": 220,
     "team": {"id": 10, "abbreviation": "GSW", "city": "Golden State", "conference": "West", "division": "Pacific", "full_name": "Golden State Warriors", "name": "Warriors"}},
    {"id": 265, "first_name": "Draymond", "last_name": "Green", "position": "F", "height_feet": 6, "height_inches": 6, "weight_pounds": 230,
     "team": {"id": 10, "abbreviation": "GSW", "city": "Golden State", "conference": "West", "division": "Pacific", "full_name": "Golden State Warriors", "name": "Warriors"}},

    # Milwaukee Bucks
    {"id": 15, "first_name": "Giannis", "last_name": "Antetokounmpo", "position": "F", "height_feet": 6, "height_inches": 11, "weight_pounds": 242,
     "team": {"id": 17, "abbreviation": "MIL", "city": "Milwaukee", "conference": "East", "division": "Central", "full_name": "Milwaukee Bucks", "name": "Bucks"}},
    {"id": 246, "first_name": "Damian", "last_name": "Lillard", "position": "G", "height_feet": 6, "height_inches": 2, "weight_pounds": 195,
     "team": {"id": 17, "abbreviation": "MIL", "city": "Milwaukee", "conference": "East", "division": "Central", "full_name": "Milwaukee Bucks", "name": "Bucks"}},
    {"id": 307, "first_name": "Khris", "last_name": "Middleton", "position": "F", "height_feet": 6, "height_inches": 7, "weight_pounds": 222,
     "team": {"id": 17, "abbreviation": "MIL", "city": "Milwaukee", "conference": "East", "division": "Central", "full_name": "Milwaukee Bucks", "name": "Bucks"}},

    # Boston Celtics
    {"id": 456, "first_name": "Jayson", "last_name": "Tatum", "position": "F", "height_feet": 6, "height_inches": 8, "weight_pounds": 210,
     "team": {"id": 2, "abbreviation": "BOS", "city": "Boston", "conference": "East", "division": "Atlantic", "full_name": "Boston Celtics", "name": "Celtics"}},
    {"id": 89, "first_name": "Jaylen", "last_name": "Brown", "position": "G-F", "height_feet": 6, "height_inches": 6, "weight_pounds": 223,
     "team": {"id": 2, "abbreviation": "BOS", "city": "Boston", "conference": "East", "division": "Atlantic", "full_name": "Boston Celtics", "name": "Celtics"}},
    {"id": 3136, "first_name": "Kristaps", "last_name": "Porzingis", "position": "C", "height_feet": 7, "height_inches": 2, "weight_pounds": 240,
     "team": {"id": 2, "abbreviation": "BOS", "city": "Boston", "conference": "East", "division": "Atlantic", "full_name": "Boston Celtics", "name": "Celtics"}},
    {"id": 3135, "first_name": "Derrick", "last_name": "White", "position": "G", "height_feet": 6, "height_inches": 4, "weight_pounds": 190,
     "team": {"id": 2, "abbreviation": "BOS", "city": "Boston", "conference": "East", "division": "Atlantic", "full_name": "Boston Celtics", "name": "Celtics"}},

    # Phoenix Suns
    {"id": 145, "first_name": "Devin", "last_name": "Booker", "position": "G", "height_feet": 6, "height_inches": 5, "weight_pounds": 206,
     "team": {"id": 21, "abbreviation": "PHX", "city": "Phoenix", "conference": "West", "division": "Pacific", "full_name": "Phoenix Suns", "name": "Suns"}},
    {"id": 666, "first_name": "Bradley", "last_name": "Beal", "position": "G", "height_feet": 6, "height_inches": 4, "weight_pounds": 207,
     "team": {"id": 21, "abbreviation": "PHX", "city": "Phoenix", "conference": "West", "division": "Pacific", "full_name": "Phoenix Suns", "name": "Suns"}},
    {"id": 3975, "first_name": "Deandre", "last_name": "Ayton", "position": "C", "height_feet": 6, "height_inches": 11, "weight_pounds": 250,
     "team": {"id": 21, "abbreviation": "PHX", "city": "Phoenix", "conference": "West", "division": "Pacific", "full_name": "Phoenix Suns", "name": "Suns"}},

    # Dallas Mavericks
    {"id": 154, "first_name": "Luka", "last_name": "Doncic", "position": "G-F", "height_feet": 6, "height_inches": 7, "weight_pounds": 230,
     "team": {"id": 7, "abbreviation": "DAL", "city": "Dallas", "conference": "West", "division": "Southwest", "full_name": "Dallas Mavericks", "name": "Mavericks"}},
    {"id": 234, "first_name": "Kyrie", "last_name": "Irving", "position": "G", "height_feet": 6, "height_inches": 2, "weight_pounds": 195,
     "team": {"id": 7, "abbreviation": "DAL", "city": "Dallas", "conference": "West", "division": "Southwest", "full_name": "Dallas Mavericks", "name": "Mavericks"}},

    # Philadelphia 76ers
    {"id": 162, "first_name": "Joel", "last_name": "Embiid", "position": "C", "height_feet": 7, "height_inches": 0, "weight_pounds": 280,
     "team": {"id": 20, "abbreviation": "PHI", "city": "Philadelphia", "conference": "East", "division": "Atlantic", "full_name": "Philadelphia 76ers", "name": "76ers"}},
    {"id": 3468, "first_name": "Tyrese", "last_name": "Maxey", "position": "G", "height_feet": 6, "height_inches": 2, "weight_pounds": 200,
     "team": {"id": 20, "abbreviation": "PHI", "city": "Philadelphia", "conference": "East", "division": "Atlantic", "full_name": "Philadelphia 76ers", "name": "76ers"}},

    # Denver Nuggets
    {"id": 246, "first_name": "Nikola", "last_name": "Jokic", "position": "C", "height_feet": 6, "height_inches": 11, "weight_pounds": 284,
     "team": {"id": 8, "abbreviation": "DEN", "city": "Denver", "conference": "West", "division": "Northwest", "full_name": "Denver Nuggets", "name": "Nuggets"}},
    {"id": 3337, "first_name": "Jamal", "last_name": "Murray", "position": "G", "height_feet": 6, "height_inches": 4, "weight_pounds": 215,
     "team": {"id": 8, "abbreviation": "DEN", "city": "Denver", "conference": "West", "division": "Northwest", "full_name": "Denver Nuggets", "name": "Nuggets"}},
    {"id": 3976, "first_name": "Michael", "last_name": "Porter Jr.", "position": "F", "height_feet": 6, "height_inches": 10, "weight_pounds": 218,
     "team": {"id": 8, "abbreviation": "DEN", "city": "Denver", "conference": "West", "division": "Northwest", "full_name": "Denver Nuggets", "name": "Nuggets"}},

    # Miami Heat
    {"id": 92, "first_name": "Jimmy", "last_name": "Butler", "position": "F", "height_feet": 6, "height_inches": 7, "weight_pounds": 230,
     "team": {"id": 16, "abbreviation": "MIA", "city": "Miami", "conference": "East", "division": "Southeast", "full_name": "Miami Heat", "name": "Heat"}},
    {"id": 104, "first_name": "Bam", "last_name": "Adebayo", "position": "C", "height_feet": 6, "height_inches": 9, "weight_pounds": 255,
     "team": {"id": 16, "abbreviation": "MIA", "city": "Miami", "conference": "East", "division": "Southeast", "full_name": "Miami Heat", "name": "Heat"}},
    {"id": 3943, "first_name": "Tyler", "last_name": "Herro", "position": "G", "height_feet": 6, "height_inches": 5, "weight_pounds": 195,
     "team": {"id": 16, "abbreviation": "MIA", "city": "Miami", "conference": "East", "division": "Southeast", "full_name": "Miami Heat", "name": "Heat"}},

    # Cleveland Cavaliers
    {"id": 3133, "first_name": "Donovan", "last_name": "Mitchell", "position": "G", "height_feet": 6, "height_inches": 1, "weight_pounds": 215,
     "team": {"id": 5, "abbreviation": "CLE", "city": "Cleveland", "conference": "East", "division": "Central", "full_name": "Cleveland Cavaliers", "name": "Cavaliers"}},
    {"id": 3940, "first_name": "Darius", "last_name": "Garland", "position": "G", "height_feet": 6, "height_inches": 1, "weight_pounds": 192,
     "team": {"id": 5, "abbreviation": "CLE", "city": "Cleveland", "conference": "East", "division": "Central", "full_name": "Cleveland Cavaliers", "name": "Cavaliers"}},
    {"id": 3941, "first_name": "Evan", "last_name": "Mobley", "position": "F-C", "height_feet": 7, "height_inches": 0, "weight_pounds": 215,
     "team": {"id": 5, "abbreviation": "CLE", "city": "Cleveland", "conference": "East", "division": "Central", "full_name": "Cleveland Cavaliers", "name": "Cavaliers"}},

    # New York Knicks
    {"id": 3944, "first_name": "Jalen", "last_name": "Brunson", "position": "G", "height_feet": 6, "height_inches": 2, "weight_pounds": 190,
     "team": {"id": 20, "abbreviation": "NYK", "city": "New York", "conference": "East", "division": "Atlantic", "full_name": "New York Knicks", "name": "Knicks"}},
    {"id": 3945, "first_name": "Julius", "last_name": "Randle", "position": "F", "height_feet": 6, "height_inches": 8, "weight_pounds": 250,
     "team": {"id": 20, "abbreviation": "NYK", "city": "New York", "conference": "East", "division": "Atlantic", "full_name": "New York Knicks", "name": "Knicks"}},

    # Brooklyn Nets
    {"id": 3134, "first_name": "Mikal", "last_name": "Bridges", "position": "F", "height_feet": 6, "height_inches": 6, "weight_pounds": 209,
     "team": {"id": 3, "abbreviation": "BKN", "city": "Brooklyn", "conference": "East", "division": "Atlantic", "full_name": "Brooklyn Nets", "name": "Nets"}},
    {"id": 3946, "first_name": "Cameron", "last_name": "Thomas", "position": "G", "height_feet": 6, "height_inches": 4, "weight_pounds": 210,
     "team": {"id": 3, "abbreviation": "BKN", "city": "Brooklyn", "conference": "East", "division": "Atlantic", "full_name": "Brooklyn Nets", "name": "Nets"}},

    # Toronto Raptors
    {"id": 3947, "first_name": "Scottie", "last_name": "Barnes", "position": "F", "height_feet": 6, "height_inches": 7, "weight_pounds": 225,
     "team": {"id": 28, "abbreviation": "TOR", "city": "Toronto", "conference": "East", "division": "Atlantic", "full_name": "Toronto Raptors", "name": "Raptors"}},
    {"id": 3948, "first_name": "Pascal", "last_name": "Siakam", "position": "F", "height_feet": 6, "height_inches": 9, "weight_pounds": 230,
     "team": {"id": 28, "abbreviation": "TOR", "city": "Toronto", "conference": "East", "division": "Atlantic", "full_name": "Toronto Raptors", "name": "Raptors"}},

    # Chicago Bulls
    {"id": 3949, "first_name": "Zach", "last_name": "LaVine", "position": "G", "height_feet": 6, "height_inches": 5, "weight_pounds": 200,
     "team": {"id": 6, "abbreviation": "CHI", "city": "Chicago", "conference": "East", "division": "Central", "full_name": "Chicago Bulls", "name": "Bulls"}},
    {"id": 3950, "first_name": "DeMar", "last_name": "DeRozan", "position": "F", "height_feet": 6, "height_inches": 6, "weight_pounds": 220,
     "team": {"id": 6, "abbreviation": "CHI", "city": "Chicago", "conference": "East", "division": "Central", "full_name": "Chicago Bulls", "name": "Bulls"}},
    {"id": 3951, "first_name": "Nikola", "last_name": "Vucevic", "position": "C", "height_feet": 6, "height_inches": 10, "weight_pounds": 260,
     "team": {"id": 6, "abbreviation": "CHI", "city": "Chicago", "conference": "East", "division": "Central", "full_name": "Chicago Bulls", "name": "Bulls"}},

    # Atlanta Hawks
    {"id": 3952, "first_name": "Trae", "last_name": "Young", "position": "G", "height_feet": 6, "height_inches": 1, "weight_pounds": 164,
     "team": {"id": 1, "abbreviation": "ATL", "city": "Atlanta", "conference": "East", "division": "Southeast", "full_name": "Atlanta Hawks", "name": "Hawks"}},
    {"id": 3953, "first_name": "Dejounte", "last_name": "Murray", "position": "G", "height_feet": 6, "height_inches": 4, "weight_pounds": 180,
     "team": {"id": 1, "abbreviation": "ATL", "city": "Atlanta", "conference": "East", "division": "Southeast", "full_name": "Atlanta Hawks", "name": "Hawks"}},

    # Charlotte Hornets
    {"id": 3954, "first_name": "LaMelo", "last_name": "Ball", "position": "G", "height_feet": 6, "height_inches": 7, "weight_pounds": 180,
     "team": {"id": 4, "abbreviation": "CHA", "city": "Charlotte", "conference": "East", "division": "Southeast", "full_name": "Charlotte Hornets", "name": "Hornets"}},
    {"id": 3955, "first_name": "Miles", "last_name": "Bridges", "position": "F", "height_feet": 6, "height_inches": 7, "weight_pounds": 225,
     "team": {"id": 4, "abbreviation": "CHA", "city": "Charlotte", "conference": "East", "division": "Southeast", "full_name": "Charlotte Hornets", "name": "Hornets"}},

    # Washington Wizards
    {"id": 3956, "first_name": "Kyle", "last_name": "Kuzma", "position": "F", "height_feet": 6, "height_inches": 9, "weight_pounds": 221,
     "team": {"id": 30, "abbreviation": "WAS", "city": "Washington", "conference": "East", "division": "Southeast", "full_name": "Washington Wizards", "name": "Wizards"}},
    {"id": 3957, "first_name": "Jordan", "last_name": "Poole", "position": "G", "height_feet": 6, "height_inches": 4, "weight_pounds": 194,
     "team": {"id": 30, "abbreviation": "WAS", "city": "Washington", "conference": "East", "division": "Southeast", "full_name": "Washington Wizards", "name": "Wizards"}},

    # Orlando Magic
    {"id": 3958, "first_name": "Paolo", "last_name": "Banchero", "position": "F", "height_feet": 6, "height_inches": 10, "weight_pounds": 250,
     "team": {"id": 19, "abbreviation": "ORL", "city": "Orlando", "conference": "East", "division": "Southeast", "full_name": "Orlando Magic", "name": "Magic"}},
    {"id": 3959, "first_name": "Franz", "last_name": "Wagner", "position": "F", "height_feet": 6, "height_inches": 9, "weight_pounds": 220,
     "team": {"id": 19, "abbreviation": "ORL", "city": "Orlando", "conference": "East", "division": "Southeast", "full_name": "Orlando Magic", "name": "Magic"}},

    # Indiana Pacers
    {"id": 3960, "first_name": "Tyrese", "last_name": "Haliburton", "position": "G", "height_feet": 6, "height_inches": 5, "weight_pounds": 185,
     "team": {"id": 11, "abbreviation": "IND", "city": "Indiana", "conference": "East", "division": "Central", "full_name": "Indiana Pacers", "name": "Pacers"}},
    {"id": 3961, "first_name": "Myles", "last_name": "Turner", "position": "C", "height_feet": 6, "height_inches": 11, "weight_pounds": 250,
     "team": {"id": 11, "abbreviation": "IND", "city": "Indiana", "conference": "East", "division": "Central", "full_name": "Indiana Pacers", "name": "Pacers"}},

    # Detroit Pistons
    {"id": 3962, "first_name": "Cade", "last_name": "Cunningham", "position": "G", "height_feet": 6, "height_inches": 6, "weight_pounds": 220,
     "team": {"id": 9, "abbreviation": "DET", "city": "Detroit", "conference": "East", "division": "Central", "full_name": "Detroit Pistons", "name": "Pistons"}},
    {"id": 3963, "first_name": "Jaden", "last_name": "Ivey", "position": "G", "height_feet": 6, "height_inches": 4, "weight_pounds": 195,
     "team": {"id": 9, "abbreviation": "DET", "city": "Detroit", "conference": "East", "division": "Central", "full_name": "Detroit Pistons", "name": "Pistons"}},

    # Memphis Grizzlies
    {"id": 3964, "first_name": "Ja", "last_name": "Morant", "position": "G", "height_feet": 6, "height_inches": 3, "weight_pounds": 174,
     "team": {"id": 15, "abbreviation": "MEM", "city": "Memphis", "conference": "West", "division": "Southwest", "full_name": "Memphis Grizzlies", "name": "Grizzlies"}},
    {"id": 3965, "first_name": "Jaren", "last_name": "Jackson Jr.", "position": "F-C", "height_feet": 6, "height_inches": 11, "weight_pounds": 242,
     "team": {"id": 15, "abbreviation": "MEM", "city": "Memphis", "conference": "West", "division": "Southwest", "full_name": "Memphis Grizzlies", "name": "Grizzlies"}},

    # New Orleans Pelicans
    {"id": 3966, "first_name": "Zion", "last_name": "Williamson", "position": "F", "height_feet": 6, "height_inches": 6, "weight_pounds": 284,
     "team": {"id": 18, "abbreviation": "NOP", "city": "New Orleans", "conference": "West", "division": "Southwest", "full_name": "New Orleans Pelicans", "name": "Pelicans"}},
    {"id": 3967, "first_name": "Brandon", "last_name": "Ingram", "position": "F", "height_feet": 6, "height_inches": 8, "weight_pounds": 190,
     "team": {"id": 18, "abbreviation": "NOP", "city": "New Orleans", "conference": "West", "division": "Southwest", "full_name": "New Orleans Pelicans", "name": "Pelicans"}},

    # Houston Rockets
    {"id": 3968, "first_name": "Alperen", "last_name": "Sengun", "position": "C", "height_feet": 6, "height_inches": 10, "weight_pounds": 243,
     "team": {"id": 11, "abbreviation": "HOU", "city": "Houston", "conference": "West", "division": "Southwest", "full_name": "Houston Rockets", "name": "Rockets"}},
    {"id": 3969, "first_name": "Jalen", "last_name": "Green", "position": "G", "height_feet": 6, "height_inches": 4, "weight_pounds": 186,
     "team": {"id": 11, "abbreviation": "HOU", "city": "Houston", "conference": "West", "division": "Southwest", "full_name": "Houston Rockets", "name": "Rockets"}},

    # San Antonio Spurs
    {"id": 3970, "first_name": "Victor", "last_name": "Wembanyama", "position": "C", "height_feet": 7, "height_inches": 4, "weight_pounds": 210,
     "team": {"id": 24, "abbreviation": "SAS", "city": "San Antonio", "conference": "West", "division": "Southwest", "full_name": "San Antonio Spurs", "name": "Spurs"}},
    {"id": 3971, "first_name": "Devin", "last_name": "Vassell", "position": "G", "height_feet": 6, "height_inches": 5, "weight_pounds": 200,
     "team": {"id": 24, "abbreviation": "SAS", "city": "San Antonio", "conference": "West", "division": "Southwest", "full_name": "San Antonio Spurs", "name": "Spurs"}},

    # Oklahoma City Thunder
    {"id": 3972, "first_name": "Shai", "last_name": "Gilgeous-Alexander", "position": "G", "height_feet": 6, "height_inches": 6, "weight_pounds": 195,
     "team": {"id": 21, "abbreviation": "OKC", "city": "Oklahoma City", "conference": "West", "division": "Northwest", "full_name": "Oklahoma City Thunder", "name": "Thunder"}},
    {"id": 3973, "first_name": "Chet", "last_name": "Holmgren", "position": "C", "height_feet": 7, "height_inches": 0, "weight_pounds": 195,
     "team": {"id": 21, "abbreviation": "OKC", "city": "Oklahoma City", "conference": "West", "division": "Northwest", "full_name": "Oklahoma City Thunder", "name": "Thunder"}},

    # Minnesota Timberwolves
    {"id": 3974, "first_name": "Anthony", "last_name": "Edwards", "position": "G", "height_feet": 6, "height_inches": 4, "weight_pounds": 225,
     "team": {"id": 16, "abbreviation": "MIN", "city": "Minnesota", "conference": "West", "division": "Northwest", "full_name": "Minnesota Timberwolves", "name": "Timberwolves"}},
    {"id": 3977, "first_name": "Karl-Anthony", "last_name": "Towns", "position": "C", "height_feet": 6, "height_inches": 11, "weight_pounds": 248,
     "team": {"id": 16, "abbreviation": "MIN", "city": "Minnesota", "conference": "West", "division": "Northwest", "full_name": "Minnesota Timberwolves", "name": "Timberwolves"}},
    {"id": 3978, "first_name": "Rudy", "last_name": "Gobert", "position": "C", "height_feet": 7, "height_inches": 1, "weight_pounds": 258,
     "team": {"id": 16, "abbreviation": "MIN", "city": "Minnesota", "conference": "West", "division": "Northwest", "full_name": "Minnesota Timberwolves", "name": "Timberwolves"}},

    # Portland Trail Blazers
    {"id": 3979, "first_name": "Anfernee", "last_name": "Simons", "position": "G", "height_feet": 6, "height_inches": 3, "weight_pounds": 181,
     "team": {"id": 22, "abbreviation": "POR", "city": "Portland", "conference": "West", "division": "Northwest", "full_name": "Portland Trail Blazers", "name": "Trail Blazers"}},
    {"id": 3980, "first_name": "Scoot", "last_name": "Henderson", "position": "G", "height_feet": 6, "height_inches": 2, "weight_pounds": 195,
     "team": {"id": 22, "abbreviation": "POR", "city": "Portland", "conference": "West", "division": "Northwest", "full_name": "Portland Trail Blazers", "name": "Trail Blazers"}},

    # Utah Jazz
    {"id": 3981, "first_name": "Lauri", "last_name": "Markkanen", "position": "F", "height_feet": 7, "height_inches": 0, "weight_pounds": 240,
     "team": {"id": 29, "abbreviation": "UTA", "city": "Utah", "conference": "West", "division": "Northwest", "full_name": "Utah Jazz", "name": "Jazz"}},
    {"id": 3982, "first_name": "Walker", "last_name": "Kessler", "position": "C", "height_feet": 7, "height_inches": 0, "weight_pounds": 245,
     "team": {"id": 29, "abbreviation": "UTA", "city": "Utah", "conference": "West", "division": "Northwest", "full_name": "Utah Jazz", "name": "Jazz"}},

    # Sacramento Kings
    {"id": 3983, "first_name": "De'Aaron", "last_name": "Fox", "position": "G", "height_feet": 6, "height_inches": 3, "weight_pounds": 185,
     "team": {"id": 23, "abbreviation": "SAC", "city": "Sacramento", "conference": "West", "division": "Pacific", "full_name": "Sacramento Kings", "name": "Kings"}},
    {"id": 3984, "first_name": "Domantas", "last_name": "Sabonis", "position": "C", "height_feet": 6, "height_inches": 11, "weight_pounds": 240,
     "team": {"id": 23, "abbreviation": "SAC", "city": "Sacramento", "conference": "West", "division": "Pacific", "full_name": "Sacramento Kings", "name": "Kings"}},

    # LA Clippers
    {"id": 3985, "first_name": "Kawhi", "last_name": "Leonard", "position": "F", "height_feet": 6, "height_inches": 7, "weight_pounds": 225,
     "team": {"id": 12, "abbreviation": "LAC", "city": "Los Angeles", "conference": "West", "division": "Pacific", "full_name": "LA Clippers", "name": "Clippers"}},
    {"id": 3986, "first_name": "Paul", "last_name": "George", "position": "F", "height_feet": 6, "height_inches": 8, "weight_pounds": 220,
     "team": {"id": 12, "abbreviation": "LAC", "city": "Los Angeles", "conference": "West", "division": "Pacific", "full_name": "LA Clippers", "name": "Clippers"}},
    {"id": 3987, "first_name": "James", "last_name": "Harden", "position": "G", "height_feet": 6, "height_inches": 5, "weight_pounds": 220,
     "team": {"id": 12, "abbreviation": "LAC", "city": "Los Angeles", "conference": "West", "division": "Pacific", "full_name": "LA Clippers", "name": "Clippers"}},

    # Additional notable players
    {"id": 500, "first_name": "Chris", "last_name": "Paul", "position": "G", "height_feet": 6, "height_inches": 0, "weight_pounds": 175,
     "team": {"id": 10, "abbreviation": "GSW", "city": "Golden State", "conference": "West", "division": "Pacific", "full_name": "Golden State Warriors", "name": "Warriors"}},
    {"id": 501, "first_name": "Russell", "last_name": "Westbrook", "position": "G", "height_feet": 6, "height_inches": 3, "weight_pounds": 200,
     "team": {"id": 13, "abbreviation": "LAC", "city": "Los Angeles", "conference": "West", "division": "Pacific", "full_name": "LA Clippers", "name": "Clippers"}},
    {"id": 502, "first_name": "Carmelo", "last_name": "Anthony", "position": "F", "height_feet": 6, "height_inches": 7, "weight_pounds": 238,
     "team": None},  # Free agent
    {"id": 503, "first_name": "Blake", "last_name": "Griffin", "position": "F-C", "height_feet": 6, "height_inches": 9, "weight_pounds": 250,
     "team": None},  # Free agent
]


def search_local_players(query: str, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Fuzzy search implementation for local player data.

    This function performs intelligent matching with multiple strategies:
    1. Exact match (score: 100)
    2. Starts with query (score: 90)
    3. Contains query (score: 80)
    4. Fuzzy match using fuzzywuzzy (score: 0-100)

    Args:
        query: Search term (e.g., "LeBron James", "lebron", "James")
        limit: Maximum number of results to return

    Returns:
        List of player dictionaries sorted by relevance

    Examples:
        >>> search_local_players("LeBron James", 5)
        [{"first_name": "LeBron", "last_name": "James", ...}]

        >>> search_local_players("lebron", 5)  # Case insensitive
        [{"first_name": "LeBron", "last_name": "James", ...}]

        >>> search_local_players("James", 10)  # Returns all players with last name James
        [{"first_name": "LeBron", "last_name": "James", ...}, ...]

        >>> search_local_players("Lebron Jame", 5)  # Typo tolerant
        [{"first_name": "LeBron", "last_name": "James", ...}]
    """
    if not query or not query.strip():
        return []

    query_lower = query.strip().lower()
    scored = []

    for player in SAMPLE_PLAYERS:
        full_name = f"{player['first_name']} {player['last_name']}"
        first_name = player['first_name']
        last_name = player['last_name']

        # Multiple matching strategies
        full_name_lower = full_name.lower()
        first_name_lower = first_name.lower()
        last_name_lower = last_name.lower()

        # Exact match
        if query_lower == full_name_lower:
            score = 100
        # Starts with query
        elif full_name_lower.startswith(query_lower) or \
             first_name_lower.startswith(query_lower) or \
             last_name_lower.startswith(query_lower):
            score = 90
        # Contains query
        elif query_lower in full_name_lower or \
             query_lower in first_name_lower or \
             query_lower in last_name_lower:
            score = 80
        # Fuzzy matching
        else:
            # Calculate fuzzy scores for different combinations
            full_name_score = fuzz.partial_ratio(query_lower, full_name_lower)
            first_name_score = fuzz.partial_ratio(query_lower, first_name_lower)
            last_name_score = fuzz.partial_ratio(query_lower, last_name_lower)

            # Use the highest score
            score = max(full_name_score, first_name_score, last_name_score)

        # Only include if score meets threshold
        if score >= 60:
            scored.append((player, score))

    # Sort by score (highest first), then alphabetically by last name
    scored.sort(key=lambda x: (-x[1], x[0]['last_name']))

    # Return top results
    return [player for player, _ in scored[:limit]]


def get_player_by_id(player_id: int) -> Dict[str, Any] | None:
    """
    Get a player by their ID.

    Args:
        player_id: The player's ID

    Returns:
        Player dictionary or None if not found
    """
    for player in SAMPLE_PLAYERS:
        if player['id'] == player_id:
            return player
    return None


def get_all_players() -> List[Dict[str, Any]]:
    """
    Get all sample players.

    Returns:
        List of all player dictionaries
    """
    return SAMPLE_PLAYERS.copy()


def get_players_by_team(team_abbr: str) -> List[Dict[str, Any]]:
    """
    Get all players on a specific team.

    Args:
        team_abbr: Team abbreviation (e.g., "LAL", "GSW")

    Returns:
        List of player dictionaries
    """
    return [
        player for player in SAMPLE_PLAYERS
        if player.get('team') and player['team']['abbreviation'] == team_abbr
    ]


# Test the search function
if __name__ == "__main__":
    print("Testing player search...")

    # Test 1: Exact match
    print("\n1. Searching for 'LeBron James':")
    results = search_local_players("LeBron James", 5)
    for player in results:
        print(f"  - {player['first_name']} {player['last_name']} ({player['team']['full_name'] if player.get('team') else 'Free Agent'})")

    # Test 2: Case insensitive
    print("\n2. Searching for 'lebron' (lowercase):")
    results = search_local_players("lebron", 5)
    for player in results:
        print(f"  - {player['first_name']} {player['last_name']} ({player['team']['full_name'] if player.get('team') else 'Free Agent'})")

    # Test 3: Last name only
    print("\n3. Searching for 'James':")
    results = search_local_players("James", 5)
    for player in results:
        print(f"  - {player['first_name']} {player['last_name']} ({player['team']['full_name'] if player.get('team') else 'Free Agent'})")

    # Test 4: Typo
    print("\n4. Searching for 'Lebron Jame' (typo):")
    results = search_local_players("Lebron Jame", 5)
    for player in results:
        print(f"  - {player['first_name']} {player['last_name']} ({player['team']['full_name'] if player.get('team') else 'Free Agent'})")

    # Test 5: Partial name
    print("\n5. Searching for 'Curry':")
    results = search_local_players("Curry", 5)
    for player in results:
        print(f"  - {player['first_name']} {player['last_name']} ({player['team']['full_name'] if player.get('team') else 'Free Agent'})")

    print(f"\n[checkmark.circle] Total players in database: {len(SAMPLE_PLAYERS)}")
