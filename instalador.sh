#!/bin/bash

# Update package lists
sudo apt update

# Install pipx
sudo apt install -y pipx

# Ensure pipx is in the PATH
pipx ensurepath

# Install Poetry using pipx
pipx install poetry

# Install dependencies using Poetry
poetry install

# Activate the virtual environment
poetry shell