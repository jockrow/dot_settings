# Path to Oh My Fish install.
set -q XDG_DATA_HOME
and set -gx OMF_PATH "$XDG_DATA_HOME/omf"
or set -gx OMF_PATH "$HOME/.local/share/omf"
and set -gx OMF_PATH ~/.config/omf/

# Preview file content using bat (https://github.com/sharkdp/bat)
set -gx FZF_CTRL_T_OPTS "
  --preview 'bat -n --color=always {}'
	--prompt='󰚩 '
	--height 80%"

# TODO:ignorar binarios, probar con /Users/richard/devs/java/api_rest/build, y al verificar que funciona poner que ignore las carpetas build y obj
# TODO:ignorar node_modules con tree y tre

set -gx FZF_CTRL_T_COMMAND "find . -type f | grep -Ev '\.git|node_modules'"
set -gx FZF_ALT_C_OPTS "--preview 'tree -C {}'
	--prompt='󰚩 '
	--height 80%"

alias tre='eza -T --git --icons'
alias ll='eza --long --header --git --icons'
alias la='eza --all --long --header --git --icons'
alias tree='tree -I \'node_modules | cache |test_*\''

# Load Oh My Fish configuration.
source $OMF_PATH/init.fish
