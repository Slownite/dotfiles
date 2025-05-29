# ~/.config/nushell/env.nu

# Path configuration (this fixes your current error)
$env.PATH = ($env.PATH | append [
    "/usr/local/bin"
    "/home/linuxbrew/.linuxbrew/bin"
    "~/.cargo/bin"
])

# Aliases
alias ll = ls -l
alias la = ls -a
alias .. = cd ..
alias k = kubectl
alias z = zellij -l welcome options --default-shell nu
$env.CARAPACE_BRIDGES = 'zsh,fish,bash,inshellisense'
fastfetch

