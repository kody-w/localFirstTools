#!/bin/bash
docker build -t level-1-container .
docker run -d --name level-1-app -p 3001:3000 level-1-container
echo "Level 1 Container running at http://localhost:3001"
