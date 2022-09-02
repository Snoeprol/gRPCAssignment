#!/bin/bash

# This makes sures output is shown in the terminal
export PYTHONUNBUFFERED=true

n=10
for ((i = 1; i <= $n ; i++)); 
do
    python ./async_greeter_client.py &
done

wait