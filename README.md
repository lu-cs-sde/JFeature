
|_**Docker Image**_|[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7053443.svg)](https://doi.org/10.5281/zenodo.7053443)|
|:------------|---------------|
|_**Repository**_| This Repository |x


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


# Requirements
Before getting **JFeature**, ensure that your machine meets all hardware and software requirements described in [REQUIREMENTS.md](https://github.com/lu-cs-sde/JFeature/blob/main/REQUIREMENTS.md).

# Get JFeature 
We provide three different ways of getting and running **JFeature**:
  * You can download the pre-built Docker image (recommended).  
  * Build your own Docker image using the Dockerfile script.
  * Download and build **JFeature** from the artifact source code.

The three different steps are described in [INSTALL.md](https://github.com/lu-cs-sde/JFeature/blob/main/INSTALL.md).




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

