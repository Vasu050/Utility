# Windows Process Monitoring System

## Overview
This project is a Windows Process Monitoring System that consists of three main components:

1. **Agent (EXE)**: Collects running process information from a Windows machine and sends it to the backend.
2. **Backend (Django)**: REST API that receives process data and stores it in a SQLite database.
3. **Frontend (HTML/JS)**: Web interface that displays the process hierarchy and latest data.

The system allows monitoring of processes, their subprocesses, CPU/memory usage, and hostname information in an interactive and user-friendly interface.

## Features

- Collects process name, PID, CPU usage, memory usage, and parent-child relationships.
- Sends data to a Django REST API.
- Hostname identification for machines.
- Web interface with expandable/collapsible process tree.
- Timestamped data display with refresh capability.
- Simple API key authentication for agent.
- Clean, responsive UI.
- Search Functionality to search processesses.

## Architecture Overview

[Windows Machine]
|
[Agent EXE]
|
REST API (Django)
|
SQLite Database
|
Frontend (HTML/JS)

## Future Enhancements
- Currently same data is getting updated for processes everytime we run exe, this is done to improve visibility and only get latest updates and not get older updates or offline users details. So we can implement filter to get historical data as well.
- Visualisation using charts or graphs or processes.
- we can fetch data at regular intervals and update the frontend if data changes or can use web sockets to build a persistent connection.
  
