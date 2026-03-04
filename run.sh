#!/bin/bash

set -e

echo "Instalando dependências do frontend..."
cd Front
npm i

echo "Iniciando frontend..."
npm run dev &

FRONT_PID=$!

cd ..

echo "Iniciando solver..."
cd Solver
uv run main.py

wait $FRONT_PID
