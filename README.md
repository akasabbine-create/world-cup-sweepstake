# World Cup Sweepstake Dashboard Starter

A starter GitHub Pages + GitHub Actions project for an automated World Cup sweepstake dashboard.

## What it does
- Fetches World Cup fixtures/results from API-Football
- Normalises team names
- Scores players based on teams they own
- Adds knockout, goals, clean-sheet, and bonus logic hooks
- Generates `data/state.json` for the website
- Publishes a Sky Sports-style dashboard via GitHub Pages

## Quick start
1. Create a new GitHub repository.
2. Upload all files from this folder.
3. In GitHub, go to Settings > Secrets and variables > Actions > New repository secret.
4. Add:
   - `RAPIDAPI_KEY` = your API-Football key
5. Edit `data/players.json` with your sweepstake players and teams.
6. Enable GitHub Pages from the repository root or `/docs` depending on your setup.
7. Run the workflow manually from the Actions tab.

## Local test
```bash
pip install -r requirements.txt
python scripts/update.py
python -m http.server 8000
```
Then open `http://localhost:8000`.

## Important
The API league/season IDs may need confirming before the tournament starts. Start with the API-Football dashboard/docs and update `scripts/fetch_matches.py` if required.
