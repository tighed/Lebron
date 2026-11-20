from drafter import *
from dataclasses import dataclass




@dataclass
class Game:
    """general information about the game that Lebron played this season"""
    opponent: str
    points: int
    win: bool


@dataclass
class Question:
    """ Stores questions and asks user about the difficulty of said questions"""
    question_text: str
    options: list[str]
    answer: str


@dataclass
class Lebron:
    """ Lebron's stats stored in its own place"""
    points: int
    full_name: str
    the_goat: bool
    wins: int
    games_played: int
    record: str
    
@dataclass
class State:
    """ Everything the site must remember between pages"""
    correct_answers: int
    games: list[Game]
    player_name: str
    lebron: Lebron
    questions: list[Question]
    question_number: int
    current_stat: str


QUESTIONS_EASY = [

    Question("What jersey number is LeBron James wearing for the 76ers?",
        ["23", "69", "3"], "23"),

    Question("Which team did LeBron leave in free agency to join Philadelphia?",
         ["Dallas Mavericks", "Sacramento Kings", "LA Lakers"], "LA Lakers"),

    Question("How many NBA seasons has LeBron played as of the 2026–27 campaign?",
         ["1", "20", "30", "24"], "24")
                  ]
QUESTIONS_MEDIUM = [

    Question("What contract did LeBron James sign with the Philadelphia 76ers?",
             ["1-year, $8 million", "2-year, $8 million", "3-year, $15 million", "2-year, $20 million"], "2-year, $8 million"),

    Question("How many NBA championships has LeBron James won?",
             ["2", "3", "4", "5"], "4"),

    Question("Which team drafted LeBron James in 2003?",
             ["Miami Heat", "Chicago Bulls", "Cleveland Cavaliers", "LA Lakers"], "Cleveland Cavaliers"),

    Question("What year did LeBron James win his first NBA championship?",
             ["2008", "2010", "2012", "2016"], "2012"),

    Question("How many NBA MVP awards has LeBron James won?",
             ["2", "3", "4", "5"], "4")
]


QUESTIONS_HARD = [

    Question("How many consecutive NBA games did LeBron James score at least 10 points in before the streak ended?",
             ["500", "1,000", "1,297", "1,500"], "1,297"),

    Question("What was LeBron James' overall draft position in the 2003 NBA Draft?",
             ["1st", "2nd", "3rd", "5th"], "1st"),

    Question("How many points did LeBron James score in his famous 2016 NBA Finals Game 5?",
             ["35", "41", "45", "51"], "41"),

    Question("Which team did LeBron James defeat to win his first NBA championship?",
             ["Oklahoma City Thunder", "Boston Celtics", "San Antonio Spurs", "Golden State Warriors"], "Oklahoma City Thunder"),

    Question("What is LeBron James' career-high single-game scoring total in the NBA?",
             ["56", "61", "65", "71"], "61")
]




'''
set_website_title("Lebron Quiz")
set_site_information(
    author="Tighe Duffy",
    description="Take a short quiz about Lebron's 26-27 season with the 76ers!",
    sources="Thanks to the Drafter docs",
    planning=["plan.pdf", "design.pdf"],
    links=[]
)
hide_debug_information()
set_website_framed(False)
'''

@route
def index(state: State) -> Page:
    return Page(state, [
        Header("Welcome to Lebron quiz! \n WE LOVE LEBRON", 1),
        Button("Start Quiz", "whats_your_name"),
        Button("Stats", "stats_page"), 
    ])

@route
def whats_your_name(state: State) -> Page:
    return Page(state, [
        Header("What's your name?"),
        TextBox("new_player_name", state.player_name),
        "\n",
        Button("OK", "new_name")
    ])

@route
def new_name(state: State, new_player_name: str) -> Page:
    state.player_name = new_player_name
    return select_difficulty(state)


@route
def select_difficulty(state: State) -> Page: 
  return Page(state, [
      Header("Hi " + state.player_name + " Welcome to the Lebron Quiz!"),
      "\nPick your difficulty \n", 
      SelectBox("difficulty", ["easy", "medium", "hard"], "easy"),
      "\n",
      Button("Start", add_questions)
    ])

@route
def add_questions(state: State, difficulty: str):
  if difficulty == "easy":
    state.questions = QUESTIONS_EASY
  elif difficulty == "medium":
    state.questions = QUESTIONS_MEDIUM
  elif difficulty == "hard":
    state.questions = QUESTIONS_HARD
  return display_quiz_question(state)



@route
def display_quiz_question(state: State) -> Page:
    question = state.questions[state.question_number]
    content = [
        Header("Question " + str(state.question_number + 1)),
        question.question_text + "\n"
    ]
    for option in question.options:
        content.append(Button(option, "right_or_wrong", [Argument("chosen", option)]))
        content.append("\n")
    return Page(state, content)



@route
def right_or_wrong(state: State, chosen: str) -> Page:
    question = state.questions[state.question_number]
    state.question_number = state.question_number + 1
    if chosen == question.answer:
        message = "Correct!"
        state.correct_answers = state.correct_answers + 1
    else:
        message = "Wrong. Fake fan. The answer was " + question.answer + "."
    if state.question_number < len(state.questions):
        return Page(state, [
            message + "\n",
            Button("Go on", "display_quiz_question")
        ])
    return Page(state, [
        message + "\n",
        Button("How'd you do?", "results")
    ])


@route
def results(state: State) -> Page:
    total = len(state.questions)
    if state.correct_answers / total >= 1:
        conclusion = "Good. LeGoat would be proud of you"
    elif state.correct_answers / total >= 0.6:
        conclusion = "Not bad. But also not good. LeHandsome will spare you"
    elif state.correct_answers / total >= 0.4:
        conclusion = "What?"
    else:
        conclusion = "You answer questions like Bronny plays basketball."

    return Page(state, [
        Header("Results"),
        "You scored " + str(state.correct_answers) + " out of " + str(total) + ".\n",
        conclusion + "\n",
        Button("Play again", "reset_quiz")
    ])

@route
def reset_quiz(state: State) -> Page:
    state.question_number = 0
    state.correct_answers = 0
    state.questions = []
    return index(state)



@route
def stats_page(state: State) -> Page:
    total = 0
    for game in state.games:
        total = total + game.points
    state.lebron.points = total
    
    return Page(state, [
        Header(state.lebron.full_name + "\'s Record"),
        state.current_stat + "\n",
        SelectBox("ideal_stats", ["points", "wins", "games played", "record"], "points"),
        "\n",
        Button("View Stat", "stat_viewer"),
        "\n",
        Button("Home", "index")
    ])

@route
def stat_viewer(state: State, ideal_stats: str) -> Page:
    total = 0
    wins = 0
    best = state.games[0]
    for game in state.games:
        total = total + game.points
        if game.win:
            wins = wins + 1
        if game.points > best.points:
            best = game
    state.lebron.points = total
    average = total / len(state.games)
    state.lebron.the_goat = average >= 25
    state.lebron.wins = wins
    state.lebron.games_played = len(state.games)
    state.lebron.record = str(wins) + "-" + str(len(state.games) - wins)
    if ideal_stats == "points":
      state.current_stat = str(state.lebron.points)
    elif ideal_stats == "wins":
      state.current_stat = str(state.lebron.wins)
    elif ideal_stats == "games played":
      state.current_stat = str(state.lebron.games_played)
    else:
      state.current_stat = str(state.lebron.record)
    return stats_page(state)
        
    


start_server(State(
    0,
    [Game("Boston Celtics", 27, True)],
    "Fan",
    Lebron(0, "Lebron James", True, 0, 0, ""),
    [],
    0,
    ""
    
))
