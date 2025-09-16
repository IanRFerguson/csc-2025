from sklearn.linear_model import LinearRegression
import pandas as pd
from sklearn.model_selection import train_test_split

MODEL_FEATURES = [
    "age",
    "games_played",
    "minutes_played",
    "field_goal_percentage",
    "field_goals_attempted",
    "three_point_field_goal_percentage",
    "three_point_field_goals_attempted",
]


# NOTE - dbt and session are required parameters for dbt models
def model(dbt, session):
    # Load the data
    df = dbt.ref("stg_nba__player_data").to_pandas()

    # Select features and target variable
    features = df[MODEL_FEATURES]
    target = df["points"]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42
    )

    # Create and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Fit the regression model to the full dataset
    _prediction_set = df[MODEL_FEATURES]
    _predicted_points = model.predict(_prediction_set)

    df["predicted_points"] = _predicted_points

    return df
