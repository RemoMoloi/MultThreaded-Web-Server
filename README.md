# Multi-Threaded Python Web Server (Assignment 1 - Remotlotlo Moloi)

## Overview
This project implements a simplified multi-threaded web server in Python.

## Features
- Multi-threaded handling of client requests
- Thread synchronization (logging with locks)
- Simple scheduling with worker thread pool
- Memory management (queue-based connections)
- File serving from `www/`
- Logging of requests and responses

## How to run
1. Ensure Python 3.9+ is installed.
2. Run: `python3 server.py`
3. Access: `http://localhost:8080/`

## Test
Open multiple browser tabs or use tools like `ab` (Apache Benchmark) or `wrk` to simulate load.
