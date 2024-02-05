#!/bin/bash

ansi_nc="\e[0m"
ansi_green="\e[6;32m"
ansi_red="\e[6;31m"

prev_dir="$(pwd)"

cd "$(dirname $0)"
script_dir="$(pwd)"

cd "${prev_dir}"

export PROJECT_ROOT="$(dirname ${script_dir})"

source "${script_dir}/venv/bin/activate"
echo -e "environement python [${ansi_green}activate${ansi_nc}] !"

source "${script_dir}/.env_setup.sh" 1
echo -e "your project's environement variables are [${ansi_green}exported${ansi_nc}] !"

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

run_command"bash ${script_dir}/compile_css.sh" "CSS compilation"

run_command"pip install --quiet -r ${script_dir}/requirements.txt" "Pip requirements"

run_command"python ${script_dir}/../manage.py collectstatic --noinput" "Static files collection"

python "${script_dir}/../manage.py" runserver
