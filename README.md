## Installation
```bash
curl https://raw.githubusercontent.com/oh-my-fish/oh-my-fish/master/bin/install | fish

#For git abbreviations
omf install https://github.com/jhillyerd/plugin-git
omf install bobthefish
omf install z

brew install tree
brew install ranger
brew install tmux
brew install eza
brew install fzf
```

## Create symbolic links
```bash
ln -s -f ~/dot_settings/.tmux.conf ~/.tmux.conf
ln -s -f ~/dot_settings/.ideavimrc ~/.ideavimrc
ln -s -f ~/dot_settings/.vimrc ~/.vimrc

mv ~/.config/fish ~/.config/fishBk
ln -s -f ~/dot_settings/.config/fish ~/.config/fish

mv ~/.config/ranger ~/.config/rangerBk
ln -s -f ~/dot_settings/.config/ranger ~/.config/ranger

rm -fr ~/.config/fishBk
rm -fr ~/.config/rangerBk
```

## For more documentation about commands like vim in fish
https://fishshell.com/docs/current/interactive.html#vi-mode-commands
