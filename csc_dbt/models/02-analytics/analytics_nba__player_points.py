from sklearn.linear_model import LinearRegression
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
    # Load the required columns to train our model
    target_columns = MODEL_FEATURES + ["points", "player_id"]
    df = dbt.ref("stg_nba__player_data").select(*target_columns).toPandas()

    # A little naive but we'll impute 0's for missing data
    df.fillna(0, inplace=True)

    # Select features and target variable
    features = df[MODEL_FEATURES]

    target = df["points"].fillna(0)

    # Split the data into training and testing sets
    X_train, _, y_train, _ = train_test_split(
        features, target, train_size=0.3, random_state=101
    )

    # Create and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Fit the regression model to the full dataset
    _prediction_set = df[MODEL_FEATURES]
    _predicted_points = model.predict(_prediction_set)

    df["predicted_points"] = _predicted_points

    return df
