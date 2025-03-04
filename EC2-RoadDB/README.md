# This is the EC2 Instance for setting up the Database storing all the roads

Steps to get Post GIS installed 

```
sudo dnf groupinstall 'Development Tools'
dnf install readline readline-devel
dnf install openssl-devel libicu-devel
```


Then without root perms

```
wget https://ftp.postgresql.org/pub/source/v16.1/postgresql-16.1.tar.gz
tar xfz postgresql-16.1.tar.gz
cd postgresql-16.1
./configure  --with-ssl=openssl
make
```

