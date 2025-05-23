# ~/.config/nushell/config.nu

# Starship prompt
$env.PROMPT_COMMAND = {|| starship prompt }
$env.PROMPT_INDICATOR = ""
$env.PROMPT_MULTILINE_INDICATOR = "::: "

# Updated config format
$env.config = {
  edit_mode: vi
  cursor_shape: {}
  show_banner: false

  hooks: {
    pre_prompt: []
    pre_execution: []
    env_change: {}
  }
}

