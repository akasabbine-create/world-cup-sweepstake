from engine.normaliser import normalise
from engine.tournament import detect_stage, match_winner


def owners_of(team, players):
    return [p["name"] for p in players if team in [normalise(t) for t in p.get("teams", [])]]


def generate_match_events(match, players, match_index):
    events = []
    stage = detect_stage(match_index)
    t1 = normalise(match["team1"])
    t2 = normalise(match["team2"])
    s1 = match.get("score1")
    s2 = match.get("score2")

    events.append({
        "type": "FULL_TIME",
        "stage": stage,
        "text": f"{t1} {s1}-{s2} {t2}"
    })

    winner = match_winner(match)
    if winner:
        for player in owners_of(winner, players):
            events.append({
                "type": "POINTS",
                "stage": stage,
                "text": f"{player} gains points from {winner}"
            })

    return events
