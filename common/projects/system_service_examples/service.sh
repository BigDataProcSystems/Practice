#!/usr/bin/env bash

main() {

    while true; do
        case "$1" in
            "-d"|"--deploy")
                deploy
                break
            ;;
            "-q"|"--stop")
                stop
                break
            ;;
            "-r"|"--start")
                start
                break
            ;;
            "-R"|"--restart")
                restart
                break
            ;;
            "-l"|"--logs")
                show_logs
                break
            ;;
            "-s"|"--status")
                show_status
                break
            ;;
            "-c"|"--client")
                run_client
                break
            ;;
            *)
                echo "Argument is not found." >&2
                exit 1
            ;;
        esac
    done
}

function deploy()
{
    # Copy service from a develop dir to the systemd directory
    cp .service /etc/systemd/system/sysprog.service

    #  Reload systemd manager configuration
    systemctl daemon-reload

    # Start the sysprog service
    systemctl start sysprog
}

function start()
{
    systemctl start sysprog
}

function stop()
{
    systemctl stop sysprog
}

function restart()
{
    systemctl restart sysprog
}

function show_status()
{
    systemctl status sysprog
}

function show_logs()
{
    journalctl -u sysprog -f
}

function run_client()
{
    /home/ubuntu/ML/anaconda3/bin/python sysprog_client.py
}


main "$@"