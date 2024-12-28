#!/bin/sh

echo "Setting up the environment..."
apt-get update 
apt-get install -y python3 python3-pip
pip install elasticsearch

echo "Indexing csv file..."
python3 /usr/elastic-backend/cv-index.py
python3 /usr/elastic-backend/test-cv-index.py