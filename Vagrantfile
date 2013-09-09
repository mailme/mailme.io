Vagrant::Config.run do |config|
    config.vm.box = "mailme"
    config.vm.box_url = "http://files.vagrantup.com/precise64.box"
    config.vm.host_name = 'mailme'

    config.vm.share_folder "vagrant-root", "/vagrant", "./deploy"
    config.vm.provision :shell, :path => "vagrant/vagrant.sh"
end
