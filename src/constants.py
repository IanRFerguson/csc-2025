TEAM_INITIALS = ["MIL", "ATL", "NYK"]

# TEAM_INITIALS += ["LAL", "BOS", "MIA"]

YEARS = range(2020, 2026)

BUCKET_NAME = "csc-scratch"
PREFIX = "nba_data/"
DESTINATION_DATASET_NAME = "csc_main"
DESTINATION_TABLE_NAME = "nba_player_data"

BASE_URL = "https://www.basketball-reference.com/teams/{team_initials}/{year}.html"
