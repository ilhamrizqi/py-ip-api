#!/usr/bin/python

import json
import socket
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/ip')
def show_ip():
    if request.headers.getlist("X-Forwarded-For"):
       ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
       ip = request.remote_addr
       
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except Exception as e:
        hostname = ''
    
    return jsonify({'ip': ip, 'hostname': hostname}), 200

@app.route('/port/<int:port>')
def port_status(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = request.remote_addr
    try:
        s.connect((ip, port))
        status = True
        s.close()
    except Exception:
        status = False

    return jsonify({'port': port, 'open': status}), 200
