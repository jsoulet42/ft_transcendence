#!/bin/bash
# Shell script to compile a css file from a scss file using sass.

# If sass is not installed :
#  sudo apt install npm
#  sudo npm install -g sass

# ********************************************************************************************** #

# Color output variables
ansi_nc="\e[0m"
ansi_blue="\e[34m"
ansi_yellow="\e[33m"

# Files variables
static_dir="transcendence/static"
scss_file_path="${static_dir}/scss/main.scss"
output_css_file_path="${static_dir}/transcendence/css/style.css"

# ********************************************************************************************** #

build_path_dependencies()
{
    local path="$1"
    local output_file_path="$2"

    # Split the path variable into an array
    IFS=':' read -ra path_array <<< "${path}"

    # Append the output file to each file  directory in the path and echo the result
    for path in "${path_array[@]}"; do
        find ${path} -name '*.scss' | sed "s|$|:${output_file_path}|g"
    done
}


# ********************************************************************************************** #

# If the first script argument is equal to 1, compile the output css file with the --watch option.
# This will update the output css file at each modification of one of the imported scss files
# inside the scss file at '${scss_file_path}'.
if [ $# -gt 0 ] && [ "$1" == "1" ]; then
    dependencies="`build_path_dependencies ${SASS_PATH} ${output_css_file_path}`"
    sass --watch "${scss_file_path}:${output_css_file_path}" ${dependencies}

    if [ $? -eq 0 ]; then
        echo -e "Compiled ${ansi_yellow}${output_css_file_path}${ansi_nc} with the --watch option."
        echo -e "Don't forget to run '${ansi_yellow}python manage.py collectstatic${ansi_nc}' now."
    fi
    exit $?
fi

# If no argument is given or the first one isn't equal to 1, compile the output css file only
# once.
# The script will need to be run again if one of the imported scss files inside the scss file at
# '${scss_file_path}' is modified.
sass "${scss_file_path}" "${output_css_file_path}"
if [ $? -eq 0 ]; then
    echo -e "Compiled ${ansi_yellow}${output_css_file_path}${ansi_nc}."
    echo -e "Don't forget to run '${ansi_yellow}python manage.py collectstatic${ansi_nc}' now."
fi
