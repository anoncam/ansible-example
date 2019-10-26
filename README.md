# Ansible Playbook for Example Application
---

Installation and configuration of the example application can be found here.

# Pre-requisites for Example Application

## AWS infrastructure
Representative AWS infrastructure needs to in place.
Including:
  - [ ] host / instance with the appropriate subnet
  - [ ] service account keys installed with `sudo` / `su` that allows actions from an Ansible playbook
  - [ ] security groups

## Application Infrastructure Needs

Info for cluster, DB, etc.  You will find information on the supporting infrastructure.

### Sizing

Setup | Ram | Disk | AWS Instance Type
----- | --- | ---- | -----------------
Minimum | 2 GB | 700 MB | t2.small
MVP | 4 GB | 40 GB | t2.medium

### Base OS

OS | Instance Type | AMI ID
-- | ------------- | ------
RHEL 7.X | RHEL-7.6_HVM_GA-20181017-x86_64-0-Hourly2-GP2 | ami-a1d349c0


#### Port Information

Type | Port number | Description
---- | ----------- | -----------
TCP | 22 | SSH
HTTP | 8181 | Used by the web-based administration console; the default for web services endpoints
HTTPS | 8443 | Encrypted; used by the web-based administration console; the default for web services endpoints

## Software Dependencies

- Base OS updated
- Install java `java-1.8.0-openjdk`
- Install `python2-pip`

## Using this repository

To fully utilize the module features where there are dependencies on another repository exists, you will want to clone with recursive.  More information on using modules can be found at [Git documentation](https://git-scm.com/book/en/v2/Git-Tools-Submodules) or [Github documentation](https://github.blog/2016-02-01-working-with-submodules/).

Example clone:

```
git clone --recursive ssh://git@bitbucket.ngendevops.com:7999/ex/ansible-example.git
```

## Installation

Check and confirm the defaults found in `./defaults/main.yml`.  The role installs and configures Example Application, including AWS infrastructure.

Example invocation:

```
ansible-playbook -i inventory/inventory example-install.yml
```

## Application Setup Process
1. Build representative AWS infrastructure
  a. Create VPC
  b. Create EC2 instances
2. Configure AWS EC2 instances
  a. Update and install base packages
  b. Account Configuration
3. Application dependencies
  a. Get binaries
  b. Install binaries
4. Get the application binary
5. Install application binary
6. Configure application
7. Setup application for a service

## Initiate Playbook

Example invocation:

Depending on your scenario, environment variables will need to be set.  More information on credentials management can be found in [developer-notes.md](developer-notes.md)

```
ansible-playbook -i inventory/inventory example-install.yml
```

## Variables of Note

You are able to set specific configuration values and information with the following information. Just be sure to match the existing data structures and perform testing to help ensure your changes meet your expectations.

Variables have been named spaced to help prevent collision of configuration data.  All current variables, are defined and found in `roles/role-name/defaults/main.yml`

One example of how to override the variable information can be found in, [example-application-custom-example.yml](example-application-custom-example.yml).

### Specific to AWS Infrastructure Build Out:

Location | `ansible-example/roles/aws-initial/defaults/main.yml`
-------- | ---

Example information:
```yaml
example_vpc_name: example-vpc
example_vpc_key: example-key
example_vpc_key_material: "{{ lookup('file', 'keys/public/perspecta_ngendevops_dev.pub') }}"

example_project_name: ghost-train
example_created_by: Ansible

# Change CIDR Block
# IP CIDR block for the VPC
example_vpc_cidr_block: 10.1.1.0/28
example_aws_region: "us-gov-west-1"

# a map defining the subnets we will build in the VPC
example_vpc_subnets:
  example-subnet1:
    cidr: 10.1.1.0/28
    az: "{{ example_aws_region }}a"

# a list defining the security groups for our VPC
example_vpc_security_groups:
  - name: allow-example-public-ssh
    description: "Allow public SSH"
    rules:
      - proto: tcp
        cidr_ip: 0.0.0.0/0
        ports:
          - 22
  - name: allow-example-public-http
    description: "Allow example public http"
    rules:
      - proto: tcp
        cidr_ip: 0.0.0.0/0
        ports:
          - 8181
  - name: allow-example-public-https
    description: "Allow example public https"
    rules:
      - proto: tcp
        cidr_ip: 0.0.0.0/0
        ports:
          - 8443

# This list should contain the unique values for the instance
# "usage" parameter
example_usage_list:
  - example-usage

# Create the data structure for the EC2 instances.
example_instances:
  awsexample01:
    subnet: "{{ example_vpc_subnet_ids['example-subnet1'] }}"
    secgroup: ['allow-example-public-ssh', 'allow-example-public-http', 'allow-example-public-https']
    instancetype: t2.medium
    usage: example-usage
    image: ami-a1d349c0
    vol_device_name: /dev/xvda
    vol_type: gp2
    vol_size: 40
```

### Specific to Instance Configuration:

Location | `ansible-example/roles/configure-instances/defaults/main.yml`
-------- | ---

Example information:
```yaml
example_base_packages:
  - unzip
  - vim
  - wget
  - git
  - logwatch
```

### Specific to Application Configuration:

Location | `ansible-example/roles/example/defaults/main.yml`
-------- | ---

Example information:
```yaml
application_group: example_group
application_user: example_user
application_name: example_name

project_name: ghost-train
vpc_name: standalone-vpc

application_version: 6.2
remote_binary_url: "https://nexus.apps.ngendevops.com/repository/ghosttrain-app-zips/{{ application_name }}/"
# remote_binary_url: https://nexus.apps.ngendevops.com/repository/ghosttrain-app-rpms/
application_package_name: application-full-6.2.1.redhat-084
application_package: "{{ application_package_name }}.zip"
application_remote_username: "svcnexus"
aaplication_remote_password: "{{ lookup('env', 'NEXUS_SERVICE_ACCOUNT_PASSWORD') }}"

application_download_dir: /tmp/{{ application_name }}
application_install_dir: /var/{{ application_user }}
application_home_dir: /var/{{ application_user }}/application-6.2.1.redhat-084
application_configuration_file: "{{ application_home_dir }}/etc/org.apache.karaf.features.cfg"

application_users:
  -
    password: "{{ lookup('env', 'APPLICATION_ADMIN_ACCOUNT_PASSWORD') }}"
    roles:
      - Administrator
    username: admin
  -
    password: "{{ lookup('env', 'APPLICATION_GUEST_ACCOUNT_PASSWORD') }}"
    roles:
      - viewer
    username: guest

```

## Development Information
Development information can be found in [developer-notes.md](developer-notes.md), included is information on molecule testing.
