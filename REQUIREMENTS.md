### Tested on:
The three installation methods (see INSTALL.md), were tested on: 

| Kind                        | CPU                             | Memory      | HDD/SSD | OS Version                          |
|-----------------------------|---------------------------------|-------------|---------|-------------------------------------|
| MacBook Pro (16-inch, 2019) | 2,6 GHz, 6-Core Intel Core i7   | 16 GiB DDR4 | 500 GiB | macOS Monterey 12.5.1               |
| MacBook Pro (16-inch, 2021) | Apple M1 Pro                    | 16 GiB      | 1 TiB   | macOS Monterey 12.2.1               |
| 2 Benchmarking Machines      | 3.6 GHz, 8-Core Intel i7-11700K | 128GiB DDR4 | 1TiB    | Linux version 5.13.7-051307-generic |

| ⚠️ Note          |
|:---------------------------|
|If you wish to duplicate the evaluation findings, we recommend allocating a minimum of 100 Gigabytes of memory. The evaluation scripts will download more than one hundred repositories. |



---


# Requirements

* `zsh` for Ubuntu: zsh 5.8 (x86_64-ubuntu-linux-gnu)
* `zsh` for MacOS: zsh 5.8.1 (x86_64-apple-darwin21.0)

## Docker

We provide a [Docker](https://www.docker.com) image that contains *JFeature* and evaluation scripts, packaged together with all the necessary dependencies.
To run such an image, make sure to install the relevant tools:

* For Windows and OS X systems, follow the guidelines on the [Docker desktop download site](https://www.docker.com/products/docker-desktop)

* On Linux-based systems, install the docker command-line tool. This tool may be provided by the docker.io and/or docker-ce packages. If your distribution does not provide these packages, follow the steps here:
  * For [Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
  * For [Debian](https://docs.docker.com/engine/install/debian/)
  * For [CentOS](https://docs.docker.com/engine/install/centos/)
  * For [Fedora](https://docs.docker.com/engine/install/fedora/)
Users of other distributions can download [pre-compiled binaries](https://docs.docker.com/engine/install/binaries/) or build Docker from [source](https://github.com/docker) (both "cli" and "engine")


## Getting Java
| ⚠️ Note          |
|:---------------------------|
|If you are utilising the given Docker image, there is no need to continue with the steps below. The docker image has already installed all prerequisites. |

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



## Python (3.9.13) Dependencies
| ⚠️ Note          |
|:---------------------------|
|If you are utilising the given Docker image, there is no need to continue with the steps below. The docker image has already installed all prerequisites. |

To install Python dependencies, you can execute the following instruction:

```
pip install 'numpy==1.19.5' 'pandas==1.1.5' 'matplotlib==3.3.4' 'seaborn==0.11.1' 'ipython==7.16.0' 'PyPDF2==1.26.0' 'Pillow==6.2.2' 'tabulate==0.8.9'
```

---
