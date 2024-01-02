# Transcendence Project

## Introduction

- Welcome to the Transcendence Project! This project is designed to streamline the development workflow using Docker and direnv, ensuring a seamless and efficient environment setup for developers. Here, we focus on creating a robust structure that simplifies processes like service management, data storage, and environment configuration. Whether you're working on a complex backend system, an interactive frontend, or diving into data analysis with ELK stack, Transcendence Project has got you covered. Join us in this journey to elevate your development experience to new heights!

## Prerequisites

- `direnv` must be installed on your system. For installation instructions, refer to the [official `direnv` documentation](https://direnv.net/docs/installation.html).
- Command `sudo apt-get install direnv`

## Configuration
- Run this commande `chmod +x .init.sh`

### Initialize `direnv`:

- Add `eval "$(direnv hook bash)"` to your `~/.bashrc` or `~/.zshrc` file, depending on your shell.
- Command `echo 'eval "$(direnv hook bash)"' >> ~/.bashrc`

### Configure the Project:

- A `.envrc` file is located at the root of the project. This file contains environment variables and scripts needed to set up the project environment.

### Authorize `direnv`:

- Run `direnv allow .` in the project directory to authorize the execution of the `.envrc` file.

## Usage

- Upon entering the project directory, `direnv` will automatically load the configurations set in `.envrc`.
- Project management commands (such as starting Docker services) can be executed via the provided `Makefile`.

## Directory Structure

TRANSC/
│
├── srcs/ # Source code and Docker configurations
│ ├── docker-compose.yaml
│ └── .env # Environment variables for Docker
│
├── .envrc # direnv configuration script
├── Makefile # Make commands for project management
├── init.sh # Initialization script for setting permissions
└── Readme.md # This file


## Makefile

The `Makefile` is set up to manage various aspects of the project, such as starting services (`frontend`, `backend`, `elk`), building Docker images (`build`), creating volumes, stopping, and cleaning up services.

## Important Notes

- The `.envrc` file should not be shared publicly if it contains sensitive information.
- Ensure all team members have `direnv` configured on their systems for a consistent development experience.
