#!/data/data/com.termux/files/usr/bin/bash

echo "Starting Termux Arch Linux Integration Setup..."

# Step 1: Update Termux and install essential packages
echo "Updating Termux and installing essential packages..."
pkg update -y && pkg upgrade -y
pkg install -y proot wget curl git clang zsh tar

# Step 2: Install Pacman
echo "Installing Pacman..."
wget https://github.com/termux/termux-packages/releases/download/bootstrap/bootstrap-2024.12.10.zip
unzip bootstrap-2024.12.10.zip -d $HOME/bootstrap
cd $HOME/bootstrap
bash setup-bootstrap.sh
export PATH=$HOME/bootstrap/usr/bin:$PATH

# Step 3: Configure Pacman
echo "Configuring Pacman..."
mkdir -p ~/.termux/boot/
wget -O /data/data/com.termux/files/usr/etc/pacman.conf https://raw.githubusercontent.com/TermuxArch/TermuxArch/main/pacman.conf
pacman-key --init
pacman-key --populate archlinuxarm

# Step 4: Install Base System and `base-devel`
echo "Installing Arch Linux base system and base-devel..."
pacman -Syu --noconfirm
pacman -S --noconfirm base base-devel

# Step 5: Handle Filesystem Conflicts
echo "Resolving filesystem conflicts..."
find /data/data/com.termux/files/usr/ -name '*.conflict' -exec rm {} \;

# Step 6: Set up Zsh as default shell
echo "Setting up Zsh..."
chsh -s $(which zsh)
cat << 'EOF' > ~/.zshrc
# Basic Zsh config
export PATH="/data/data/com.termux/files/usr/bin:$PATH"
autoload -U compinit && compinit
EOF

# Step 7: Install Pamac (Optional GUI for Pacman)
echo "Installing Pamac..."
pacman -S --noconfirm pamac-aur libpamac
echo "alias pamac='pamac --no-confirm'" >> ~/.zshrc

# Step 8: Cleanup
echo "Cleaning up..."
rm -rf $HOME/bootstrap bootstrap-2024.12.10.zip
pacman -Sc --noconfirm

echo "Setup Complete! Please restart Termux or run 'zsh' to start your new shell."