#!/bin/bash

###############################################################################
# Wrapper Script for code-explain.py
###############################################################################
#
# This script provides a convenient wrapper around code-explain.py that:
# - Handles virtual environment activation/deactivation automatically
# - Allows the script to be called from any directory via terminal
#
# Setup Instructions:
# ------------------
# 1. Create virtual environment:
#    python3 -m venv venv
#
# 2. Install dependencies:
#    pip3 install -r requirements.txt
#
# 3. Make executable:
#    chmod +x code-explain-wrapper.sh
#
# 4. Optional: Create system-wide command alias
#    sudo ln -s "$(pwd)/code-explain-wrapper.sh" /usr/local/bin/ce
#    This allows using the 'ce' command from any directory
###############################################################################

# Get the real path of the script, following symlinks
SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

# Activate the virtual environment
source "${SCRIPT_DIR}/venv/bin/activate"

# Run the Python script with all passed arguments
python "${SCRIPT_DIR}/code-explain.py" "$@"

# Deactivate the virtual environment
deactivate