#!/bin/bash

# Run unit tests
echo "Running unit tests..."
cd /usr/lib/python3.9/

python3 /var/jenkins_home/workspace/ikea_assignment/test.py 
unit_test_exit_code=$?

# Check if unit tests passed
if [ $unit_test_exit_code -eq 0 ]; then
  echo "Unit tests passed."
  
  # Run code execution
  echo "Running code execution..."
  python3 /var/jenkins_home/workspace/ikea_assignment/twitter.py unit_test_exit_code=$?
  code_execution_exit_code=$?
  
  # Check if code execution completed successfully
  if [ $code_execution_exit_code -eq 0 ]; then
    echo "Code execution completed successfully."
  else
    echo "Code execution failed with exit code $code_execution_exit_code."
  fi
else
  echo "Unit tests failed with exit code $unit_test_exit_code. Code execution skipped."
fi
