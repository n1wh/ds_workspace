# From here -> https://medium.com/@ferhatsukrurende/terminator-zsh-ohmyzsh-58ba4303bd09

# install terminator and set it as default
sudo apt-get install terminator
sudo update-alternatives --config x-terminal-emu

# install zsh shell and set it as default
sudo apt-get install zsh
chsh -s $(which zsh)

# download fonts for oh-my-zsh
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf
# and INSTALL THEM by hands
# select this fonts in Preferences -> Profiles in Terminator

# install oh-my-zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

