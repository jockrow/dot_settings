eval "$(/opt/homebrew/bin/brew shellenv)"

if command -v tmux>/dev/null; then
	exec fish
fi
