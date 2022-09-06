| ❗️ Very Important ❗️         |
|:---------------------------|
 |Before beginning the installation procedure, ensure that your machine meets all hardware and software requirements described in [REQUIREMENTS.md](https://github.com/lu-cs-sde/JFeature/blob/main/REQUIREMENTS.md).|



# Get JFeature
We provide three different ways of getting and running **JFeature**:
  * You can download the pre-built Docker image (recommended).  
  * Build your own Docker image using the Dockerfile script.
  * Download and build **JFeature** from the artifact source code.


# Docker

## Download pre-built Docker image
Download the pre-built image [here](https://github.com/lu-cs-sde/JFeature).
Then, anywhere in your workspace run

```
docker load < Downloads/jfeature_scam22.tar.gz
```
🛠 Troubleshooting
| ERROR |     SOLUTION    |
|:-------------------|--------|
| `Got permission denied while trying to connect to the Docker daemon socket at unix`.| Run the command as super user preappending `sudo` |
| If the error persits| Run the following commands (checkout [this](https://linuxhandbook.com/docker-permission-denied/) guide): `sudo groupadd docker`, `sudo usermod -aG docker $USER` |

## Build your own Docker image
Clone the JFeature repository by running the following command:
```
git clone https://github.com/lu-cs-sde/JFeature.git
```
Once you have cloned the repository
```
cd JFeature/Docker
docker build -t jfeature . --no-cache
```

| ⚠️ Note          |
|:---------------------------|
|It might take several minutes to build the Docker image.|


*Optional:*  Save the image as `.tar` file:
```
docker save jfeature | gzip > jfeature_scam22.tar.gz
```


## Run the image

Run the image using:

```
docker run  -it --network="host" --expose 9000 --expose 9001 --memory="10g" --memory-swap="16g" jfeature
```



Once logged in, run the following commands to launch the evaluation:

```
cd workspace/jfeature/evaluation
zsh run_eval.sh arg

```

Where arg can be: 
* `true` will clone all the repositories in 'projects.json' and perform the evaluation, 
* `false` will just perform the evaluation without cloning the repositories, and 
* `only` will clone the repositories only without performing the evaluation. 
  

| ❗️ Very Important ❗️         |
|:---------------------------|
 |Be sure you are using `zsh run_eval.sh arg` and not `./run_eval.sh arg`. The latter will generate a `permission denied` error.|

The results are saved in: `~/workspace/jfeature/evaluation/results/YYYYMMDDHHMMSS`

To generate a summary of the results run from the `evaluation` directory the following command:

```
python3 table.py results/YYMMDDHHMMSS/
```
This will generate a summary of all the subresults and will save it in `table.txt`.
| ⚠️ Note          |
|:---------------------------|
|It might take several minutes to run the `table.py` script.|

| ❗️ Very Important ❗️         |
|:---------------------------|
 |Do not close the bash nor kill the container or the results will be lost!|

## Saving the results
To save the results in your own machine, run the following commands in a new bash:
```
> docker ps
```
This will print:
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
4d882c86b5ab   jfeature   "bash"    x   Up x seconds  random_name
```
With *your* CONTAINER ID run the following command:

```
docker cp 4d882c86b5ab:workspace/jfeature/evaluation/YYYYMMDDHHMMSS /PATH/IN/YOUR/MACHINE
```




# Build JFeature from the source code

## Build
To clone the **JFeature** code, run, in your working directory:
```
git clone https://github.com/lu-cs-sde/JFeature.git
```

Move to the **JFeature** directory:

```
cd JFeature
```

Clone all the submodules:

```
git submodule update
git submodule init
```

To generate the JARs necessary for the evaluation, execute

```
./gradlew build
```

| ⚠️ Note          |
|:---------------------------|
|See section 'Run the Image' to know how reproduce the results|


