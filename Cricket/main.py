
# Cricket Tournament Points Table and Net Run Rate Calculator

def overs_to_float(overs, balls):
    return overs + balls / 6

def get_adjusted_overs(overs, balls, wickets):
    actual_overs = overs_to_float(overs, balls)
    if wickets == 10 and actual_overs < 20:
        return 20.0
    return actual_overs

def calculate_nrr(team):
    if team["overs_faced"] == 0 or team["overs_bowled"] == 0:
        return 0.0
    run_rate_scored = team["runs_scored"] / team["overs_faced"]
    run_rate_conceded = team["runs_given"] / team["overs_bowled"]
    return run_rate_scored - run_rate_conceded

def validate_team_name(name, teams):
    if name.strip() == "" or name in teams:
        return False
    return True

def validate_match_data(runs, wickets, overs, balls):
    if runs < 0:
        return False
    if wickets < 0 or wickets > 10:
        return False
    if overs < 0 or overs > 20:
        return False
    if balls < 0 or balls > 5:
        return False
    if overs == 20 and balls > 0:
        return False
    return True

def display_points_table(teams):
    standings = []
    for team_name, data in teams.items():
        nrr = calculate_nrr(data)
        standings.append({
        "team": team_name,
        "played": data["played"],
        "won": data["won"],
        "lost": data["lost"],
        "tied": data["tied"],
        "points": data["points"],
        "runs_scored": data["runs_scored"],
        "runs_given": data["runs_given"],
        "overs_faced": data["overs_faced"],
        "overs_bowled": data["overs_bowled"],
        "nrr": nrr
        })
    standings.sort(key=lambda team: (team["points"], team["nrr"]), reverse=True)
    print("\n" + "=" * 150)
    print("FINAL TOURNAMENT STANDINGS")
    print("=" * 150)
    print(f"{'Pos':<5}{'Team':<20}{'Played':<10}{'Won':<8}{'Lost':<8}{'Tied':<8}{'Points':<10}{'Runs Scored':<15}{'Runs Given':<15}{'Overs Faced':<15}{'Overs Bowled':<15}{'NRR':<10}")
    for position, team in enumerate(standings, start=1):
        print(f"{position:<5}{team['team']:<20}{team['played']:<10}{team['won']:<8}{team['lost']:<8}{team['tied']:<8}{team['points']:<10}{team['runs_scored']:<15}{team['runs_given']:<15}{team['overs_faced']:<15.2f}{team['overs_bowled']:<15.2f}{team['nrr']:<10.3f}")

# Team registration
while True:
    try:
        no_of_teams = int(input("Enter the number of teams playing: "))
        if no_of_teams < 2:
            print("Number of teams must be at least 2.")
            continue
        break
    except ValueError:
        print("Enter a valid whole number.")

teams = {}
for i in range(no_of_teams):
    while True:
        team_name = input(f"Enter the team-{i + 1} name: ").strip()
        if not validate_team_name(team_name, teams):
            print("Team name cannot be empty or duplicated.")
            continue
        teams[team_name] = {
            "played": 0, "won": 0, "lost": 0, "tied": 0,
            "points": 0, "runs_scored": 0, "runs_given": 0,
            "overs_faced": 0.0, "overs_bowled": 0.0
        }
        break

# Match calculation
no_of_matches = no_of_teams * (no_of_teams - 1)
pair_count = {}
completed_matches = 0

while completed_matches < no_of_matches:
    match_num = completed_matches + 1
    print(f"\n{'=' * 60}\nEnter details for match {match_num}\n{'=' * 60}")
    team1 = input("Enter the first team played name: ").strip()
    team2 = input("Enter the second team played name: ").strip()

    if team1 not in teams or team2 not in teams:
        print("Invalid team name entered.")
        continue
    if team1 == team2:
        print("A team cannot play against itself.")
        continue

    pair = tuple(sorted((team1, team2)))
    if pair_count.get(pair, 0) >= 2:
        print("These two teams have already played twice.")
        continue

    try:
        score_1st_innings = int(input("First team's total runs scored: "))
        wickets_1st_innings = int(input("First team's wickets lost: "))
        overs_1st_innings = int(input("First team's overs faced: "))
        balls_1st_innings = int(input("First team's remaining balls (0-5): "))
        score_2nd_innings = int(input("Second team's total runs scored: "))
        wickets_2nd_innings = int(input("Second team's wickets lost: "))
        overs_2nd_innings = int(input("Second team's overs faced: "))
        balls_2nd_innings = int(input("Second team's remaining balls (0-5): "))
    except ValueError:
        print("Invalid numeric input. Please enter whole numbers.")
        continue

    valid1 = validate_match_data(score_1st_innings, wickets_1st_innings, overs_1st_innings, balls_1st_innings)
    valid2 = validate_match_data(score_2nd_innings, wickets_2nd_innings, overs_2nd_innings, balls_2nd_innings)

    if not valid1 or not valid2:
        print("Invalid match data entered. Please re-enter the match.")
        continue

    adjusted_overs1 = get_adjusted_overs(overs_1st_innings, balls_1st_innings, wickets_1st_innings)
    adjusted_overs2 = get_adjusted_overs(overs_2nd_innings, balls_2nd_innings, wickets_2nd_innings)

    teams[team1]["played"] += 1
    teams[team2]["played"] += 1
    teams[team1]["runs_scored"] += score_1st_innings
    teams[team1]["runs_given"] += score_2nd_innings
    teams[team2]["runs_scored"] += score_2nd_innings
    teams[team2]["runs_given"] += score_1st_innings
    teams[team1]["overs_faced"] += adjusted_overs1
    teams[team1]["overs_bowled"] += adjusted_overs2
    teams[team2]["overs_faced"] += adjusted_overs2
    teams[team2]["overs_bowled"] += adjusted_overs1

    if score_1st_innings > score_2nd_innings:
        teams[team1]["won"] += 1
        teams[team1]["points"] += 2
        teams[team2]["lost"] += 1
    elif score_2nd_innings > score_1st_innings:
        teams[team2]["won"] += 1
        teams[team2]["points"] += 2
        teams[team1]["lost"] += 1
    else:
        teams[team1]["tied"] += 1
        teams[team2]["tied"] += 1
        teams[team1]["points"] += 1
        teams[team2]["points"] += 1

    pair_count[pair] = pair_count.get(pair, 0) + 1
    completed_matches += 1
    print("Match recorded successfully.")

# Tournament validation
tournament_complete = all(
    pair_count.get(tuple(sorted((team1, team2))), 0) == 2
    for i, team1 in enumerate(teams)
    for team2 in list(teams)[i + 1:]
)

if tournament_complete:
    display_points_table(teams)
else:
    print("Tournament is not complete.")
