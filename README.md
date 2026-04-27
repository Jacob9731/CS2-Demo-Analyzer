# CS2 Demo Analyzer

This project analyzes Counter-Strike 2 (.dem) files and generates player statistics.

## Features
- Parses demo files using demoparser2
- Displays player stats (Kills, Deaths, K/D, HS%, ADR)
- Shows first 10 kill events
- Exports stats to CSV
- Generates graphs:
  - Top 5 Kills
  - Top 5 K/D
  - Headshot %

## How to Run
1. Install dependencies:
pip install -r requirements.txt

2. Run the program:
python analyzer.py

3. Enter your demo file path when prompted

## Example Output
(Add screenshots here)

## Future Improvements
- GUI interface
- More advanced stats (entry kills, clutch stats)
- Web dashboard (Flask)

## Status
Completed (Final Project)
