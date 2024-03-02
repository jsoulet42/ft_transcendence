#!/bin/bash
# Shell script to compile a css file from a scss file using sass.

# If sass is not installed :
#  sudo apt install npm
#  sudo npm install -g sass

# ********************************************************************************************** #

# Files variables
static_dir="$PROJECT_ROOT/transcendence/static/transcendence"
scss_file_path="${static_dir}/scss/main.scss"
output_css_file_path="${static_dir}/css/style.css"

# Color output variables
ansi_nc="\e[0m"
ansi_blue="\e[34m"
ansi_yellow="\e[33m"

# ********************************************************************************************** #

# Function to echo the files found inside the directories stored in the ':' separated path
# variable given as first argument with a ':' character and a string given as second parameter
# appended after each file name.
build_path_dependencies()
{
    local path="$1"
    local output_file_path="$2"
    local path_array=()

    # Split the path variable into an array
    IFS=':' read -ra path_array <<< "${path}"

    # Append the output file to each file inside each directory in the path and echo the result
    for path in "${path_array[@]}"; do
        find ${path} -name '*.scss' | sed "s|$|:${output_file_path}|g"
    done
}

# ********************************************************************************************** #

# If the first script argument is equal to 1, compile the output css file with the --watch option.
# This will update the output css file at each modification of one of the files found inside the
# directories from the SASS_PATH environment variable.
if [ $# -gt 0 ] && [ "$1" == "1" ]; then
    dependencies="`build_path_dependencies ${SASS_PATH} ${output_css_file_path}`"
    echo "Files watched over :"
    echo -e "${ansi_yellow}${dependencies}${ansi_nc}" | sed "s/:/ ---> /g"

    sass --watch "${scss_file_path}:${output_css_file_path}" ${dependencies}

    exit $?
fi

# If no argument is given or the first one isn't equal to 1, compile the output css file only
# once.
# The script will need to be run again if one of the imported scss files inside the scss file at
# '${scss_file_path}' is modified.
sass "${scss_file_path}" "${output_css_file_path}"

exit_code=$?
if [ ${exit_code} -ne 0 ]; then
    exit ${exit_code}
fi

echo -en "Compiled ${ansi_yellow}${output_css_file_path}${ansi_nc} "
echo -e "from ${ansi_yellow}${scss_file_path}${ansi_nc}."
