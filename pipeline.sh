#!/bin/bash
#pipeline to execute tasks
#Step 1: execute unit test 
#Step 2 : based on unit test outcome, actual kpi logic will be derived

#Removing checkpoint dirctory to support streaming logic as new data is not ingested yet
rm -rf /var/jenkins_home/workspace/checkpoint/

# Run unit tests
echo "Running unit tests..."
cd /usr/lib/python3.9/

python3 /var/jenkins_home/workspace/ikea_assignment/test.py 
unit_test_exit_code=$?

# Check if unit tests passed
if [ $unit_test_exit_code -eq 0 ]; then
  python3 /var/jenkins_home/workspace/ikea_assignment/twitter.py 
  code_execution_exit_code=$?
  if [ $code_execution_exit_code -eq 0 ]; then
 	:
  fi
else
  echo "Unit tests failed . Code execution skipped."
fi
