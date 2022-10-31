import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

import plotly.express as px
import requests



TINYBIRD_TOKEN = 'REPLACE THIS WITH YOUR TOKEN'
auth_headers = {'Authorization': f"Bearer {TINYBIRD_TOKEN}"}

###### PROCESSING

logging.info('Creating the datasource in Tinybird...')
datasource_url = 'https://data.nasa.gov/resource/gh4g-9sfh.csv'
requests.post('https://api.tinybird.co/v0/datasources', data={'url': datasource_url, 'name': 'meteor_landings', 'mode': 'replace'}, headers=auth_headers)

logging.info('Creating a pipe and preparing to operate with our data...')
# From my experience, Tinybird doesn't get the column names correctly from the CSV, 
# hence why we need to set them manually
PIPE_NAME = 'meteor_landing_pipe'
column_names = ['name', 'id', 'nametype', 'recclass', 'mass', 'fall', 'year', 'reclat', 'reclong']
query = "SELECT " + ", ".join(f"column_{i:02} as {column_name}" for i, column_name in enumerate(column_names)) + " FROM meteor_landings"
create_pipe_body = {'name': PIPE_NAME, 'sql': query}
requests.post('https://api.tinybird.co/v0/pipes', headers=auth_headers, data=create_pipe_body)

logging.info('Creating an endpoint and getting the data...')
requests.post(f"https://api.tinybird.co/v0/pipes/{PIPE_NAME}/nodes/{PIPE_NAME}_0/endpoint", headers=auth_headers)
sql_query = """
SELECT name, reclat as lat, reclong as lon, toFloat32(mass) as mass, recclass as meteor_type, year
FROM (
    SELECT *
    FROM meteor_landing_pipe
    WHERE reclat IS NOT NULL AND reclong IS NOT NULL AND mass <> ''
)
ORDER BY mass DESC
FORMAT JSON
""".strip()
response = requests.get('https://api.tinybird.co/v0/sql', headers=auth_headers, params={'q': sql_query})
data = response.json()['data']


####### VIZ

logging.info('Visualizing data...')
# The meteor with the highest mass is several orders of magnitude bigger than the rest,
# so we'll exclude it to avoid making the data hard to visualize
usable_data = data[1:]
fig = px.scatter_geo(usable_data, lat="lat", lon="lon", hover_name="name", size="mass", color="meteor_type")
fig.update_geos(projection_type="orthographic")
fig.show()