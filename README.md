# sf-citibike-simple-streamlit

### A super simple Streamlit that reads from Snowflake and renders visuals

Pre-reqs: Setup [Citibike](https://github.com/snowflakecorp/citibike) on your Snowflake account.

Steps to run:

1. Download the zip, uncompress
2. Install the requirements:

```
pip install -r requirements.txt
```

3. Create a folder called `.streamlit` in the same folder and add a file called `secrets.toml` with the below content:

```
# .streamlit/secrets.toml

[snowflake]
account = "<your_snowflake_locator>"
user = "<username>"
password = "<password>"


```

4. Execute the program as below:

```
streamlit run st_sp_citibike_ex_helper.py
```
