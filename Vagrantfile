# -*- mode: ruby -*-
# vi: set ft=ruby :

#https://github.com/dgmorales/cm-sandbox/blob/0a6f19b7931877bf08a480fc79237e96d4cc9ea6/ansible/roles/neel.rundeck/tests/vagrant-centos70/Vagrantfile

Vagrant.configure("2") do |config|
 config.vm.box_check_update = "false"
 config.vm.provider "virtualbox" do |vb|
   vb.memory = "2048"
   vb.cpus = 1
   vb.gui = false
   vb.linked_clone = true
   vb.customize ["modifyvm", :id, "--cpuexecutioncap", "50"]
 end

 config.vm.define "webserver" do |web|
   web.vm.hostname = "odesiflask"
   web.vm.box = "bento/ubuntu-20.04"
   web.vm.network :private_network, ip: "192.168.10.10"
   web.vm.network "forwarded_port", guest: "80", host: "8080"
   #Provision the webserver with Ansible
   web.vm.provision "ansible" do |ansible|
     ansible.inventory_path = "./inventory"
     ansible.playbook="./ubuntu-playbook.yml"
   end
  end
end
