# Changemakers dbt

## Anatomy of a dbt Project
* The [dbt Project YAML](./dbt_project.yml) defines where everything lives in your project, and how dbt should build it
* The [profiles YAML](./profiles.yml) handles our authentication and our connection to the warehouse
* The [target directory](./target/) has all of our compiled SQL - this is what the dbt models look like once we run our pipeline


## Using dbt

```bash
# Install our dependencies
dbt deps

# Run a basic pipeline
dbt build

# Run a more complicated pipeline
dbt build --vars '{"RUN_ML_MODELS": "true"}'

# You can build individual models
dbt build --select stg_nba__knicks_players

# You can build all the models UPSTREAM of a model
dbt build --select +stg_nba__knicks_players

# You can build all the models DOWNSTREAM of a model
dbt build --select stg_nba__knicks_players+

# You can build an entire path of models
dbt build --select path:models/03-reporting

# If you just want to create the models without testing
dbt run

# If you just want to test without recreating the models
dbt test
```


## dbt Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
