# Developer Notes
----

## EXAMPLE

This repo is used as an example that enables quick cloning and setup for the basic structure needed for an application playbook.

## Secrets Management

The ansible playbook needs certain credentials to complete it's configuration in the runtime environment. These credentials are not being stored in the repository.  The credentials are needed at run time, as a result, the playbook needs certain environment variable set.  The following are needed and provided with example information:

### Access to Running AWS instance

Local playbook runtime environment private key example:

```
ssh-add -K  ~/.ssh/perspecta_ngendevops_dev
```

Ansible Tower playbook runtime environment private key example:

- Install or ensure that the `perspecta_ngendevops_dev` private key is setup in _credentials_ for use by Ansible Tower.

### Access to External Systems

Local playbook runtime example to set environment variables:

```
AWS_ACCESS_KEY_ID=AskYourAWSinfrastructureManager
AWS_SECRET_ACCESS_KEY=AskYourAWSinfrastructureManager4Secret
NEXUS_SERVICE_ACCOUNT_PASSWORD=AskYourNexusManager
APPLICATION_ADMIN_ACCOUNT_PASSWORD=SetYourPassword
APPLICATION_GUEST_ACCOUNT_PASSWORD=SetYourPassword
```

Molecule runtime environment example:

Be sure to set environment variables in the docker container when iniating `molecule test`:

```
NEXUS_SERVICE_ACCOUNT_PASSWORD=AskYourNexusManager
```

Ansible Tower runtime environment variables example:

- Install or ensure that the `Amazon Web Services` credential type is setup for use by Ansible Tower.
- Install or ensure that the `nexus-service-account-creds` custom credential type is setup for use by Ansible Tower.

Additional information on Ansible Tower setup can be found [here](https://bitbucket.ngendevops.com/projects/AT/repos/tower-config/browse).


## Molecule Development Environment

Information around developing around docker containers. How to setup to run molecule testing. More information can be found in [molecule.md](molecule.md)

You can utilize a docker container in your local development environment for playbook development and testing. Run the following from the `/ansible-example/roles` directory

```
docker run --rm -it -w /usr/src/app -v ${PWD}:/usr/src/app -v /var/run/docker.sock:/var/run/docker.sock quay.io/ansible/molecule:latest /bin/sh
```

## BUILDING WINDOWS EC2

Make sure that you export an environment variable named `WINDOWS_PASSWORD`. The ec2 userdata script will set the password during boot.
