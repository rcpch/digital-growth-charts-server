---
title: Docker development
reviewers: Dr Marcus Baw, Dr Sean Cusack, Dr Anchit Chandran
audience: developers
---

# Developing locally in a Docker container

Docker containers avoid many of the problems and irritating snags related to conflicting versions of Python and libraries when setting up a development environment on your machine.

In the Dockerized environment, all the code is running in an isolated virtual environment, so there are no version conflicts. This is similar to a virtual machine, but more efficient in terms of resources.

The Docker container closely resembles our deployment environment, helping to prevent “Well It Works On *My* Machine”-type deployment difficulties.

## Running the API server locally in Docker

If you haven’t already, `git clone` the server repository to a suitable place on your local machine.

```bash
git clone https://github.com/rcpch/digital-growth-charts-server.git
```

## Scripts

The `s/` folder contains some simple scripts to help with development.

To run them, ensure they are made executable in your filesystem. This may not happen by default, depending on your OS. You can do that in whatever File > Permissions > Make Executable menu your desktop provides. For \*nix environments or the WSL, you can type `chmod +x <filename>` to add executable permissions.

Run all scripts from the root of the project, or they won't work.

## Build the Docker image with all required dependencies

Run the `s/build-docker` script, which builds the Docker image with all the required dependencies/

This is useful for rapid development environment set-up. It pulls the `python` Docker base image, deletes any existing identically-named images, and builds the new image with the server code linked into it.

## Start the Docker container

Run the `s/start-docker` script, which will run the image in a Docker container.

The dGC server will then be running in development mode in the container. It will be available at <https://localhost:5000>.
