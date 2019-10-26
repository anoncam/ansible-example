## Developing with Molecule

Molecule is the official testing tool by RedHat and is designed to aid in the development and testing of Ansible roles.

Molecule provides support for testing with multiple instances, operating systems and distributions, virtualization providers, test frameworks and testing scenarios.

Molecule encourages an approach that results in consistently developed roles that are well-written, easily understood and maintained.

Molecule allows for the linting and testing of playbooks inside of a specified docker environment without the need to leverage inventories or hosts.

### Prerequisites

1. Docker
2. Ansible
3. Python

### Installing Molecule

To install Molecule, using ```pip```, you can run:

```
pip install molecule
```

To check if it's working:

```
molecule --version
molecule, version 2.20.0
```

Or you can use ```Docker``` to pull in your current directory into a container with ```Molecule``` installed by running this command:

```
docker run --rm -it -w /usr/src/app -v ${PWD}:/usr/src/app -v /var/run/docker.sock:/var/run/docker.sock quay.io/ansible/molecule:latest /bin/sh
```

To check if it's working:

```
molecule --version
molecule, version 2.20.0
```

### Initializing a New Ansible Role With Molecule

Molecule allows for the ability to create new Ansible Roles leveraging ```ansible-galaxy``` to create a new role with the molecule folder injected into the new directory, to create the new role you can use:

```
molecule init role -r molecule.example -d docker
```
The command:

```Molecule Init role``` creates a new role.
```-r molecule.example``` specifies the name of the new role.
```-d docker``` is used by default but is used here for the example.

Inside of the created Molecule directory is a default directory that indicates the default test scenario. It contains:

```
$ cd molecule.example/molecule/default/ && ls
Dockerfile.j2
INSTALL.rst
molecule.yml
playbook.yml
tests
```

### Initializing Molecule in an existing Ansible Role

To add molecule to an existing Ansible role, navigate to the roles directory:

```
└── Roles
    ├── existingRole
    ├────*run command in this directory*
    ├──── tasks
    ├──── defaults
    ├──── meta
    ├──── vars
```

In that directory you can then run:

```
molecule init scenario -r roleName
```

### Running Your First Molecule Test

Here's a quick rundown of what these files and directories are used for:

* Dockerfile.j2: This is the Dockerfile used to build the Docker container used as a test environment for your role. You can customize it to your heart's content, and you can even use your own Docker image instead of building the container from scratch every time. The key is this makes sure important dependencies like Python, sudo, and Bash are available inside the build/test environment.
* INSTALL.rst: Contains instructions for installing required dependencies for running molecule tests.
* molecule.yml: Tells molecule everything it needs to know about your testing: what OS to use, how to lint your role, how to test your role, etc.
* playbook.yml: This is the playbook Molecule uses to test your role. For simpler roles, you can usually leave it as-is (it will just run your role and nothing else). But for more complex roles, you might need to do some additional setup, or include other roles prior to running your role.
* tests/: This directory contains a basic Testinfra test, which you can expand on if you want to run additional verification of your build environment state after Ansible's done its thing.

To run your first test from the same directory that contains your molecule folder:

```
├── *molecule.example*
│   ├── files
│   ├── molecule
│   │   └── default
│   │       └── tests
│   └── tasks
```

you can run the command:

```
molecule test
```

The output will look like:

```
Validation completed successfully.
--> Test matrix

└── default
    ├── lint
    ├── destroy
    ├── dependency
    ├── syntax
    ├── create
    ├── prepare
    ├── converge
    ├── idempotence
    ├── side_effect
    ├── verify
    └── destroy

--> Executing Yamllint on files found in /molecule.example/...
Lint completed successfully.
--> Action: 'syntax'
    playbook: /molecule.example/molecule/default/playbook.yml
--> Action: 'converge'
--> Action: 'idempotence'
Idempotence completed successfully.
...
```

Since the role was created without actual ansible code the test will have passed successfully.

You can also just run yamllint and Ansible Lint using the command:

```
molecule lint
```

As you develop your ansible code, when running ```molecule lint``` you will get information pertaining to specific files and possible syntax errors are found in your playbook.

### Using Molecule Converge for Quick Playbook Execution Tests

One of the more useful commands to use is ```molecule converge```.

This will create the docker image that is specified in the ```Dockerfile.j2``` file and will run your playbook within the container to test if the playbook will run correctly.

```
molecule converge
<Do some work>
molecule converge
<See that some additions didn't work>
molecule converge
<see everything working well>
molecule converge
<idempotence check - make sure Ansible doesn't report any changes on a second run>
molecule destroy # which destroys the docker container that was created
```

### Using Molecule Test to test Ansible Playbooks

As mentioned in the docs, whithin the tests/ directory in the molecule/defaults folder there contains a standard test_default.py file which contains a default test using [testinfra](https://testinfra.readthedocs.io/en/latest/modules.html) that will always pass.

For example purposes, if you were using ansible to create an nginx deployment for example you could write a test that will check if nginx is installed and the service is running.

```
def test_nginx_is_installed(host):
    nginx = host.package("nginx")
    assert nginx.is_installed
    assert nginx.version.startswith("1.2")


def test_nginx_running_and_enabled(host):
    nginx = host.service("nginx")
    assert nginx.is_running
    assert nginx.is_enabled
```

After running `Molecule Converge` it will create your container which you can test against. Then by running `Molecule Verify` it will run the test against the created container.

After running a test you will get an output like below.

```
Validation completed successfully.
--> Test matrix

└── default
    └── verify

--> Scenario: 'default'
--> Action: 'verify'
--> Executing Testinfra tests found in /usr/src/app/elasticsearch/molecule/default/tests/...
    ============================= test session starts ==============================
    platform linux -- Python 3.7.2, pytest-4.3.1, py-1.8.0, pluggy-0.9.0
    rootdir: /usr/src/app/elasticsearch/molecule/default, inifile:
    plugins: testinfra-1.19.0
collected 3 items

    tests/test_default.py ...                                                [100%]
```

To follow Test Driven Development it will be useful to use this test as a baseline for functionaility.

If you have any questions reach out to ##### if you have any questions or concerns.

For more information visit [https://molecule.readthedocs.io/en/latest/index.html]
