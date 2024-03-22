# Docker and Python

For this assignment you will be combining Docker with Python to create a program that generates a QR code PNG file that
contains a URL. The QR code can be viewed with the camera on your phone to allow a user to click on it and send them to
the target website. You must make your program generate a QR code that takes someone to your GitHub homepage i.e. https://github.com/kaw393939 <replace mine with yours>

## Submission Requirements:

1. QR code that links to your GitHub homepage


## Lesson Video

[Instructor Video](https://youtu.be/ATajsJRFWEs)

## Readings / Tutorials - No, really you should read these

* [Official docker Getting Started - Go over all the sections](https://docs.docker.com/guides/get-started/)
* [Entrypoint vs. CMD vs. RUN ](https://codewithyury.com/docker-run-vs-cmd-vs-entrypoint/)
* [Make QR with Python](https://towardsdatascience.com/generate-qrcode-with-python-in-5-lines-42eda283f325)
* [Make Dockerfile](https://thenewstack.io/docker-basics-how-to-use-dockerfiles/)
* [Docker Compose File Basics](https://www.techrepublic.com/article/how-to-build-a-docker-compose-file/)
* [Args and Environment Variables in Docker](https://vsupalov.com/docker-arg-env-variable-guide/)
* [Docker Run Mount Local Windows Important Info](https://medium.com/@kale.miller96/how-to-mount-your-current-working-directory-to-your-docker-container-in-windows-74e47fa104d7)
* [How to run a program as another user in linux](https://unix.stackexchange.com/questions/232669/how-can-i-run-a-program-as-another-user-in-every-way)

### Building the Image

```sh
docker build -t my-qr-app .
```
This command builds a Docker image named `my-qr-app` from the Dockerfile in the current directory (`.`).

### Running the Container with Default Settings
```sh
docker run -d --name qr-generator my-qr-app
```

Runs your QR code generator application in detached mode (`-d`) with a container named `qr-generator`.

### Setting Environment Variables for QR Code Customization

```sh
docker run -d --name qr-generator \
  -e QR_DATA_URL='https://example.com' \
  -e QR_CODE_DIR='qr_codes' \
  -e QR_CODE_FILENAME='exampleQR.png' \
  -e FILL_COLOR='blue' \
  -e BACK_COLOR='yellow' \
  my-qr-app
```
Customizes the QR code generation settings through environment variables.

### Sharing a Volume for QR Code Output

```sh
docker run -d --name qr-generator \
  -v /host/path/for/qr_codes:/app/qr_codes \
  my-qr-app
```
Mounts a host directory to the container for storing QR codes.

### Combining Volume Sharing and Environment Variables

```sh
docker run -d --name qr-generator \
  -e QR_DATA_URL='https://example.com' \
  -e QR_CODE_DIR='qr_codes' \
  -e QR_CODE_FILENAME='exampleQR.png' \
  -e FILL_COLOR='blue' \
  -e BACK_COLOR='yellow' \
  -v /host/path/for/qr_codes:/app/qr_codes \
  my-qr-app
```

A comprehensive command that configures the QR code settings and mounts volumes for QR codes and logs.

### Basic Docker Commands Explained

**Building an Image**

```sh
docker build -t image_name .
```

Builds a Docker image with the tag `image_name` from the Dockerfile in the current directory.

**Running a Container**

```sh
docker run --name container_name image_name
```
Runs a container named `container_name` from `image_name` in the foreground / attached mode

```sh
docker run -d --name container_name image_name
```
Runs a container named `container_name` from `image_name` in detached mode

**Listing Running Containers**

```sh
docker ps
```
Shows a list of all running containers.

**Stopping a Container**

```sh
docker stop container_name
```
**Removing a Container**

```sh
docker rm container_name
```
**Listing Docker Images**


```sh
docker images
```
Lists all Docker images available on your machine.

**Removing a Docker Image**


```sh
docker rmi image_name
```

Removes a Docker image.

**Viewing Logs of a Container**

```sh
docker logs container_name
```
Displays the logs from a running or stopped container.

These commands cover the essentials of building, running, and managing Docker containers and images, along with specific examples for your QR code generation application.
