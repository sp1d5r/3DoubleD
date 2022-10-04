#! /bin/bash

flask --app db/flash-server run &
python3 main.py &
python3 3d-rendering/3d-cube.py

