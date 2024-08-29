#!/usr/bin/env python3

import os
import requests
import time
from pathlib import Path
from dotenv import load_dotenv
import subprocess

# Load environment variables from .env file if present
load_dotenv()

# Constants
DO_API_URL = "https://api.digitalocean.com/v2"
SSH_KEY_PATH = str(Path.home() / ".ssh/id_ed25519.pub")
HOSTS_FILE_PATH = "/root/ansible/hosts"
DIGITALOCEAN_SSH_FINGERPRINT = "SSH_KEY_FINGERPRINT"
TAG_NAME = "cloud-1"

# Emojis for user interaction
EMOJI_KEY_CHECK = "🔑"
EMOJI_CLOUD = "🌊"
EMOJI_SUCCESS = "✅"
EMOJI_WAIT = "⏳"
EMOJI_ERROR = "❌"
EMOJI_SAVE = "💾"
EMOJI_PLUS = "➕"

# Function to check if the SSH key is already registered on DigitalOcean
def get_registered_ssh_keys():
    headers = {
        "Authorization": f"Bearer {os.getenv('DIGITALOCEAN_TOKEN')}",
        "Content-Type": "application/json",
    }
    response = requests.get(f"{DO_API_URL}/account/keys", headers=headers)
    response.raise_for_status()
    return response.json()["ssh_keys"]

# Function to register the SSH key if it's not registered
def register_ssh_key():
    with open(SSH_KEY_PATH, 'r') as f:
        public_key = f.read().strip()

    registered_keys = get_registered_ssh_keys()
    for key in registered_keys:
        if key["public_key"] == public_key:
            print(f"{EMOJI_KEY_CHECK} SSH key is already registered.")
            return key["fingerprint"]

    # Register the SSH key
    headers = {
        "Authorization": f"Bearer {os.getenv('DIGITALOCEAN_TOKEN')}",
        "Content-Type": "application/json",
    }
    data = {
        "name": TAG_NAME,
        "public_key": public_key,
    }
    response = requests.post(f"{DO_API_URL}/account/keys", headers=headers, json=data)
    response.raise_for_status()
    fingerprint = response.json()["ssh_key"]["fingerprint"]
    print(f"{EMOJI_KEY_CHECK} SSH key registered with fingerprint: {fingerprint}")
    return fingerprint

# Function to list all droplets with the specified tag
def list_droplets():
    headers = {
        "Authorization": f"Bearer {os.getenv('DIGITALOCEAN_TOKEN')}",
        "Content-Type": "application/json",
    }
    response = requests.get(f"{DO_API_URL}/droplets?tag_name={TAG_NAME}", headers=headers)
    response.raise_for_status()
    droplets = response.json()["droplets"]
    if not droplets:
        print(f"{EMOJI_ERROR} No droplets found with tag '{TAG_NAME}'.")
    else:
        print(f"{EMOJI_CLOUD} Droplets with tag '{TAG_NAME}':")
        for droplet in droplets:
            print(f"ID: {droplet['id']}, Name: {droplet['name']}, IP: {droplet['networks']['v4'][0]['ip_address']}")
    return droplets

# Function to create a new droplet
def create_droplet(name, ssh_key_fingerprint):
    headers = {
        "Authorization": f"Bearer {os.getenv('DIGITALOCEAN_TOKEN')}",
        "Content-Type": "application/json",
    }
    data = {
        "name": name,
        "region": "fra1",
        # "size": "s-1vcpu-512mb-10gb",
        "size": "s-4vcpu-8gb-amd",
        "image": "ubuntu-20-04-x64",
        "ssh_keys": [ssh_key_fingerprint],
        "tags": [TAG_NAME],
    }
    response = requests.post(f"{DO_API_URL}/droplets", headers=headers, json=data)
    response.raise_for_status()
    droplet = response.json()["droplet"]
    print(f"{EMOJI_SUCCESS} Created droplet '{name}' with ID: {droplet['id']}")
    return droplet

# Function to wait for droplets to become active and get their IPs
def wait_for_droplet_ip(droplet_id):
    headers = {
        "Authorization": f"Bearer {os.getenv('DIGITALOCEAN_TOKEN')}",
        "Content-Type": "application/json",
    }
    while True:
        response = requests.get(f"{DO_API_URL}/droplets/{droplet_id}", headers=headers)
        response.raise_for_status()
        droplet = response.json()["droplet"]
        if droplet["status"] == "active":
            ip_address = droplet["networks"]["v4"][0]["ip_address"]
            print(f"{EMOJI_SUCCESS} Droplet ID: {droplet_id}, IP: {ip_address}")
            return ip_address
        print(f"{EMOJI_WAIT} Waiting for droplet ID {droplet_id} to become active...")
        time.sleep(10)

# Function to save IPs to Ansible hosts file
def save_ips_to_ansible_hosts(ips):
    with open(HOSTS_FILE_PATH, 'w') as f:
        f.write("[cloud1]\n")
        for ip in ips:
            f.write(f"{ip}\n")
    print(f"{EMOJI_SAVE} IPs saved to {HOSTS_FILE_PATH}")

def destroy_all_droplets():
    headers = {
        "Authorization": f"Bearer {os.getenv('DIGITALOCEAN_TOKEN')}",
        "Content-Type": "application/json",
    }
    response = requests.delete(f"{DO_API_URL}/droplets?tag_name={TAG_NAME}", headers=headers)
    if response.status_code == 204:
        print(f"{EMOJI_SUCCESS} All droplets with tag '{TAG_NAME}' have been destroyed.")
    else:
        print(f"{EMOJI_ERROR} Failed to destroy droplets. Status code: {response.status_code}")

def test_ansible_ping():
    print(f"\n{EMOJI_WAIT} Running Ansible ping test...")
    # Path to the Ansible hosts file
    hosts_file = "/root/ansible/hosts"

    # Command to run the Ansible ping module on all hosts in the hosts file
    command = ["ansible", "all", "-i", hosts_file, "-m", "ping"]

    try:
        # Run the command and capture the output
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"{EMOJI_SUCCESS} Ansible ping test successful:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"{EMOJI_ERROR} Ansible ping test failed:\n{e.stderr}")


def main():
    # Check if the first argument is '-d' for destroying all droplets
    if len(os.sys.argv) > 1 and os.sys.argv[1] == "-d":
        destroy_all_droplets()
        save_ips_to_ansible_hosts([])
        return

    # Check or register SSH key
    ssh_key_fingerprint = os.getenv(DIGITALOCEAN_SSH_FINGERPRINT)
    if not ssh_key_fingerprint:
        print(f"{EMOJI_KEY_CHECK} SSH key fingerprint not found in environment, checking registration...")
        ssh_key_fingerprint = register_ssh_key()
        os.environ[DIGITALOCEAN_SSH_FINGERPRINT] = ssh_key_fingerprint

    # List existing droplets
    droplets = list_droplets()

    # Ask if new droplets should be created
    create_new = input("Do you want to create new droplets? (yes/no): ").strip().lower()
    new_droplet_ips = []
    if create_new == "yes":
        while True:
            name = input(f"{EMOJI_PLUS} Enter droplet name (or 'done' to finish): ").strip()
            if name.lower() == "done":
                break
            droplet = create_droplet(name, ssh_key_fingerprint)
            ip = wait_for_droplet_ip(droplet["id"])
            new_droplet_ips.append(ip)

    # Collect all droplet IPs
    all_ips = [droplet['networks']['v4'][0]['ip_address'] for droplet in droplets] + new_droplet_ips

    # Print and save IPs to Ansible hosts file
    print(f"\n{EMOJI_CLOUD} All cloud-1 droplet IPs:")
    for ip in all_ips:
        print(ip)
    save_ips_to_ansible_hosts(all_ips)
    test_ansible_ping()

if __name__ == "__main__":
    main()
