# User Documentation of MarconiBB
##### Created By: Marcon D. - Strambini E. - Tezza G.

# .1 Introduction
MarconiBB is a quick and easy solution that allows teachers and students to book rooms inside the institute, while keeping low the paper usage and the overall time consuming process of booking a room by hand. This document will provide instructions for accessing the application code and installing it into a simulator or compatible device.

# .2 Hardware and Software Requirements
- A Raspberry PI 2+ or better with Raspbian Installed
- Docker and python3+ installed
- RFID Reader

# .3 Starting the rfid reader
1. `cd` into the project folder
2. run `sudo python3 ReaderDeamon.py` while the reader is attached to the corresponding pins


# .4 Docker setup
1. Start the `dockerd` deamon with the right priviledges
2. `cd` into the project folder
3. run `docker-compose build --no-cache`
4. run `docker-compose up`
5. now the webserer is exposed on `localhost:5000`
 

# .5 System Maintenance
1. Flask Code
   1. The files are organized in /flask/
   2. Inside the templates folder there are all the jinjia2 templates
   3. The app.py takes care of all the logic and rounting needed
