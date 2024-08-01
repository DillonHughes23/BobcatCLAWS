#!/bin/bash

# Store the custom path in a different variable, not to overwrite the system PATH
PROJECT_PATH="/home/workspace/Software-Engineering-Project-Course"

NODE_EXECUTABLE="/usr/local/bin/node"  # Replace with actual path
PYTHON_EXECUTABLE="/usr/bin/python3"  # Replace with actual path

# call API script
$NODE_EXECUTABLE "${PROJECT_PATH}/scripts/api_scripts/wmAPI.js"
$NODE_EXECUTABLE "${PROJECT_PATH}/scripts/api_scripts/tAPI.js"
$PYTHON_EXECUTABLE "${PROJECT_PATH}/scripts/api_scripts/Parsehub.py"
$PYTHON_EXECUTABLE "${PROJECT_PATH}/scripts/api_scripts/bluecartAPI.py"

# call DB insert script
$NODE_EXECUTABLE "${PROJECT_PATH}/scripts/database_scritps/Insert_Product_to_DB.js"
