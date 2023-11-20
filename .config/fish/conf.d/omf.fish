# Path to Oh My Fish install.
set -q XDG_DATA_HOME
and set -gx OMF_PATH "$XDG_DATA_HOME/omf"
or set -gx OMF_PATH "$HOME/.local/share/omf"
and set -gx OMF_PATH ~/.config/omf/

set -gx TREE_COLORS "fi=00:di=01;34:ln=01;36:pi=40;33:so=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42"

# List command history
set -gx FZF_CTRL_R_OPTS "
	--prompt='󰚩 '
	--height 80%"

# List file content using bat (https://github.com/sharkdp/bat)
set -gx FZF_CTRL_T_OPTS "
  --preview 'bat -n --color=always {}'
	--prompt='󰚩 '
	--height 80%"

# TODO:ignorar binarios, probar con /Users/richard/devs/java/api_rest/build, y al verificar que funciona poner que ignore las carpetas build y obj
set -gx FZF_CTRL_T_COMMAND "find . -type f | grep -Ev '\.git|node_modules'"

# List directories
set -gx FZF_ALT_C_OPTS "--preview 'tree -C {}'
	--prompt='󰚩 '
	--height 80%"

# Alias and showing the command to edit
# git compare tool
abbr -a -g gct git difftool --dir-diff

# tree immproved showing with icons
abbr -a -g tre eza -T --icons

# list
abbr -a -g ll eza --long --created --modified --header --git --icons

# list all
abbr -a -g la eza --all --long --created --modified --header --git --icons

# grep 
abbr -g -g grep grep --exclude-dir={node_modules,.git} -RinH 

# Load Oh My Fish configuration.
source $OMF_PATH/init.fish
