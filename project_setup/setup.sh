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

pip install --quiet -r "${script_dir}/requirements.txt"
if [ $? -eq 0 ]; then
	echo -e "requirements [${ansi_green}OK${ansi_nc}] !"
else
	echo -e "requirements [${ansi_red}Failed${ansi_nc}] !"
	return 1
fi

python "${script_dir}/../manage.py" collectstatic --noinput
if [ $? -eq 0 ]; then
	echo -e "collectstatic [${ansi_green}OK${ansi_nc}] !"
else
	echo -e "collectstatic [${ansi_red}failed${ansi_nc}] !"
	return 1
fi

python "${script_dir}/../manage.py" runserver
