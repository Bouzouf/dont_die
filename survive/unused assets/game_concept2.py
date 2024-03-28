import random, time
bases = [
    "@ gave @ a $, and @ got jealous so he & them",
    "When @ saw *, they couldn't believe their eyes!",
    "After a long day, @ decided to & with a $.",
    "In the enchanted forest, @ encountered a mysterious *.",
    "The secret recipe for happiness involves @, $, and &.",
    "During the treasure hunt, @ found a hidden *.",
    "Late at night, @ whispered sweet nothings into @'s ear.",
    "The mischievous gnome stole @'s * and ran away.",
    "In the bustling market, @ haggled over the price of a $.",
    "The ancient prophecy foretold that @ would one day & the *.",
    "When @ danced, the whole world seemed to spin with them.",
    "The magical potion turned @ into a talking *.",
    "On a moonlit night, @ confessed their love to *.",
    "The eccentric inventor created a machine that could * with a $.",
    "In the haunted mansion, @ encountered a ghostly *.",
    "The mischievous fairy sprinkled @ with pixie dust, and they *.",
    "The time-traveling adventurer accidentally stepped on a $.",
    "The mysterious stranger handed @ a cryptic note containing *.",
    "When @ played the violin, the entire audience was moved to tears.",
    "The ancient scroll revealed the location of the legendary *.",
    "In the parallel universe, @ met their doppelgänger, who was *.",
    "The fortune teller predicted that @ would find their true love under a $.",
    "The brave knight embarked on a quest to rescue @ from a *.",
    "During the thunderstorm, @ discovered a hidden cave filled with $.",
    "The eccentric professor conducted experiments involving @ and *.",
    "In the enchanted garden, @ planted a magical seed that grew into a $.",
    "The time-traveling detective solved the case by unraveling the mystery of *.",
    "When @ sang, the birds joined in harmony with their *.",
    "The ancient artifact had the power to grant @ three wishes: $, &, and *.",
    "In the whimsical tea party, @ sipped from a cup that made them see *.",
]

names = [
    "Alice", "Bob", "Charlie", "David", "Eva",
    "Fiona", "George", "Hannah", "Isaac", "Julia",
    "Kevin", "Lena", "Max", "Nina", "Oliver",
    "Penny", "Quinn", "Rachel", "Sam", "Tina",
    "Ursula", "Victor", "Wendy", "Xander", "Yara",
    "Zane", "Alex", "Grace", "Henry", "Ivy"
]

nouns = [
    "unicorn", "treasure", "key", "map", "spell",
    "diamond", "dragon", "wand", "crown", "enchanted forest",
    "magic potion", "time machine", "fairy tale", "star",
    "secret passage", "mermaid", "wizard", "castle", "rainbow",
    "phoenix", "moonstone", "storybook", "genie", "amulet",
    "goblin", "crystal ball", "enchanted garden", "el", "sorcerer"
]

outcomes = [
    "eternal happiness", "true love", "adventure", "mystery",
    "hidden treasure", "enchanted realm", "magical transformation",
    "time-traveling journey", "epic quest", "fairy wings",
    "enchanted melody", "lost civilization", "enchanted mirror",
    "whimsical tea party", "enchanted spellbook", "enchanted rose",
    "enchanted waterfall", "enchanted sunset", "enchanted moon",
    "enchanted starlight", "enchanted dance", "enchanted sunrise",
    "enchanted labyrinth", "enchanted dream", "enchanted harmony",
    "enchanted whispers", "enchanted laughter", "enchanted wings",
    "enchanted sunrise", "enchanted twilight", "enchanted voyage"
]

verbs = [
    "danced", "discovered", "whispered", "created", "solved",
    "embarked", "haggled", "planted", "confessed", "encountered",
    "sang", "conducted", "stole", "sprinkled", "transformed",
    "saw", "decided", "hunted", "unraveled", "played",
    "invented", "met", "rescued", "haggled", "sipped",
    "wished", "confided", "swirled", "laughed", "journeyed"
]

player_questions = base_sentences_past_tense = [
    "Had @ really & a $, resulting in *?",
    "Did you think @ should have & if the $ was not *?",
    "Was it possible for @ to have & without a $?",
    "Why would @ have chosen to & a $?",
    "What happened when @ and @ both & the same $?",
    "Should @ have & a $ before * occurred?",
    "Could @ and @ have & together with a $?",
    "Would @ ever have & a $ to achieve *?",
    "How could @ have & a $ and still ended up with *?",
    "Who would @ have & if the $ was not available?",
    "When did @ decide to & the $?",
    "Where did @ go to & a $?",
    "Which $ should @ have & to ensure *?",
    "Were there any reasons @ wouldn't have & a $?",
    "What if @ and @ had & at the same time?",
    "Did @ have what it took to & a $?",
    "Was @ able to & a $ after *?",
    "How often did @ & a $?",
    "Had @ ever managed to & a $?",
    "Who else besides @ might have & a $?",
    "What kind of $ would @ have &?",
    "Why didn't @ & a $ more often?",
    "Could @ have & a $ for *?",
    "When had @ last & a $?",
    "Where was the best place for @ to have & a $?",
    "Which was more likely for @, to have & a $ or to have *?",
    "Were you expecting @ to have & a $ soon?",
    "What if @ never & a $?",
    "Did @ know how to & a $ properly?",
    "Had @ & a $ in time for *?"
]




import random

def generate_random_sentence(sentence=''):
    if not(sentence):
        sentence = random.choice(bases)
    sentence = sentence.replace("@", random.choice(names))
    sentence = sentence.replace("$", random.choice(nouns))
    sentence = sentence.replace("&", random.choice(verbs))
    sentence = sentence.replace("*", random.choice(outcomes))
    return sentence

while True:
    print(generate_random_sentence())
    time.sleep(3)
    choice = random.randint(1,2)
    if choice == 2:
        sentence = random.choice(player_questions)
        question = str(generate_random_sentence(sentence)) + " "
        input(question)