#!/bin/bash
nc -l -p 5000 -k -c '/bin/cat'
# | tee ./shell_echo.txt
