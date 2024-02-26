#!/bin/bash

ansi_nc="\e[0m"
ansi_green="\e[6;32m"
ansi_red="\e[6;31m"

prev_dir="$(pwd)"

cd "$(dirname "$0")" || exit
script_dir="$(pwd)"

cd "${prev_dir}" || exit

export PROJECT_ROOT="$(dirname "${script_dir}")"

# Vérification de l'existence du fichier d'activation de l'environnement virtuel
if [ -f "${script_dir}/venv/bin/activate" ]; then
    source "${script_dir}/venv/bin/activate"
    echo -e "Python environment [${ansi_green}activated${ansi_nc}]!"
else
    echo -e "[${ansi_red}Error${ansi_nc}]: Virtual environment activation script not found!"
    exit 1
fi

# Vérification de l'existence du script de configuration des variables d'environnement
if [ -f "${script_dir}/.env_setup.sh" ]; then
    source "${script_dir}/.env_setup.sh" 1
    echo -e "Project environment variables [${ansi_green}exported${ansi_nc}]!"
else
    echo -e "[${ansi_red}Error${ansi_nc}]: Environment setup script not found!"
    exit 1
fi

run_command() {
    local command="$1"
    local command_msg="$2"

    eval "${command} 1>/dev/null"
    local exit_code=$?

    printf "%-30s " "${command_msg} :"

    if [ ${exit_code} -ne 0 ]; then
        echo -e "[${ansi_red}Failed${ansi_nc}] !"
        return ${exit_code}
    else
        echo -e "[${ansi_green}OK${ansi_nc}] !"
    fi
}

run_command "bash ${script_dir}/compile_css.sh" "CSS compilation"
run_command "pip install --quiet -r ${script_dir}/requirements.txt" "Pip requirements"
run_command "python3 ${script_dir}/../manage.py collectstatic --noinput" "Static files collection"

python3 "${script_dir}/../manage.py" runserver
