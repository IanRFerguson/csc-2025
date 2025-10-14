import os

STEP_TWO = os.environ.get("DEMO_STEP") == "2"

TEAM_INITIALS = ["MIL", "ATL", "NYK"]

# When we run the pipeline a second time we'll
# add in these additional team
if STEP_TWO:
    TEAM_INITIALS += ["LAL", "BOS", "MIA"]

YEARS = range(2020, 2026)

BUCKET_NAME = "csc-scratch"
PREFIX = "nba_data/"
BACKUP_PREFIX = "nba_data_backup/"
DESTINATION_DATASET_NAME = "csc_main"
DESTINATION_TABLE_NAME = "nba_player_data"

BASE_URL = "https://www.basketball-reference.com/teams/{team_initials}/{year}.html"
