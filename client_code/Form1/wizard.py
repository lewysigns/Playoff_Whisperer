import anvil.http
#from collections import Counter
#from itertools import product


def fetch_matchups(league_id, week):
    """
    Fetch matchups for a specific week from the Sleeper API.
    """
    url = f"https://api.sleeper.app/v1/league/{league_id}/matchups/{week}"
    return anvil.http.request(url,json=True)

def fetch_rosters(league_id):
    """
    Fetch rosters and team IDs for a league.
    """
    url = f"https://api.sleeper.app/v1/league/{league_id}/rosters"
    return anvil.http.request(url,json=True)

def fetch_users(league_id):
    """
    Fetch user details (team names) for a league.
    """
    url = f"https://api.sleeper.app/v1/league/{league_id}/users"
    return anvil.http.request(url,json=True)

def build_weekly_matchups(league_id, start_week, end_week):
    """
    Fetch matchups for all weeks between start_week and end_week.
    """
    matchups = []
    for week in range(start_week, end_week + 1):
        week_data = fetch_matchups(league_id, week)
        weekly_matchups = []
        for matchup in week_data:
            if matchup.get("matchup_id"):
                team1 = matchup.get("roster_id")
                team2 = matchup.get("opponent_roster_id")
                if team1 and team2:
                    weekly_matchups.append((team1, team2))
        matchups.append(weekly_matchups)
    return matchups

def calculate_playoff_percentages(permutations, current_records):
    """
    Calculate playoff percentages based on match permutations and current records.
    """
    playoff_appearances = Counter()
    total_permutations = len(permutations)
    
    for scenario in permutations:
        updated_records = current_records.copy()
        for matchup, winner in scenario.items():
            updated_records[winner] += 1
        sorted_teams = sorted(updated_records.items(), key=lambda x: (-x[1], x[0]))
        top_teams = [team for team, _ in sorted_teams[:6]]
        for team in top_teams:
            playoff_appearances[team] += 1
    
    return {team: (playoff_appearances[team] / total_permutations) * 100
            for team in current_records.keys()}

def get_odds(league_id, current_week, final_week):
    # Fetch league data
    rosters = fetch_rosters(league_id)
    users = fetch_users(league_id)
    
    # Map roster IDs to team names
    roster_to_team = {roster['roster_id']: next(
        user['display_name'] for user in users if user['user_id'] == roster['owner_id'])
        for roster in rosters}

    # Initialize current records
    current_records = {roster_to_team[roster['roster_id']]: roster['settings']['wins'] 
                       for roster in rosters}

    # Fetch weekly matchups
    weekly_matchups = build_weekly_matchups(league_id, current_week, final_week)
    all_matchups = [match for week in weekly_matchups for match in week]
    
    # Generate permutations
    outcomes = [list(matchup) for matchup in all_matchups]
    all_permutations = list(product(*outcomes))
    formatted_permutations = [
        {all_matchups[i]: combination[i] for i in range(len(all_matchups))}
        for combination in all_permutations
    ]
    
    # Calculate playoff percentages
    playoff_percentages = calculate_playoff_percentages(formatted_permutations, current_records)
    
    # Print results
    for team, percentage in playoff_percentages.items():
        print(f"{team}: {percentage:.2f}% chance of making the playoffs")