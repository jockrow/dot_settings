<!-- TODO: quitar .DS_Store -->

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

mv ~/.config/omf ~/.config/omfBk
ln -s -f ~/dot_settings/.config/omf ~/.config/omf

mv ~/.config/ranger ~/.config/rangerBk
ln -s -f ~/dot_settings/.config/ranger ~/.config/ranger

rm -fr ~/.config/fishBk
rm -fr ~/.config/omfBk
rm -fr ~/.config/rangerBk
```
