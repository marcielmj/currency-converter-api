#!/bin/sh

if type pipx > /dev/null 2>&1; then
    echo "Installing project dependencies..."
    pipx install hatch
    hatch dep show requirements --all | xargs pip install --user
fi
