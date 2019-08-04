# DESCRIPTION
A computer vision approach to detecting and counting boxes in an image.

![alt text][logo]
[logo]: https://github.com/julianaddison/counting_boxes/sample.PNG "Input and Results"

## INSTALLATION & USAGE
### TO RUN VIA DOCKER (RECOMMENDED)

FOR WINDOWS OS (MODIFY PATH FOR LINUX OS),
1. clone contents to a folder ./CountingBoxes

2. Launch Windows Powershell as Administrator or Linux shell
	
3. cd to docker file location

```bash
cd .\.\CountingBoxes\
```

4. Build docker image. Ensure the '.' is placed at the end of the line.
   **NOTE:** Ensure docker container has enough resources allocated. Go to docker > settings > advanced and configure resources
 
```bash
docker build -t countboxes .
```
	
5. Run docker - launch the container with a mounted volume, file will be saved on host filesystem when container exits
   Where countboxes outputs the CSV file to /CountingBoxes/data. File will be in the pwd/data/ folder on host filesystem

```bash
docker run -v $PWD/output:/CountBoxes/output countboxes
```

### TO RUN LOCALLY
1. copy content to a folder ./CountingBoxes

2. Install all packages and dependencies in requirements.txt

3. cd to .py location

```bash
cd ./CountingBoxes
``` 

4. Run script

```bash 
python count_boxes.py
```
 
---

## ADDITIONAL DOCKER COMMANDS

+ To stop, get docker container ID and replace f237e1000da3 by the actual ID
'''bash
docker container ls
docker container stop f237e1000da3
'''

+ To remove <none> tag docker images

```bash
docker rmi -f $(docker images -f dangling=true -q)
```

+ To remove all stopped containers

```bash
docker rm $(docker ps -a -q)
```

+ To remove container after running 

```bash
docker run --rm ssgtgs_demo 
```