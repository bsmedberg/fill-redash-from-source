# fill-redash-from-source

A tool to generate redash queries from a source-controlled, reviewable, pull-requestable repository.

## Usage Instructions

### To log to Mozilla re:dash and find your API key

* Visit https://sql.telemetry.mozilla.org/
* Choose "Log In with Google"
* Log in with your *@mozilla.com address. For privacy reasons, re:dash query access is currently limited to Mozilla employees.
* In the upper right corner choose your name and open settings.
* In the "API Key" tab you can copy your API key. **Keey your API key secret; do not share it with anyone.**

### To modify an existing query:

* edit autogen.yaml with your changes
* run `python autogen.py autogen.yaml *API_KEY*` using your API key from above
* Unless you are a re:dash admin, you will only be able to make changes to the queries that you created.

### To create a new query

This tool does not make brand-new queries. To create a new query, you create a dummy query in re:dash and then update it using the tool

* Visit https://sql.telemetry.mozilla.org/queries/new
* Choose the data source you need (most queries use the "Presto" datasource)
* Type in a dummary query such as `SELECT TRUE`.
* Choose the "execute" button.
* After the query has finished executing, choose the "Save" button.
* The URL will change to contain the new query ID: https://sql.telemetry.mozilla.org/queries/*id*/source
* Next to the save button is a hamburger menu which has a "Show API Key" menu item. Copy the query API key.
* In `autogen.yaml`, create a new query definition using the query ID and query API key from above.
* It may be useful to prototype the query text in the re:dash UI before copying it to the YAML.

## About API Keys ##

There are two different kinds of API keys in re:dash:

* The **user API key** allows a script to impersonate a user and make changes on their behalf. This is what `autogen.py` uses to update queries. You should keep your user API key secret.
* The **query API key** allows anyone to view a query and query results. You use this API key to publish query results using URLs such as https://sql.telemetry.mozilla.org/api/queries/*id*/results.json?api_key=*query-api-key* (you can also use .csv and .xslx)
