ART = {
    "horse": ("horse-barn.jpg", "A chestnut horse standing in a wooden barn"),
    "pony": ("pony-and-horse-pasture.jpg", "A chestnut pony and taller bay horse standing in a pasture"),
    "elephant": ("baby-elephant.jpg", "A young elephant in a leafy grove"),
    "puppies": ("puppies.jpg", "Three puppies resting together by a window"),
    "books": ("lemonade-books.jpg", "Books and a lemon on a table"),
    "interviews": ("interviews-barn-notebook.jpg", "A notebook and empty chair near a horse’s stall"),
}

# Remove a key here when replacing an illustration with a photograph.
ILLUSTRATIONS = {"horse", "pony", "elephant", "puppies", "books", "interviews"}

STORIES = {
    "martha-wunder": {
        "title": "At the Barn with Martha Wunder",
        "label": "At the barn",
        "summary": "Charlotte goes to check on Crispy and wonders how a trainer knows when a horse needs more time.",
        "art": "horse",
        "body": ("Checking on Crispy", "Charlotte’s visit to check on Crispy is a starting point for thinking about horse care. Checking in on a familiar horse and helping a horse get comfortable with something new are two different moments that make Charlotte curious about what a trainer pays attention to. Horse trainer Martha Wunder is someone she wants to ask."),
        "questions": ("a-question-for-a-trainer", [
            "How can a trainer tell when a horse needs more time to get comfortable with something new?",
            "What might you notice when you check in on a horse you know well?",
            "How do you decide when to try again and when to give the horse a break?",
        ]),
    },
    "baby-elephant": {
        "title": "A Baby Elephant at the National Zoo",
        "label": "At the zoo",
        "summary": "A visit to the National Zoo gets Charlotte wondering what it takes to care for a growing elephant.",
        "art": "elephant",
        "body": ("A visit to the zoo", "Charlotte went to the National Zoo to see a baby elephant. Seeing a young elephant as a visitor made her curious about the parts of its day she couldn’t see. She’d like to know what keepers pay attention to as the elephant grows and what their work looks like on an ordinary day."),
        "questions": ("a-question-for-a-keeper", [
            "What does a typical day caring for a baby elephant look like?",
            "What changes do keepers watch for as a young elephant grows?",
            "How do keepers get to know what an elephant needs?",
        ]),
    },
    "puppies": {
        "title": "Meet the Puppies",
        "label": "At home",
        "summary": "Three young puppies are growing up, learning to play, and getting to know their surroundings.",
        "art": "puppies",
        "body": ("Three little explorers", "This story follows three young puppies at home as they grow, play, and get to know their surroundings. Charlotte is curious about how play changes as puppies get bigger and how the people looking after them can tell when it’s time for a rest."),
        "questions": ("a-question-about-growing-up", [
            "How does the way puppies play together change as they get bigger?",
            "What might a puppy do when it’s ready for a break?",
            "How can you tell when a puppy feels comfortable exploring somewhere new?",
        ]),
    },
}

GUIDES = {
    "ponies-and-horses": {
        "title": "Do ponies behave differently from horses?",
        "summary": "Size tells you how tall an animal is. Getting to know the individual tells you much more about how it might act.",
        "art": "pony",
        "question": "What could you ask a handler to learn about the personality of a horse or pony they know?",
        "sections": [
            ("Get to know the individual", "One pony might explore a new object right away. Another might hang back, just as a larger horse might. Researchers have found some differences between breeds, and they also find that personality varies from one animal to another. Experience and how an animal is kept can matter too."),
            ("Watch with someone who knows them", "Ask an experienced adult to show you what relaxed or worried behavior looks like in a horse or pony they know. Before approaching, ask the handler where to stand and whether the animal is comfortable being greeted."),
        ],
        "sources": [
            ("Effects of size and personality in horses", "https://pmc.ncbi.nlm.nih.gov/articles/PMC6834737/"),
            ("Equine Personality: Association With Breed, Use, and Husbandry Factors", "https://pubmed.ncbi.nlm.nih.gov/30929783/"),
        ],
    },
    "hoof-care": {
        "title": "Hoof care",
        "summary": "Find out what a hoof check is and what a farrier does.",
        "art": "horse",
        "question": "What might a farrier notice that you would want to ask about?",
        "sections": [
            ("What are we looking for?", "A hoof is the hard outer part of a horse’s foot. Mud and little stones can collect underneath it. When an experienced adult checks a hoof, they look for trapped debris and changes such as cracks or a loose shoe."),
            ("Who helps keep hooves healthy?", "A qualified farrier trims hooves and fits shoes when a horse needs them. Watch an experienced adult before trying to handle a hoof. If the horse suddenly limps or seems sore, tell the adult so they can contact a veterinarian."),
        ],
        "sources": [("Caring for your horse’s hooves · University of Minnesota Extension", "https://extension.umn.edu/agriculture/animals-and-livestock/horse/caring-for-your-horses-hooves")],
    },
    "grooming": {
        "title": "Grooming",
        "summary": "A brush can lift dust and help you notice how a horse is feeling.",
        "art": "horse",
        "question": "What could you ask the handler before choosing a brush?",
        "sections": [
            ("A closer look at the coat", "Grooming means looking after the coat, mane, and tail. Brushes help lift loose dirt and hair. While grooming, a handler has a chance to notice changes such as a scrape or a tender spot."),
            ("Learn where to stand", "Ask an experienced adult which brush to use and where it’s safe to stand. If the horse moves away or a spot seems sore, pause and tell the adult so they can decide whether a veterinarian should take a look."),
        ],
        "sources": [("Grooming tips · US Equestrian", "https://www.usef.org/media/press-releases/pro-tip-5-grooming-tips-from-max-corcoran")],
    },
    "grazing": {
        "title": "Grazing",
        "summary": "Learn what horses eat in a pasture and why grazing time can vary.",
        "art": "pony",
        "question": "What would you ask the person in charge before opening a pasture gate?",
        "sections": [
            ("Eating a little at a time", "Grazing means eating grass and other suitable plants as a horse moves through a pasture. Grass and hay are examples of forage, the fibrous plants that make up much of a horse’s diet."),
            ("Every horse has its own plan", "A horse’s needs depend on its health, activity, and what’s growing in the field. Ask the adult in charge before opening a gate or offering extra grass. A veterinarian can help plan pasture access for a horse with a health condition."),
        ],
        "sources": [("Grazing horses on mixed pastures · University of Minnesota Extension", "https://extension.umn.edu/agriculture/animals-and-livestock/horse/grazing-horses-on-grass-and-legume-mixed-pastures")],
    },
    "washing": {
        "title": "Washing",
        "summary": "See what goes into a wash and why the weather matters.",
        "art": "horse",
        "question": "What would you check with the handler before getting the hose ready?",
        "sections": [
            ("A rinse or a bath?", "Washing usually means rinsing away dirt or sweat with water. An experienced handler can decide whether a small area needs rinsing or whether a full bath makes sense for that horse and weather."),
            ("Set up with an adult", "An experienced adult checks the footing, water temperature, and water pressure and makes sure the horse is comfortable. Ask where you can help. If you spot a sore or irritated patch of skin, tell the adult so they can ask a veterinarian about it."),
        ],
        "sources": [("Care skills guidance, including bathing · British Horse Society", "https://www.bhs.org.uk/media/gzdpv23w/ap-guidance-for-signing-skills-records-04-2023.pdf")],
    },
}
