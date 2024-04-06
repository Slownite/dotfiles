#!/usr/bin/env python3
import os
import shutil
import subprocess
import argparse


def get_paths():
    """Get the home path and dotfile path"""
    home = os.getenv("HOME")
    dotfiles = os.getcwd()
    if home is None:
        home = input("Enter your home directory path: ")
        while not os.path.exists(home):
            home = input("Enter your home directory path: ")
    return home, dotfiles


def goto(path):
    """cd to a directory"""
    if os.path.exists(path):
        os.chdir(path)
    else:
        raise FileNotFoundError(f"directory {path} not found")


def removefile(file_path):
    """remove file"""
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"The file {file_path} has been deleted.")
    else:
        print(f"The file {file_path} does not exist.")


def removedirectory(path):
    """Remove the specified directory and all its contents.

    Args:
    path (str): The path to the directory to be removed.
    """
    # Check if the directory exists
    if os.path.exists(path) and os.path.isdir(path):
        try:
            # Remove the directory and all its contents
            shutil.rmtree(path)
            print(f"The directory {path} has been successfully removed.")
        except Exception as e:
            # Handle any errors that occur
            print(
                f"An error occurred while attempting to remove the directory {path}: {e}"
            )
    else:
        print(f"The directory {path} does not exist or is not a directory.")


def runcommand(command, cwd=None):
    """Executes a shell command in an optional working directory."""
    try:
        subprocess.run(command, shell=True, check=True, cwd=cwd)
        print(f"Command executed successfully: {command}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the command: {e}")


def askpermission(step_name):
    """ask the permission to execute a task"""
    return input(f"Do you want to execute {step_name}? (y/n) ").lower().startswith("y")


def oh_my_zsh():
    """install oh-my-zsh"""
    command = 'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"'
    runcommand(command)


def doom_emacs():
    """install dom emacs"""
    # Define the commands
    git_clone_command = (
        "git clone --depth 1 https://github.com/doomemacs/doomemacs ~/.config/emacs"
    )
    runcommand(git_clone_command)

    # Install Doom Emacs
    doom_script_path = os.path.expanduser("~/.config/emacs/bin/doom")
    doom_install_command = f"{doom_script_path} install"
    if os.path.exists(doom_script_path):
        runcommand(doom_install_command)
    else:
        print("Doom install script does not exist. Please check the clone operation.")
        return  # Exit the function if install script doesn't exist

    # Execute doom sync
    doom_sync_command = f"{doom_script_path} sync"
    runcommand(doom_sync_command, cwd=os.path.dirname(doom_script_path))

    # Execute doom upgrade
    doom_upgrade_command = f"{doom_script_path} upgrade"
    runcommand(doom_upgrade_command, cwd=os.path.dirname(doom_script_path))


def zsh_config(home):
    """Setup zsh and oh my zsh"""
    goto(home)
    if os.path.exists(".oh-my-zsh"):
        print(
            "skipped the installation oh my zsh because it seem to be already install"
        )
        return
    print(f"delete all previous .zshrc config from {home}")
    removefile(f"{home}/.zshrc")
    oh_my_zsh()
    removefile(f"{home}/.zshrc")


def emacs_config(home):
    """setup doom emacs"""
    goto(home)
    if os.path.exists(f".config/emacs"):
        print(
            "skipped the installation doom emacs because it seem to be already install"
        )
        return
    doom_emacs()
    removedirectory(f"{home}/.doom.d")


def stow(dotfiles):
    """stow my dotfiles"""
    goto(dotfiles)
    runcommand("stow .", cwd=dotfiles)


def generate_ssh_key(email_address):
    """
    Generates an SSH key pair using the Ed25519 algorithm and saves it to the .ssh directory.

    Args:
    key_name (str): The name of the SSH key file. Default is 'id_ed25519'.
    """
    # Define the path to the .ssh directory
    ssh_dir = os.path.expanduser("~/.ssh")

    # Create the .ssh directory if it doesn't exist
    if not os.path.exists(ssh_dir):
        os.makedirs(ssh_dir)
        print(f"Created directory: {ssh_dir}")
    print(email_address)
    if email_address is None:
        email = input("email: ")
    else:
        email = email_address
    # Generate the SSH key pair using Ed25519
    command = f'ssh-keygen -t ed25519 -f -N -C "{email}"'
    runcommand(command)


def parse_arguments():
    """parse the command arguments"""
    parser = argparse.ArgumentParser(description="setup script for Slownite dotfiles.")
    parser.add_argument(
        "--all", help="Execute all step without asking", action="store_true"
    )
    parser.add_argument(
        "-e",
        "--email",
        help="Fill the Email address in ssh-key",
        type=str,
        default=None,
    )
    args = parser.parse_args()
    return args


def main():
    home, dotfiles = get_paths()
    args = parse_arguments()
    print(args.email)
    print("Start installation of dotfiles")
    if args.all:
        zsh_config(home)
        emacs_config(home)
        stow(dotfiles)
        generate_ssh_key(args.email)
    else:
        if askpermission("zsh setup"):
            zsh_config(home)
        if askpermission("emacs setup"):
            emacs_config(home)
        if askpermission("the stow step"):
            stow(dotfiles)
        if askpermission("ssh key setup"):
            generate_ssh_key(args.email)
    print("installation finished!")


if __name__ == "__main__":
    main()
