from engine.normaliser import normalise

POINTS = {
    "group_win": 3,
    "group_draw": 1,
    "round_of_32": 5,
    "round_of_16": 5,
    "quarter_final": 5,
    "semi_final": 10,
    "final": 10,
    "winner": 15,
    "top_scoring_nation": 5,
    "golden_boot_team": 5,
    "knockout_clean_sheet": 2
}


def detect_stage(match_index: int) -> str:
    """Detect World Cup 2026 stage by completed-match index.

    48-team World Cup format:
    - 72 group matches
    - 16 round-of-32 matches
    - 8 round-of-16 matches
    - 4 quarter-finals
    - 2 semi-finals
    - 1 third-place match
    - 1 final
    """
    number = match_index + 1
    if number <= 72:
        return "group"
    if number <= 88:
        return "round_of_32"
    if number <= 96:
        return "round_of_16"
    if number <= 100:
        return "quarter_final"
    if number <= 102:
        return "semi_final"
    if number == 103:
        return "third_place"
    return "final"


def match_winner(match: dict):
    t1 = normalise(match["team1"])
    t2 = normalise(match["team2"])
    s1 = match.get("score1")
    s2 = match.get("score2")

    if s1 is None or s2 is None:
        return None
    if s1 > s2:
        return t1
    if s2 > s1:
        return t2
    return match.get("winner")
