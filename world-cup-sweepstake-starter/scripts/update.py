import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(command):
    subprocess.run(command, cwd=ROOT, check=True)


if __name__ == "__main__":
    print("Fetching live matches...")
    run([sys.executable, "scripts/fetch_matches.py"])

    print("Calculating leaderboard/state...")
    run([sys.executable, "-m", "engine.scorer"])

    print("Done.")
