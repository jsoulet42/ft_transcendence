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

bash "${script_dir}/compile_css.sh" 1>/dev/null
echo -e "[${ansi_green}compiled${ansi_nc}] your scss files!"

run_command() {
	local command="$@"

	$@ 1>/dev/null

	if [ $? -ne 0 ]; then
		echo -e "[${ansi_red}Failed${ansi_nc}] !"
		return 1
	else
		echo -e "[${ansi_green}OK${ansi_nc}] !"
	fi

}


run_command pip install --quiet -r ${script_dir}/requirements.txt
run_command python ${script_dir}/../manage.py collectstatic --noinput


python "${script_dir}/../manage.py" runserver
