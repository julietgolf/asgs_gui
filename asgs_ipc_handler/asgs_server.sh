#!/bin/bash

ASGS_HOME="/p/work/jogra/real_work/asgs2"

# This causes an exit on any error
# This is done to keep any process from starting if something goes wrong during setup
set -e

echo ""

# Find asgsh
if [ -z "$ASGS_HOME" ];then
    echo "ASGS_HOME wasn't set in the asgs_server.sh"
    echo "Aborting"
    exit 1
elif [ ! -f "${ASGS_HOME}/asgsh" ];then
    echo "Couldn't find asgsh at ASGS_HOME=${ASGS_HOME}"
    echo "Aborting"
    exit 1
else
    asgsh_exe="${ASGS_HOME}/asgsh"
fi

# Build server meta path unique for each user
[ ! -z "$HOME" ] || HOME=$(realpath ~)
server_meta_dir="${HOME}/.asgsh"

# Check if the server has a pid file
pid_file="${server_meta_dir}/pid"
if [ ! -f "${pid_file}" ]; then
    echo "Starting asgs"
    echo "Server meta dir: ${server_meta_dir}"

    # Check if the meta dir exists
    # If it does then something went wrong
    if [ -d "${server_meta_dir}" ]; then
        echo "${server_meta_dir} already exists"
        echo "Confirm asgs is not running and remove the meta dir."
        echo "Aborting"
        exit 1
    fi

    # Build the meta dir and pipes 
    mkdir "${server_meta_dir}"
    pipein="${server_meta_dir}/pipein"
    pipeout="${server_meta_dir}/pipeout"
    mkfifo "${pipein}"
    mkfifo "${pipeout}"

    # Start the server
    script -qf -c "${asgsh_exe}" /dev/null < "${pipein}" > "${pipeout}" &
    server_pid=$!

    # This keeps pipein from ever closing
    # If it did, then the server would lose stdin and crash
    tail -f /dev/null > "${pipein}" &
    tail_pid=$!
    
    printf "${server_pid}\n${tail_pid}\n" > "${pid_file}" && chmod 600 "${server_meta_dir}/pid"
    echo "asgs is running with pids:"
    mapfile -t pids < "${pid_file}"
    echo "ASGSH Pid: ${pids[0]}"
    echo "Pipe Tender Pid: ${pids[1]}"


    # The || true keeps the script from crashing from set -e 
    wait $server_pid || true

    echo "Cleaning up asgs"
    # Check if tender is still running and kill it
    if [ -n "$tail_pid" ] && kill -0 "$tail_pid" 2>/dev/null; then
        echo "Killing pipe tender"
        kill $tail_pid
    fi

    # Clean up meta dir
    if [ -d "${server_meta_dir}" ];then
        echo "Removing ${server_meta_dir}"
        rm -r "${server_meta_dir}"
    fi
else
    echo "asgs is already running at ${pid_file} with pids:"
    mapfile -t pids < "${pid_file}"
    echo "ASGSH Pid: ${pids[0]}"
    echo "Pipe Tender Pid: ${pids[1]}"
fi
