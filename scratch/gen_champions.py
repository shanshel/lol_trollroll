
import json

# List of champions from the user's file
champions = [
    "Aatrox", "Ahri", "Akali", "Akshan", "Alistar", "Amumu", "Anivia", "Annie", "Aphelios", "Ashe",
    "Aurelion Sol", "Azir", "Bard", "Bel'Veth", "Blitzcrank", "Brand", "Braum", "Briar", "Caitlyn",
    "Camille", "Cassiopeia", "Cho'Gath", "Corki", "Darius", "Diana", "Dr. Mundo", "Draven", "Ekko",
    "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora", "Fizz", "Galio", "Gangplank", "Garen",
    "Gnar", "Gragas", "Graves", "Gwen", "Hecarim", "Heimerdinger", "Hwei", "Illaoi", "Irelia",
    "Ivern", "Janna", "Jarvan IV", "Jax", "Jayce", "Jhin", "Jinx", "K'Sante", "Kai'Sa", "Kalista",
    "Karma", "Karthus", "Kassadin", "Katarina", "Kayle", "Kayn", "Kennen", "Kha'Zix", "Kindred",
    "Kled", "Kog'Maw", "LeBlanc", "Lee Sin", "Leona", "Lillia", "Lissandra", "Lucian", "Lulu",
    "Lux", "Malphite", "Malzahar", "Maokai", "Master Yi", "Milio", "Miss Fortune", "Mordekaiser",
    "Morgana", "Naafiri", "Nami", "Nasus", "Nautilus", "Neeko", "Nidalee", "Nilah", "Nocturne",
    "Nunu & Willump", "Olaf", "Orianna", "Ornn", "Pantheon", "Poppy", "Pyke", "Qiyana", "Quinn",
    "Rakan", "Rammus", "Rek'Sai", "Rell", "Renata Glasc", "Renekton", "Rengar", "Riven", "Rumble",
    "Ryze", "Samira", "Sejuani", "Senna", "Seraphine", "Sett", "Shaco", "Shen", "Shyvana", "Singed",
    "Sion", "Sivir", "Skarner", "Sona", "Soraka", "Swain", "Sylas", "Syndra", "Tahm Kench",
    "Taliyah", "Talon", "Taric", "Teemo", "Thresh", "Tristana", "Trundle", "Tryndamere",
    "Twisted Fate", "Twitch", "Udyr", "Urgot", "Varus", "Vayne", "Veigar", "Vel'Koz", "Vex",
    "Vi", "Viego", "Viktor", "Vladimir", "Volibear", "Warwick", "Wukong", "Xayah", "Xerath",
    "Xin Zhao", "Yasuo", "Yone", "Yorick", "Yuumi", "Zac", "Zed", "Zeri", "Ziggs", "Zilean",
    "Zoe", "Zyra", "Smolder", "Aurora", "Ambessa", "Mel Medarda", "Yunara", "Zaahen"
]

# Mapping rules for roles and features
# This is a simplified heuristic to avoid manual tagging of 170+ items
# Real apps would use a database, but we'll simulate a well-tagged list.

role_map = {
    "Top": ["Aatrox", "Camille", "Cho'Gath", "Darius", "Dr. Mundo", "Fiora", "Garen", "Gnar", "Gwen", "Illaoi", "Irelia", "Jax", "K'Sante", "Kayle", "Kled", "Malphite", "Maokai", "Mordekaiser", "Nasus", "Olaf", "Ornn", "Poppy", "Renekton", "Riven", "Rumble", "Sett", "Shen", "Singed", "Sion", "Tahm Kench", "Teemo", "Tryndamere", "Urgot", "Volibear", "Wukong", "Yorick", "Ambessa"],
    "Jungle": ["Amumu", "Bel'Veth", "Briar", "Diana", "Ekko", "Elise", "Evelynn", "Fiddlesticks", "Gragas", "Graves", "Hecarim", "Ivern", "Jarvan IV", "Jax", "Karthus", "Kayn", "Kha'Zix", "Kindred", "Lee Sin", "Lillia", "Master Yi", "Nidalee", "Nocturne", "Nunu & Willump", "Olaf", "Rammus", "Rek'Sai", "Rengar", "Sejuani", "Shaco", "Shyvana", "Skarner", "Taliyah", "Trundle", "Udyr", "Vi", "Viego", "Volibear", "Warwick", "Wukong", "Xin Zhao", "Zac"],
    "Mid": ["Ahri", "Akali", "Akshan", "Anivia", "Annie", "Aurelion Sol", "Azir", "Cassiopeia", "Corki", "Diana", "Ekko", "Fizz", "Galio", "Heimerdinger", "Hwei", "Kassadin", "Katarina", "LeBlanc", "Lissandra", "Lux", "Malzahar", "Naafiri", "Neeko", "Orianna", "Pantheon", "Qiyana", "Ryze", "Sylas", "Syndra", "Talon", "Twisted Fate", "Veigar", "Vel'Koz", "Vex", "Viktor", "Vladimir", "Yasuo", "Yone", "Ziggs", "Zoe", "Aurora"],
    "ADC": ["Aphelios", "Ashe", "Caitlyn", "Draven", "Ezreal", "Jhin", "Jinx", "Kai'Sa", "Kalista", "Kog'Maw", "Lucian", "Miss Fortune", "Nilah", "Quinn", "Samira", "Senna", "Sivir", "Tristana", "Twitch", "Varus", "Vayne", "Xayah", "Zeri", "Smolder"],
    "Sup": ["Alistar", "Bard", "Blitzcrank", "Brand", "Braum", "Janna", "Karma", "Leona", "Lulu", "Lux", "Milio", "Morgana", "Nami", "Nautilus", "Pyke", "Rakan", "Rell", "Renata Glasc", "Senna", "Seraphine", "Sona", "Soraka", "Swain", "Taric", "Thresh", "Yuumi", "Zilean", "Zyra", "Mel Medarda"]
}

feature_map = {
    "Heal": ["Aatrox", "Alistar", "Bard", "Briar", "Dr. Mundo", "Ivern", "Milio", "Nami", "Nidalee", "Olaf", "Renata Glasc", "Senna", "Sona", "Soraka", "Swain", "Sylas", "Taric", "Vladimir", "Warwick", "Yuumi"],
    "Slow": ["Anivia", "Ashe", "Braum", "Cassiopeia", "Cho'Gath", "Darius", "Dr. Mundo", "Ekko", "Gragas", "Janna", "Jhin", "Jinx", "Karthus", "Lulu", "Malphite", "Nasus", "Nunu & Willump", "Olaf", "Rylai", "Sejuani", "Singed", "Skarner", "Thresh", "Tryndamere", "Twitch", "Viktor", "Zac", "Ziggs", "Zilean"],
    "Poison": ["Cassiopeia", "Singed", "Teemo", "Twitch"],
    "Tank": ["Alistar", "Amumu", "Blitzcrank", "Braum", "Cho'Gath", "Dr. Mundo", "Galio", "Garen", "Jarvan IV", "K'Sante", "Leona", "Malphite", "Maokai", "Mordekaiser", "Nautilus", "Ornn", "Poppy", "Rammus", "Rell", "Sejuani", "Shen", "Sion", "Skarner", "Tahm Kench", "Udyr", "Volibear", "Zac"],
    "Stun": ["Alistar", "Amumu", "Anivia", "Annie", "Ashe", "Aurelion Sol", "Bard", "Brand", "Braum", "Ekko", "Elise", "Galio", "Gnar", "Heimerdinger", "Irelia", "Jax", "Kennan", "Leona", "Lissandra", "Lux", "Malzahar", "Morgana", "Nami", "Nautilus", "Neeko", "Ornn", "Pantheon", "Poppy", "Pyke", "Rakan", "Rell", "Renekton", "Sejuani", "Sona", "Syndra", "Taric", "Thresh", "Udyr", "Varus", "Veigar", "Vex", "Viktor", "Volibear", "Warwick", "Wukong", "Xerath", "Xin Zhao", "Zac", "Zoe", "Zyra"],
    "Root": ["Caitlyn", "Ivern", "Jhin", "Jinx", "Karma", "Leblanc", "Lulu", "Lux", "Maokai", "Morgana", "Neeko", "Nidalee", "Renata Glasc", "Ryze", "Senna", "Seraphine", "Swain", "Sylas", "Varus", "Xayah", "Zyra"],
    "Short": ["Amumu", "Annie", "Fizz", "Gnar", "Heimerdinger", "Kennen", "Kled", "Lulu", "Poppy", "Rumble", "Teemo", "Tristana", "Veigar", "Vex", "Ziggs", "Yuumi", "Smolder"],
    "Scaling": ["Aurelion Sol", "Cho'Gath", "Kassadin", "Kayle", "Nasus", "Senna", "Smolder", "Veigar", "Vladimir"]
}

# Combine everything
output = []
for name in champions:
    tags = []
    # Add roles
    for role, champs in role_map.items():
        if name in champs:
            tags.append(role)
    # Add features
    for feature, champs in feature_map.items():
        if name in champs:
            tags.append(feature)
    
    # Ensure every champ has at least one role for fallback (Random)
    if not any(r in role_map.keys() for r in tags):
        tags.append("Mid") # Default fallback for missing data
        
    output.append({
        "name": name,
        "tags": tags
    })

with open('champions.json', 'w') as f:
    json.dump({"champions": output}, f, indent=2)
