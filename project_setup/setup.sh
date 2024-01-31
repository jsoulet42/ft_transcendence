#!/bin/bash

prev_dir="$(pwd)"

cd "$(dirname $0)"
script_dir="$(pwd)"

cd "${prev_dir}"

export PROJECT_ROOT="$(dirname ${script_dir})"

ansi_nc="\e[0m"
ansi_red_fg="\e[31m"
ansi_green_fg="\e[32m"
ansi_yellow_fg="\e[33m"

script_name="${ansi_yellow_fg}> SETUP >${ansi_nc}"

ok_text="[${ansi_green_fg}\e[6mOK${ansi_nc}]"
error_text="[${ansi_red_fg}ERR${ansi_nc}]"

source "${script_dir}/venv/bin/activate"
echo "${script_name} Python virtual environment ${ok_text}"

pip install --quiet -r "${script_dir}/requirements.txt"
exit_code=$?
echo -n "${script_name} Pip requirements installation "
if [ ${exit_code} -eq 0 ]; then
    echo "${ok_text}"
else
    echo "${error_text}"
    return ${exit_code}
fi

source "${script_dir}/.env_setup.sh" 1
echo "${script_name} Environment variables ${ok_text}"

bash "${script_dir}/compile_css.sh" 1>/dev/null
exit_code=$?
echo -n "${script_name} CSS compilation "
if [ ${exit_code} -eq 0 ]; then
    echo "${ok_text}"
else
    echo "${error_text}"
    return ${exit_code}
fi

python "${script_dir}/../manage.py" collectstatic --noinput
exit_code=$?
echo -n "${script_name} Static collecting "
if [ ${exit_code} -eq 0 ]; then
    echo "${ok_text}"
else
    echo "${error_text}"
    return ${exit_code}
fi

python "${script_dir}/../manage.py" runserver

try_command()
{
    local command="$1"
    local command_msg="$2"
}