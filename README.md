![image](https://user-images.githubusercontent.com/2151412/199124070-e5619c84-4cd0-445a-a198-6ee1078595f6.png)
# Meteorite map
### Introduction
This project gets data of the [Meteorite Landings NASA dataset](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh) and displays its position through the globe, in an interactive way.

Each meteorite type is displayed by using a different color, and each marker has a size relative to the meteorite mass (the bigger the meteorite, the bigger the marker size)

### How to use
First, you need to set your Tinybird auth token in the code. This will let it automatically create your datasources and pipes, which will later be used to query for the corresponding meteorites.

The token has to be set in `app.py`, in the following line:

```python
TINYBIRD_TOKEN = 'REPLACE THIS WITH YOUR TOKEN'
```

Then, install the project dependencies:

```
poetry install
```

And finally, to generate the map, execute the command that will download and process the data and visualize it

```
python app.py
```

Once the preparation finishes, the interactive map will open in your browser, ready for you to explore it!
