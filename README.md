This repo is for test Cisco ACI python scripts. These scripts are based off of walking through the Cisco ACI Automation course on Udemy. https://www.udemy.com/course/cisco-aci-automation

A good starting point for the resouces necessary can be found in the ACI Toolkit repo:
https://github.com/datacenter/acitoolkit


# Description

The ACI Toolkit is a set of python libraries that allow basic
configuration of the Cisco APIC controller. It is intended to allow users to quickly begin using the REST API and accelerate the learning curve necessary to begin using the APIC.

The full documentation is published at the following link:
[http://datacenter.github.io/acitoolkit/](http://datacenter.github.io/acitoolkit/)


# Installation

## Environment

Required

* Python 2.7+
* [setuptools package](https://pypi.python.org/pypi/setuptools)

## Downloading

### Option A:

If you have git installed, clone the repository

    git clone https://github.com/datacenter/acitoolkit.git

### Option B:

If you don't have git, [download a zip copy of the repository](https://github.com/datacenter/acitoolkit/archive/master.zip) and extract.

### Option C:

The latest build of this project is also available as a Docker image from Docker Hub

    docker pull dockercisco/acitoolkit 

## Installing

After downloading, install using setuptools.

    cd acitoolkit
    python setup.py install

If you plan on modifying the actual toolkit files, you should install the developer environment that will link the package installation to your development directory.

    cd acitoolkit
    python setup.py develop

# Usage

A tutorial and overview of the acitoolkit object model can be found in
the Documentation section found at
[http://datacenter.github.io/acitoolkit/](http://datacenter.github.io/acitoolkit/)


# Using Docker Image

```
docker run -it --name acitoolkit dockercisco/acitoolkit
```
