# microtype
##Flask Blog Mongodb
    pip install virtualenv 
    virtualenv .env --no-site-packages

#linux
    source .env/bin/activate
    pip install -r requirements.txt

#windows
    cd .env/scripts/
    activate
    pip install -r requirements.txt

#安装mongodb 并配置
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
    echo "deb http://repo.mongodb.org/apt/debian "$(lsb_release -sc)"/mongodb-org/3.0 main" | sudo tee      /etc/apt/sources.list.d/mongodb-org-3.0.list
    sudo apt-get update
    sudo apt-get install -y mongodb-org

service mongod start

##更改config.py
    MONGODB_SETTINGS = {
        'db': 'blog',
        'host': '192.168.16.1',
        'port': 27017,
        'username': 'nightraid',
        'password': 'xxxx'
    }

#初始化账号
    python manager.py shell

    from hashlib import md5
    user = models.User(email="xxx@xx.com",password=md5("xxxx").hexdigest,about_me="xxxx'",nickname="xxxx")
    user.save()

#启动debug服务器
    python manager.py runserver --port 8000
