## Installation
```bash
omf install bobthefish
curl https://raw.githubusercontent.com/oh-my-fish/oh-my-fish/master/bin/install | fish

#For git abbreviations
omf install https://github.com/jhillyerd/plugin-git
omf install z

brew install tree
brew install ranger
brew install eza
brew install fzf
brew install kitty

# for preview images in ranger with kitty
pip install pillow ranger-fm
```

## Create symbolic links
```bash
ln -s -f ~/dot_settings/.ideavimrc ~/.ideavimrc
ln -s -f ~/dot_settings/.vimrc ~/.vimrc
ln -s -f ~/dot_settings/.zprofile ~/.zprofile

mv ~/.config/fish ~/.config/fishBk
ln -s -f ~/dot_settings/.config/fish ~/.config/fish

mv ~/.config/ranger ~/.config/rangerBk
ln -s -f ~/dot_settings/.config/ranger ~/.config/ranger

mv ~/.config/kitty ~/.config/kittyBk
ln -s -f ~/dot_settings/.config/kitty ~/.config/kitty

rm -fr ~/.config/fishBk
rm -fr ~/.config/rangerBk
rm -fr ~/.config/kittyBk
```

## For more documentation about commands like vim in fish
https://fishshell.com/docs/current/interactive.html#vi-mode-commands

## kitty config
https://sw.kovidgoyal.net/kitty/conf/

## ranger config
https://github.com/ranger/ranger/blob/master/ranger/config/rc.conf
