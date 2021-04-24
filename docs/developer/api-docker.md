# Running locally in Docker

## Running the API server locally in Docker

`git clone` the server repository, if you haven't already, to a suitable place on your local machine.

```bash
git clone https://github.com/rcpch/digital-growth-charts-server.git
```

## Scripts

The `s/` folder contains some simple scripts to help with development. To run them, ensure they are made executable in your filesystem (they may not be by default depending on your OS).

You can do that in whatever File > Permissions > Make Executable menu your desktop provides, or for \*nix environments or the WSL you can type `chmod +x <filename>` to add executable permissions.

Run all scripts from the root of the project, or they won't work.

## Build the Docker image with all required dependencies

run the `s/build-docker` script which will build the Docker image with all the required dependencies

This is useful for rapidly getting a development environment set up. It pulls the `python` Docker base image, deletes any existing identically-named images, and builds the new image with the server code linked into it.

## Start the Docker container

run the `s/start-docker` script, which will run the image in a Docker container.

The dGC server should be running in development mode in the container, and mapped to the port https://localhost:5000
