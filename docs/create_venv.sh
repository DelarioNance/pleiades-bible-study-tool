#!/bin/bash
#
# ------------------------------------------------------------
# Usage Instructions
# ------------------------------------------------------------
# To make this script executable:
#     chmod +x <filename>.sh
#
# To run the script:
#     ./<filename>.sh
#
# To activate the virtual environment:
#     source venv/bin/activate
#
# Notes:
# - Ensure you are in the same directory as the script when running it.
# - If you rename the file, update the commands above accordingly.
#
# ------------------------------------------------------------

# Creates the Python virtual environment.
echo "🔧 Creating virtual environment..."
python -m venv venv
echo "🎉 Done!"