# revbayes_kernel
A Jupyter kernel for RevBayes

### Installing revbayes_kernel

```sh
sudo python3 setup.py install
python3 -m revbayes_kernel.install
pip3 install metakernel
```

Note that Linux users may have to subsitute

```
python3 -m revbayes_kernel.install install
```

for the middle line.

### RevBayes Compilation

RevBayes [pre-built executables](https://github.com/revbayes/revbayes/releases/tag/v1.2.2-preview1) are designed to work with Jupyter. The `rb` executable must be found using the `which` command or be located using the environment variable, `REVBAYES_JUPYTER_EXECUTABLE`. For instance, you can set the environment variable using

```sh
export REVBAYES_JUPYTER_EXECUTABLE=<revbayes_path>/rb
```

If you are compiling your own copy, RevBayes must be compiled with the `-jupyter` or `-j` flags, like so:

`./build.sh -jupyter true`

This functionality was added to the development branch in commit [15b440a](https://github.com/revbayes/revbayes/commit/15b440a7013e46c08c9472a89fe1e91508c49c3c).


### Deprecated RevBayes Kernel Information

The current version of `revbayes_kernel` calls the RevBayes executable named `rb-jupyter`. Support to compile `rb-jupyter` with the command `./build.sh -jupyter true` was added to the development branch of the main [RevBayes](https://github.com/revbayes/revbayes) repository in commit [6028eb2](https://github.com/revbayes/revbayes/commit/6028eb2925e2910a839e98060768401843a87362). To find `build.sh`, first change your working directory `cd <revbayes_path>/projects/cmake/`.

The `rb-jupyter` binary must be found using the `which` command or be located using the environment variable, `REVBAYES_JUPYTER_EXECUTABLE`. For instance, you can set the environment variable using
```sh
export REVBAYES_JUPYTER_EXECUTABLE=<revbayes_path>/revbayes/projects/cmake/rb-jupyter
```

### Example notebooks

Run these notebook examples from within the revbayes_kernel folder to correctly access the example data.

Notebook demo for simple MCMC analysis [[preview](https://nbviewer.jupyter.org/github/revbayes/revbayes_kernel/blob/master/revbayes_mcmc_demo.ipynb)]
```sh
jupyter notebook revbayes_mcmc_demo.ipynb
```

Notebook demo for jupyter magics (some RevBayes-python-R interoperability) [[preview](https://nbviewer.jupyter.org/github/revbayes/revbayes_kernel/blob/master/revbayes_magic_demo.ipynb)]
```sh
jupyter notebook revbayes_magic_demo.ipynb
```
