# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  
  # Increase instance size to improve performance of installing python version below
  config.vm.provider "virtualbox" do |v|
    v.memory = 8192
    v.cpus = 2
  end
  
  # Forward host port to app Flask port on VM
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  
  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    sudo apt-get update
    
    # Install pyenv prerequisites
    sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
    
    # Download pyenv
    rm -r ~/.pyenv
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
    echo 'eval "$(pyenv init -)"' >> ~/.profile
    source ~/.profile
    
    # Install Python 3.8.5
    pyenv install 3.8.5
    pyenv global 3.8.5

    # Download poetry
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  SHELL
  
  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script"
    trigger.run_remote = {privileged: false, inline: "
      # Install dependencies and launch
      cd /vagrant
      poetry install
      poetry run flask run --host=0.0.0.0
    "}
  end
end
