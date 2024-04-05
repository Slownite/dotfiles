#!/usr/bin/env python3
import os
import shutil
import subprocess


def get_paths():
    home = os.getenv("HOME")
    dotfiles = os.getcwd()
    if home is None:
        home = input("Enter your home directory path: ")
        while not os.path.exists(home):
            home = input("Enter your home directory path: ")
    return home, dotfiles


def goto(path):
    if os.path.exists(path):
        os.chdir(path)
    raise FileNotFoundError(f"directory {path} not found")


def removefile(file_path):
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


def oh_my_zsh():
    command = 'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"'
    runcommand(command)


def doom_emacs():
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
    goto(home)
    if os.path.exists(f".config/emacs"):
        print(
            "skipped the installation doom emacs because it seem to be already install"
        )
        return
    doom_emacs()
    removedirectory(f"{home}/.doom.d")


def stow(dotfiles):
    runcommand("stow .", cwd=dotfiles)


def generate_ssh_key():
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

    # Generate the SSH key pair using Ed25519
    email = input("email: ")
    command = ["ssh-keygen", "-t", "ed25519", "-C", email]
    runcommand(command)


def main():
    home, dotfiles = get_paths()
    zsh_config(home)
    emacs_config(home)


if __name__ == "__main__":
    main()
