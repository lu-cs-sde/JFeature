
|_**Docker Image**_|[![DOI](https://upload.wikimedia.org/wikipedia/commons/d/df/Figshare_logo.svg)](https://figshare.com/articles/software/jfeature_scam22_tar_gz/20627295)|
|:------------|---------------|
|_**Repository**_|[![DOI](https://zenodo.org/badge/392981505.svg)](https://zenodo.org/badge/latestdoi/392981505)|x


Software corpora are crucial for evaluating research artifacts and ensuring repeatability of outcomes. _What do we know about these corpora? What do we know about their composition? Are they really suited for our particular problem?_

**JFeature** is an extensible static analysis tool that extracts syntactic and semantic features from Java programs, to assist developers in answering these questions.  

More details can be found in the related paper:
* __[JFeature: Know Your Corpus](https://github.com/lu-cs-sde/JFeature/blob/main/preprint.pdf)__, _[Idriss Riouak 🔗](https://github.com/IdrissRio), [Görel Hedin 🔗](https://cs.lth.se/gorel-hedin/), [Christoph Reichenbach 🔗](https://creichen.net) and [Niklas Fors 🔗](https://portal.research.lu.se/portal/en/persons/niklas-fors(c1e9efdd-5891-45ec-aa9d-87b8fb7f3dbc).html)_. _[IEEE-SCAM 2022 🔗](http://www.ieee-scam.org/2022/#home)._ 


---


**JFeature** supports twenty-eight different queries and can be easily extend
with new one. 

With **JFeature** you can:
  - Analyise and get insight of your own project
  - Analyses corpora and get insight of the each single project in the corups
  - Perform longitudinal studies (studies over time) of Java projects.

# Reusability
In the paper  __[JFeature: Know Your Corpus](https://github.com/lu-cs-sde/JFeature/blob/main/preprint.pdf)__, Section IV and Section V we discuss how JFeature can be extended and reused for several different purpose. 


# Get the JFeature artifact
We provide three different ways of getting and running **JFeature**:
  * You can download the pre-built Docker image (recommended).  
  * Build your own Docker image using the Dockerfile script.
  * Download and build **JFeature** from the artifact source code.


# Docker

We provide a [Docker](https://www.docker.com) image that contains *JFeature* and evaluation scripts, packaged together with all the necessary dependencies.
To run such an image, make sure to install the relevant tools:

* For Windows and OS X systems, follow the guidelines on the [Docker desktop download site](https://www.docker.com/products/docker-desktop)

* On Linux-based systems, install the docker command-line tool. This tool may be provided by the docker.io and/or docker-ce packages. If your distribution does not provide these packages, follow the steps here:
  * For [Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
  * For [Debian](https://docs.docker.com/engine/install/debian/)
  * For [CentOS](https://docs.docker.com/engine/install/centos/)
  * For [Fedora](https://docs.docker.com/engine/install/fedora/)
Users of other distributions can download [pre-compiled binaries](https://docs.docker.com/engine/install/binaries/) or build Docker from [source](https://github.com/docker) (both "cli" and "engine")


## Download pre-built Docker image
Download the pre-built image [here](https://figshare.com/articles/software/jfeature_scam22_tar_gz/20627295).
Then, anywhere in your workspace run

```
docker load < Downloads/jfeature_scam22.tar.gz
```

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
## Run the image

Run the image using:

```
docker run  -it --network="host" --expose 9000 --expose 9001 --memory="10g" --memory-swap="16g" jfeature
```



Once logged in, run the following commands to launch the evaluation:

```
cd workspace/jfeature/evaluation
./run_eval.sh arg

```
| ⚠️ Note          |
|:---------------------------|
|Where arg can be: 'true' will clone all the repositories in 'projects.json' and perform the evaluation, 'false' will just perform the evaluation without cloning the repositories, and 'only' will clone the repositories only without performing the evaluation. |

The results are saved in: `~/workspace/jfeature/evaluation/results/YYYYMMDDHHMMSS`

To generate a summary of the results run:

```
cd ~
cd workspace/jfeature/evaluation/
python3 table.py restuls/YYMMDDHHMMSS/
```
This will generate a summary of all the subresults and will save it in `table.txt`.
| ⚠️ Note          |
|:---------------------------|
|It might take several minutes to run the `table.py` script.|

| ❗️ Very Important ❗️         |
|:---------------------------|
 |Do not close the bash nor kill the container! The results will be lost!|

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
## Prerequisites

We have run JFeature on the following Java version:

*  **Java SDK version 8**. (tested with  SDK 8.0.275.fx-zulu. See [sdkman](https://sdkman.io)).


The evaluation script uses `sdkman`.
To run the evaluation you need:
* The scripts `eval.sh` and `evaluation/run_eval.sh` uses `sdkman`. If you don't have `sdkman` installed but have Java SDK 8 installed, you can comment all the lines starting with `sdk` in `eval.sh` and in `evaluation/run_eval.sh`. You install `sdkman` by running the following commands:

  ```
  curl -s "https://get.sdkman.io" | bash
  source "$HOME/.sdkman/bin/sdkman-init.sh"
  sdk install java 8.0.275.fx-zulu
  sdk use java 8.0.275.fx-zulu
  ```

To install all the necessary Python dependencies, you can run the instruction described in the next section.


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

### Python Dependencies

To install Python dependencies, you can execute the following instruction:

```
pip install 'numpy==1.19.5' 'pandas==1.1.5' 'matplotlib==3.3.4' 'seaborn==0.11.1' 'ipython==7.16.0' 'PyPDF2==1.26.0' 'Pillow==6.2.2' 'tabulate==0.8.9'
```

---



### Repository overview
The top-level structure of the repository:

    .
    ├── build                                # Compiler generaterd files
    ├── evaluation                           # Scripts and dependencies for evaluation
    ├── extendj                              # ExtendJ source code (Submodule)
    ├── src                                  # JFeature source code
    |    ├── jastadd                  
    |    |     ├── Extension.jrag            # Extension example (Paper §4)
    |    |     ├── Java4.jrag                # Java 1-4 features
    |    |     ├── Java5.jrag                # Java 5 features
    |    |     ├── Java7.jrag                # Java 7 features
    |    |     ├── Java8.jrag                # Java 8 features
    |    |     └── Utils.jrag                # Helper attributes
    |    └── java
    |          ├── feature -- Feature.java   # Feature class
    |          └── App.java                  # Main method
    |          └── Utils.java                # Helper methods
    # JUnit test spec
    ├── tools                                # JFeature source code
    |    └── jastadd2.jar                    # Jastadd version 2.3.4-50-gf00c118
    ├── testfiles                            # Automated test files
    |    ├── JAVA4
    |    ├── JAVA5
    |    ├── JAVA7
    |    └── JAVA8
    ├── LICENSE
    └── README.md

| ⚠️ Note          |
|:---------------------------|
|There is no subdirectory for `JAVA6`, since no relevant features were introduced in Java 6. |

The _entry point_ of **JFeature** (main) is defined in:
`extendj/src/java/App.java`.


### The _evaluation_ folder
The directory is structured as follow:

    .
    ├── projects.json                        # Containing details about corpora's projects 
    ├── run_eval.sh                          # Evaluation entry-point script              
    ├── table.py                             # Python script used to collect data
    └── results/YYYYMMDDHHMMSS               # Evaluation results



---
# Related repository repositories/links 🔗
 - 🔗 **[JastAdd](https://jastadd.org)**: meta-compilation system that supports Reference Attribute Grammars. 
 - 🔗 **[ExtendJ](https://extendj.org)**: extensible Java compiler built using JastAdd. We built **JFeature** as an Static Analysis Extension of ExtendJ. More can be found [here](https://bitbucket.org/extendj/analysis-template/src/master/). 
 - 🔗 **[DaCapo](https://dacapo-bench.org/)**: Blackburn et al. introduced it in 2006 as a set of general-purpose (i.e., library), freely available, real-world Java applications. They provided performance measurements and workload characteristics, such as object size distributions, allocation rates and live sizes. Even if the primary goal of the
DaCapo Benchmark Suite is intended as a corpus for Java benchmarking, there are
several instances of frontend and static analysers evaluation.
For evaluation, we used version 9.12-bach-MR1 released in 2018.
 - 🔗 **[Defects4J](https://github.com/rjust/defects4j)**: introduced by Just et al., is a bug database consisting of 835 real-world bugs from 17 widely-used open-source Java projects.
Each bug is provided with a test suite and at least one failing test case that triggers the bug.
Defects4J found many uses in the program analysis and repair community.
For evaluation, we used version 2.0.0 released in 2020..
 - 🔗 **[Qualitas Corpus](http://qualitascorpus.com/)**:  is  a set of 112 open-source Java programs, characterised by different sizes and belonging to different
application domains.  The corpus was specially designed for empirical software engineering research and static analysis.
For evaluation, we used the release from 2013 (20130901).
 - 🔗 **[XCorpus](https://bitbucket.org/jensdietrich/xcorpus/src/master/)**: is a corpus of modern real Java programs with an explicit goal of being a target for analysing dynamic proxies. XCorpus provides a set of 76 executable, real-world Java programs, including a subset of 70 programs from the Qualitas Corpus. The corpus was designed
to overcome a lack of a sufficiently large and general corpus to validate static and dynamic analysis artefacts. The six additional projects added in the XCorpus make use of dynamic language features, i.e., invocation handler.
For evaluation, we used the release from 2017..

