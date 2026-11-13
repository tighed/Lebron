from drafter import *
from dataclasses import dataclass


@dataclass
class Game:
    """general information about the game from Lebron's season"""
    opponent: str
    points: int
    win: bool


@dataclass
class Lebron:
    """ Lebron's stats stored in its own place"""
    points: int
    full_name: str
    the_goat: bool
    
@dataclass
class State:
    """ Everything the site must remember between pages"""
    correct_answers: int
    games: list[Game]
    player_name: str
    lebron: Lebron

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


@route
def index(state: State) -> Page:
    return Page(state, [
        Header("Welcome to Lebron quiz! \n WE LOVE LEBRON", 1),
        Button("Start Quiz", "start_quiz"),
        Button("Stats", "stats_page"), 
    ])


@route
def start_quiz(state: State) -> Page:
    state.correct_answers = 0
    return Page(state, [
        Header("Quiz", 1),
        "Is Lebron the goat?",
        Button("Yes", "answer_yes"),
        Button("No", "answer_no")
    ])


@route
def answer_yes(state: State) -> Page:
    return Page(state, [
        "Correct answer!",
        Button("Home", "index"),
    ])

@route
def answer_no(state: State) -> Page:
    return Page(state, [
        "Incorrect. Try again.",
        Button("Try again", "start_quiz"),
    ])

@route
def stats_page(state: State) -> Page:
    total = 0
    for game in state.games:
        total = total + game.points
    state.lebron.points = total
    return Page(state, [
        Header(state.lebron.full_name + str(state.lebron.points), 1),
        Button("Home", "index"),
    ])



start_server(State(0, [Game("Boston Celtics", 27, True)], "Fan", Lebron("LeBron James", 27.0, False)))
