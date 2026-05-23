# Overview

Task Sync Server is a client-server networking program that allows a client to send task-management 
requests to a server. The program uses a Python TCP server and a Python command-line client. The 
client sends JSON-formatted requests, and the server processes those requests, updates or reads task 
data from a local `tasks.json` file, and sends a JSON response back to the client.

To use the software, open two terminals in the project folder using VS Code.

Start the server first: python server.py

Start the client: python client.py // Will display a menu option that is accessed using numbers 1 - 6, then hit enter.

The purpose of this software was to better understand how separate programs communicate over a network and how to better use json files. 
This project was intended as a learning project that will eventually be incorporated into another larger project.

[Software Demo Video](https://youtu.be/3cfYTT2mRbs)

# Network Communication

This project uses a client server architecture. The server runs first and waits for incoming client 
requests. The client connects to the server, sends 1 request, receives 1 response and then displays 
the result to the user.

The program uses TCP and runs on:
Host: 127.0.0.1
Port: 5050

The server stays on port 5050. The client may use a temporary local port for each request, which is handled automatically by the operating system.

Messages are sent between the client and the server using json formatted text over TCP. The client builds a json request 
based on users menu choice. The server validates the request and performs the correct action and then 
returns a json response.

# Development Environment

I used VS Code to build this project. The programming language is Python. 

Python libraries used:
socket
json
os
unittest
threading
time

This project also includes a test harness:
python run_tests.py

This will run the full suite including task manager tests, json protocol tests and tcp client server integration tests.

# Useful Websites

* [Python Server Libraries](https://docs.python.org/3.6/library/socketserver.html)
* [Python Socket Libraries](https://docs.python.org/3/library/socket.html)
* [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)

# Future Work

* Add graphical user interface.
* Connect the server to a web or mobile client for remote task management.
* Add security features to prevent unauthorized usage.
* Add a list of all incomplete tasks to List Tasks option in main menu so users know what is available.