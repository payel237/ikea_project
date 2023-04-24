# Readme: Docker Setup for Jenkins

## Prerequisites
Before proceeding with the setup, please ensure that Docker software is preinstalled on your system. You can refer to the official Docker installation guide for Mac [here](https://docs.docker.com/desktop/install/mac-install/) for installation instructions.

## Step 1: Start Docker Instance
Start the Docker instance using the Docker image that has already been committed. Keep the process running and do not close the console. Use the following command:

```
docker run -p 8084:8080 -p 50004:50000 -v /var/jenkins_home --restart=on-failure ikea_project
```

## Step 2: Login to Jenkins GUI
Open your web browser and go to http://localhost:8084/. Provide the credentials when prompted, which were set when starting the Docker instance in the previous step.

## Step 3: Login to Docker Instance
To check the already running Docker instance, use the following command:

```
docker ps
```

Extract the Docker ID from the output, as it will be required to login to the Docker server.

## Step 4: Copy Jenkins Home Tar File
Copy the tar file of the Jenkins home to the Docker container. The tar file should have already been provided to you via email. Use the following command:

```
docker cp ~/Desktop/jenkins/job_bundle.tar <docker_id>:/var/jenkins_home
```

Replace `<docker_id>` with the Docker ID obtained in Step 3.

## Step 5: Login to Docker Instance
Login to the Docker instance using the following command:

```
docker exec -it <docker_id> /bin/bash
```

Replace `<docker_id>` with the Docker ID obtained in Step 3.

## Step 6: Extract Tar File in Jenkins Home Directory
Navigate to the Jenkins home directory inside the Docker instance using the following command:

```
cd /var/jenkins_home/
```

Extract the tar file in the Jenkins home directory using the following command:

```
tar -xvf job_bundle.tar
```

## Step 7: Restart Docker Instance
Exit from the Docker instance and restart the Docker instance using the Docker ID obtained in Step 3 with the following command:

```
docker restart <docker_id>
```

Replace `<docker_id>` with the Docker ID obtained in Step 3.

## Step 8: Run Jenkins Build
Login to Jenkins GUI again and navigate to the `ikea_assignment` project. Try running the build that is already present in the GUI.

That's it! You have successfully set up Jenkins using Docker and imported the Jenkins home configuration from a tar file.
