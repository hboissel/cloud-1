# cloud-1

## Setup ssh-key

```
# create ssh key
mkdir .ssh; ssh-keygen -f .ssh/id_ed25519 -t ed25519 -N ""; cat .ssh/id_ed25519.pub
```

## cert creation

```
certbot certonly --standalone -m 'hugo.boissel03@gmail.com' -d 'cloud1.hboissel.fr'

certbot --nginx -m 'hugo.boissel03@gmail.com' -d 'cloud1.hboissel.fr'
```

https://letsdebug.net/

## Ansible

```
ansible-inventory --list -y # to check inventory

ansible all -m ping -u root # to check if we can connect the servers

ansible-playbook -i inventory playbook.yml # run a playbook

ansible all -i inventory -a "uptime" # run bash command
```

## Digital Ocean API
```
# List ssh keys
curl -X GET \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DIGITALOCEAN_TOKEN" \
  "https://api.digitalocean.com/v2/account/keys"

# create ssh key

curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DIGITALOCEAN_TOKEN" \
  -d '{"name":"cloud-1","public_key":"ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJBwYWtHi/aDTj1z/b6K7KIXCyiUkAf4N6PzFyIHDsnd hboissel@laptop"}' \
  "https://api.digitalocean.com/v2/account/keys" 

# Delete ssh key

curl -X DELETE \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DIGITALOCEAN_TOKEN" \
  "https://api.digitalocean.com/v2/account/keys/$SSH_KEY_ID" 

# create one droplet

curl -X POST -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer '$DIGITALOCEAN_TOKEN'' \
    -d '{"name":"cloud-1",
        "size":"s-1vcpu-512mb-10gb",
        "region":"fra1",
        "image":"ubuntu-24-04-x64",
        "tags":["cloud-1"],
        "ssh_keys":["'$DIGITALOCEAN_SSH_FINGERPRINT'"]}' \
    "https://api.digitalocean.com/v2/droplets"

# create multiple droplet

curl -X POST -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer '$DIGITALOCEAN_TOKEN'' \
    -d '{"names":["cloud-1-1", "cloud-1-2"],
        "size":"s-1vcpu-512mb-10gb",
        "region":"fra1",
        "image":"ubuntu-24-04-x64",
        "tags":["cloud-1"],
        "ssh_keys":["'$DIGITALOCEAN_SSH_FINGERPRINT'"]}' \
    "https://api.digitalocean.com/v2/droplets"


# List droplets

curl -X GET \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DIGITALOCEAN_TOKEN" \
  "https://api.digitalocean.com/v2/droplets?tag_name=cloud-1"

#delete
curl -X DELETE \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DIGITALOCEAN_TOKEN" \
  "https://api.digitalocean.com/v2/droplets?tag_name=cloud-1"
```