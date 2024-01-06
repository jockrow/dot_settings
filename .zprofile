eval "$(/opt/homebrew/bin/brew shellenv)"

if command -v fish>/dev/null; then
	exec fish
fi
