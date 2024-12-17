
## Setup
### SSH into your Linode server
ssh root@172.233.140.43

Use ssh-copy-id (recommended)
ssh-copy-id root@172.233.140.43
cat ~/.ssh/id_rsa.pub | ssh root@172.233.140.43 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

Secure SSH config on server
# Disable password authentication
PasswordAuthentication no

# Disable root login
PermitRootLogin no

# Restart SSH service
sudo systemctl restart sshd

Connect to Linode
Using the config method
ssh linode

Standard method
ssh -i ~/.ssh/id_rsa youruser@your_linode_ip

### Update system packages
sudo apt-get update && sudo apt-get upgrade -y

### Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

### Install Docker Compose
sudo apt-get install docker-compose -y

### Create a user (optional but recommended)
sudo adduser youruser
sudo usermod -aG docker youruser

## Deploy
# On your local machine
git clone your_repository
cd your_project

# Copy files to Linode
scp -r . youruser@your_linode_ip:/path/to/project

# On Linode server
cd /path/to/project
docker-compose up --build -d

## Resources
- https://www.linode.com/docs/guides/connect-to-server-over-ssh-on-windows/