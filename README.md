# Cloud-1

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Set Up Environment Variables](#2-set-up-environment-variables)
  - [3. Generate SSH Keys](#3-generate-ssh-keys)
  - [4. Build the Ansible Docker Container](#4-build-the-ansible-docker-container)
- [Usage](#usage)
  - [1. Access the Ansible Container](#1-access-the-ansible-container)
  - [2. Create Droplets on DigitalOcean](#2-create-droplets-on-digitalocean)
  - [3. Deploy the Infrastructure with Ansible](#3-deploy-the-infrastructure-with-ansible)
  - [4. Destroy All Droplets](#4-destroy-all-droplets)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

**Cloud-1** is an automated deployment project for a fully containerized web infrastructure. It leverages **DigitalOcean**, **Docker**, **Ansible**, and **Python** to seamlessly provision and configure servers that run a **WordPress** website backed by **MariaDB**, served through **Nginx**, and managed with **phpMyAdmin**.

This project aims to simplify the process of setting up scalable and secure web applications by automating each step, from server provisioning to application deployment.

## Features

- **Automated Server Provisioning**: Utilize a Python script to interact with the DigitalOcean API for creating and managing droplets.
- **Secure SSH Management**: Automatically register and manage SSH keys for secure server access.
- **Infrastructure as Code**: Use Ansible playbooks to configure servers, set up firewalls, and deploy Docker containers.
- **Containerized Services**:
  - **WordPress**: Easily deploy and manage your WordPress site.
  - **MariaDB**: Reliable and high-performance database backend.
  - **Nginx**: Efficient web server and reverse proxy.
  - **phpMyAdmin**: Web interface for managing your databases.
- **SSL Encryption**: Integrate SSL certificates for secure HTTPS connections.
- **Scalability**: Easily add or remove servers and services as needed.
- **Modular Design**: Customize and extend each component to fit specific needs.

## Prerequisites

Before getting started, ensure you have the following installed on your local machine:

- **Docker**: [Installation Guide](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Installation Guide](https://docs.docker.com/compose/install/)
- **Python 3.x**: [Installation Guide](https://www.python.org/downloads/)
- **Make**: Typically pre-installed on Unix systems. For Windows, consider using [Make for Windows](http://gnuwin32.sourceforge.net/packages/make.htm).
- **DigitalOcean Account**: [Sign Up](https://cloud.digitalocean.com/registrations/new)

## Installation

Follow these steps to set up and deploy the Cloud-1 project.

### 1. Clone the Repository

```bash
git clone https://github.com/hboissel/cloud-1.git
cd cloud-1
```

### 2. Set Up Environment Variables

#### a. Create `.env` Files

Create `.env` files:
- in the root directory to store API key for Digital Ocean
- in the website/srcs directory for the configuration of mariadb and wordpress accounts

You have examples with the files .envExamples

#### c. Obtain SSL Certificates

You can obtain SSL certificates using [Let's Encrypt](https://letsencrypt.org/).

Add yours in website/srcs/requirements/nginx/conf and website/srcs/requirements/phpmyadmin/cert

For nginx you need **fullchain.pem** and **privkey.pem**.
For phpmyadmin you need the same as for nginx plus **cert.pem**

### 3. Generate SSH Keys

Generate an SSH key pair that will be used for accessing the DigitalOcean droplets.

```bash
mkdir -p .ssh
ssh-keygen -f .ssh/id_ed25519 -t ed25519 -N ""
```
This command creates a new SSH key pair without a passphrase.

### 4. Build the Ansible Docker Container

We use Docker to containerize our Ansible setup for consistent and reproducible deployments.

#### a. Build the Docker Image

```bash
make build
```
This command will build the Docker image as defined in your `Makefile` and `Dockerfile`.

#### b. Verify the Docker Image

Ensure that the Docker image has been built successfully:

```bash
docker images
```
You should see an image corresponding to your Ansible setup.

## Usage

### 1. Access the Ansible Container

Enter the Ansible Docker container to perform deployment operations.

```bash
make ansible
```

This command will start a Docker container and drop you into a shell session inside it.

### 2. Create Droplets on DigitalOcean

Within the Ansible container, run the Python script to create new droplets.

#### a. Run the Script

```bash
manage_droplets
```

#### b. Follow the Prompts

- The script will check and register your SSH keys with DigitalOcean.
- It will list existing droplets tagged with `cloud-1`.
- You will be prompted to create new droplets:
  - Enter `yes` to proceed.
  - Provide a name for each droplet you wish to create.
  - Type `done` when finished adding droplets.

#### c. Verify Droplet Creation

The script will:

- Create the droplets using the DigitalOcean API.
- Wait until each droplet is active and retrieve their IP addresses.
- Save the IP addresses to the Ansible hosts file located at `/root/ansible/hosts`.
- Perform an Ansible ping test to verify connectivity.

**Example Output**:

```
🔑 SSH key is already registered.
🌊 Droplets with tag 'cloud-1':
ID: 12345678, Name: web-server-1, IP: 192.168.1.2
Do you want to create new droplets? (yes/no): yes
➕ Enter droplet name (or 'done' to finish): app-server-1
✅ Created droplet 'app-server-1' with ID: 87654321
⏳ Waiting for droplet ID 87654321 to become active...
✅ Droplet ID: 87654321, IP: 192.168.1.3
➕ Enter droplet name (or 'done' to finish): done

🌊 All cloud-1 droplet IPs:
192.168.1.2
192.168.1.3
💾 IPs saved to /root/ansible/hosts

⏳ Running Ansible ping test...
✅ Ansible ping test successful:
app-server-1 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
web-server-1 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

### 3. Deploy the Infrastructure with Ansible

Run the Ansible playbook to configure the servers and deploy the Dockerized infrastructure.

#### a. Navigate to the Ansible Directory

```bash
cd /root/ansible
```

#### b. Run the Playbook

```bash
ansible-playbook main.yml
```

#### c. Monitor the Deployment

The playbook will:

- Configure users and security settings.
- Install Docker and other dependencies.
- Synchronize source files for the Docker infrastructure.
- Build and start Docker containers as defined in your `docker-compose.yml`.

**Example Output**:

```
PLAY [Configure and deploy infrastructure] ************************************

TASK [Gathering Facts] ********************************************************
ok: [192.168.1.2]
ok: [192.168.1.3]

TASK [Init Setup] *************************************************************
changed: [192.168.1.2]
changed: [192.168.1.3]

...

PLAY RECAP ********************************************************************
192.168.1.2               : ok=10   changed=8    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.1.3               : ok=10   changed=8    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

#### d. Access Your Services

Once deployment is complete, your services should be up and running.

- **WordPress**: `https://yourdomain.com`
- **phpMyAdmin**: `https://yourdomain.com:8080`

### 4. Destroy All Droplets

When you need to tear down your infrastructure, use the following command within the Ansible container:

```bash
manage_droplets -d
```

**This will:**

- Destroy all droplets tagged with `cloud-1`.
- Clear the Ansible hosts file.

**Example Output**:

```
✅ All droplets with tag 'cloud-1' have been destroyed.
💾 IPs saved to /root/ansible/hosts
```

## Project Structure

```
cloud-1/
├── .env
├── .ssh/
│   ├── id_ed25519
│   └── id_ed25519.pub
├── ansible/
│   ├── hosts
│   ├── main.yml
│   ├── ansible.cfg
│   ├── playbooks/
├── website/
│   ├── srcs/
│   |   ├── requirements/
│   |   ├── docker-compose.yml
│   |   └── .env
│   └── Makefile
├── scripts/
│   └── manage_droplets.py
├── Makefile
├── Dockerfile
└── README.md
```

## Acknowledgements

- [DigitalOcean](https://www.digitalocean.com/) for their robust and developer-friendly cloud services.
- [Docker](https://www.docker.com/) for simplifying containerization.
- [Ansible](https://www.ansible.com/) for powerful automation capabilities.
- [Let's Encrypt](https://letsencrypt.org/) for providing free SSL certificates.
- [Certbot](https://certbot.eff.org/) for automating the certificate issuance process.
