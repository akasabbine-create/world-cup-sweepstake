import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from engine.events import generate_match_events
from engine.normaliser import normalise
from engine.tournament import POINTS, detect_stage, match_winner

ROOT = Path(__file__).resolve().parents[1]


def load_json(path, fallback):
    path = ROOT / path
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path, data):
    path = ROOT / path
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def player_owns_team(player, team):
    return normalise(team) in [normalise(t) for t in player.get("teams", [])]


def add_points(scores, players, team, points, reason):
    team = normalise(team)
    for player in players:
        if player_owns_team(player, team):
            scores[player["name"]] += points


def calculate(players, matches):
    scores = defaultdict(int)
    goals_by_team = defaultdict(int)
    clean_sheets = defaultdict(int)
    events = []

    normalised_matches = []

    for idx, raw_match in enumerate(matches):
        match = dict(raw_match)
        match["team1"] = normalise(match["team1"])
        match["team2"] = normalise(match["team2"])
        normalised_matches.append(match)

        stage = detect_stage(idx)
        t1, t2 = match["team1"], match["team2"]
        s1, s2 = match.get("score1"), match.get("score2")
        if s1 is None or s2 is None:
            continue

        goals_by_team[t1] += s1
        goals_by_team[t2] += s2

        if stage == "group":
            if s1 > s2:
                add_points(scores, players, t1, POINTS["group_win"], "group win")
            elif s2 > s1:
                add_points(scores, players, t2, POINTS["group_win"], "group win")
            else:
                add_points(scores, players, t1, POINTS["group_draw"], "group draw")
                add_points(scores, players, t2, POINTS["group_draw"], "group draw")
        elif stage != "third_place":
            # Advancement/appearance points for teams reaching each knockout round.
            stage_points = POINTS.get(stage, 0)
            add_points(scores, players, t1, stage_points, stage)
            add_points(scores, players, t2, stage_points, stage)

            winner = match_winner(match)
            if stage == "final" and winner:
                add_points(scores, players, winner, POINTS["winner"], "winner")

            if s2 == 0:
                clean_sheets[t1] += 1
            if s1 == 0:
                clean_sheets[t2] += 1

        events.extend(generate_match_events(match, players, idx))

    if goals_by_team:
        max_goals = max(goals_by_team.values())
        top_scoring_teams = [team for team, goals in goals_by_team.items() if goals == max_goals]
        for team in top_scoring_teams:
            add_points(scores, players, team, POINTS["top_scoring_nation"], "top scoring nation")
    else:
        top_scoring_teams = []

    for team, count in clean_sheets.items():
        add_points(scores, players, team, count * POINTS["knockout_clean_sheet"], "knockout clean sheets")

    leaderboard = sorted(
        [
            {
                "rank": None,
                "name": player["name"],
                "teams": player.get("teams", []),
                "points": scores[player["name"]]
            }
            for player in players
        ],
        key=lambda row: row["points"],
        reverse=True
    )

    for i, row in enumerate(leaderboard, start=1):
        row["rank"] = i

    insights = {
        "top_scoring_teams": top_scoring_teams,
        "goals_by_team": dict(sorted(goals_by_team.items())),
        "clean_sheets": dict(sorted(clean_sheets.items())),
        "wooden_spoon": leaderboard[-1]["name"] if leaderboard else None,
        "leader": leaderboard[0]["name"] if leaderboard else None
    }

    return {
        "leaderboard": leaderboard,
        "matches": normalised_matches,
        "events": events[-25:],
        "insights": insights,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


if __name__ == "__main__":
    players = load_json("data/players.json", [])
    matches = load_json("data/live_matches.json", [])
    state = calculate(players, matches)
    save_json("data/state.json", state)
    save_json("data/leaderboard.json", state["leaderboard"])
