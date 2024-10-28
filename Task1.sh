#!/bin/bash/

# Check if $2 (second argument) exists
if [ -z "$2" ]; then
    # Run Task1.py with only $1 if $2 is missing
    python3 Task1.py "$1"
else
    # Run Task1.py with $1, $2, and optionally $3
    python3 Task1.py "$1" "$2" "$3"
fi

# Run unit tests and redirect errors to test_report.log
python3 -m unittest ./TestTask1.py 2> test_report.log

