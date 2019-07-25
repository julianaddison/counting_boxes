DESCRIPTION:

----------
TO RUN VIA DOCKER (RECOMMENDED):

FOR WINDOWS OS (MODIFY PATH FOR LINUX OS),
1. copy content to a folder ./CountingBoxes

2. Launch powershell as Administrator
	
3. cd to docker file location
	> cd .\.\CountingBoxes\

4. Build docker image - Ensure the '.' is placed at the end of the line - NOTE: Ensure docker container has enough resources allocated. Go to docker > settings > advanced and configure resources 
	> docker build -t countboxes .
	
5. Run docker - launch the container with a mounted volume, file will be saved on host filesystem when container exits
   Where countboxes outputs the CSV file to /CountingBoxes/data. File will be in the pwd/data/ folder on host filesystem
	> docker run -v $PWD/output:/CountBoxes/output countboxes


TO RUN LOCAL:
1. copy content to a folder ./CountingBoxes

2.	Install all packages and dependencies in requirements.txt

3. cd to .py location
	> cd ./CountingBoxes 

4. Run script
    > python count_boxes.py
 
----------
ADDITIONAL DOCKER COMMANDS:

1. To stop, get docker container ID and replace f237e1000da3 by the actual ID
	> docker container ls
	> docker container stop f237e1000da3

2. To remove <none> tag docker images
    > docker rmi -f $(docker images -f dangling=true -q)

3. To remove all stopped containers
	> docker rm $(docker ps -a -q)

   To remove container after running 
	> docker run --rm ssgtgs_demo 