# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.network "private_network", ip: "192.168.100.100"
  config.vm.network :forwarded_port, guest: 8000, host: 8000

  config.vm.provision :shell, :inline => "apt-get update"
  config.vm.provision :shell, :inline => "apt-get install -y curl"
  config.vm.provision :shell, :inline => "curl -sL https://deb.nodesource.com/setup | bash"

  config.vm.provision :shell, :inline => "apt-get install -y postgresql postgresql-contrib python-dev python-pip libpq-dev git-core build-essential nodejs"
  #config.vm.provision :shell, :inline => "curl https://www.npmjs.com/install.sh | sudo sh"
  config.vm.provision :shell, :inline => "npm install ngrok -g"

  # Generate config files and initialize DB
  config.vm.provision :shell do |shell|
    shell.inline = <<-EOS
      set -e
      sudo -u postgres psql -c "DROP DATABASE IF EXISTS kikar"
      sudo -u postgres psql -c "DROP ROLE IF EXISTS kikar"
      sudo -u postgres psql -c "CREATE USER kikar WITH PASSWORD 'kikar'"
      sudo -u postgres psql -c "CREATE DATABASE kikar TEMPLATE=template0 ENCODING='UTF8' LC_CTYPE='en_US.utf8' LC_COLLATE='en_US.UTF-8'"
    EOS
  end

  # pip requirements
  config.vm.provision :shell do |shell|
    shell.inline = <<-EOS
      set -e
      # Do 2 pip tries as sometimes repositories fail to respond
      PIP="sudo pip install -r /vagrant/requirements/vps.txt"
      $PIP || $PIP
    EOS
  end

  # Django setup
  config.vm.provision :shell do |shell|
    shell.inline = <<-EOS
      set -e
      cd /vagrant/kikar_hamedina/
      [ ! -d logs ] && mkdir logs
      python manage.py syncdb --noinput
      [ -f ../devOps/user_backup.json ] && python manage.py loaddata ../devOps/user_backup.json
      python manage.py dumpdata --indent=4 auth > ../devOps/user_backup.json
      for m in core mks links facebook_feeds  persons polyorg video zinnia taggit updater reporting tastypie; do
        python manage.py migrate $m
      done
      python manage.py migrate kikartags 0004
      for f in sites data_fixture_planet data_fixture_mks data_fixture_mks_altnames data_fixture_facebook_feeds data_fixture_feed_popularity data_fixture_persons data_fixture_polyorg data_fixture_status_comment_pattern ; do
        python manage.py loaddata $f
       done
      for f in 1001_1001 1001_1002 1001_1003 1001_1004 1001_1005 1001_1006; do
        python manage.py loaddata $f
      done
      #for f in 1002_1007 1002_1008 1002_1009 1002_1010 1002_1011; do
      #  python manage.py loaddata -i $f
      #done
      python manage.py migrate kikartags
      python manage.py convert_tags_data_to_kikartags
      python manage.py loaddata data_fixture_kikartags
      python manage.py fetchfeedproperties || true
      python manage.py update_facebook_personas
      python manage.py update_is_current_feed
      # python manage.py classify_and_test_autotag 1
    EOS
  end

  config.vm.provision :shell do |shell|
    shell.inline = <<-EOS
      set -e
      echo 'exec python /vagrant/kikar_hamedina/manage.py runserver 0.0.0.0:8000' > /etc/init/kikar.conf
      STATUS="$(sudo status kikar)"
      if [[ $STATUS == *"start"* ]]; 
      then
        restart kikar
      else 
        start kikar 
      fi
      
    EOS
  end

  config.vm.provision :shell do |shell|
    shell.inline = <<-EOS
      cd /vagrant/kikar_hamedina/
      # echo 'exec python /vagrant/kikar_hamedina/manage.py runserver 0.0.0.0:8000' > /etc/init/kikar.conf
      python manage.py fetchfeedstatuses -a -f
    EOS
  end
end
