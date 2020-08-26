# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  
  config.vm.provider "virtualbox" do |v|
    v.memory = 4096
    v.cpus = 2
  end
  
  config.vm.provision "shell", privileged: false, inline: <<-SHELL
	 sudo apt-get update
	 
	 # Install pyenv prerequisites
	 sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
	 
	 # Install pyenv
	 rm -r ~/.pyenv
	 git clone https://github.com/pyenv/pyenv.git ~/.pyenv
	 echo 'echo "Path:" $PATH' >> ~/.profile
	 echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
     echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
	 echo 'eval "$(pyenv init -)"' >> ~/.profile
	 
	 # Install Python 3.8.5
	 echo 'python --version' >> ~/.profile
	 echo 'pyenv install 3.8.5' >> ~/.profile
	 echo 'pyenv global 3.8.5' >> ~/.profile
	 echo 'python --version' >> ~/.profile
     source ~/.profile
	 
	 echo 'Updated path:' $PATH
	 python --version
	 
	 # Install poetry
	 curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  SHELL
end
