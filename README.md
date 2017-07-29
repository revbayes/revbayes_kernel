# revbayes_kernel
A Jupyter kernel for RevBayes

### Installing revbayes_kernel

```sh
sudo python3 setup.py install
python3 -m revbayes_kernel.install
```

The current version of `revbayes_kernel` calls the RevBayes executable named `rb-jupyter`. Support to compile `rb-jupyter` with the command `./projects/cmake/build.sh -jupyter true` was added to the development branch of the main [RevBayes](https://github.com/revbayes/revbayes) repository in commit [6028eb2](https://github.com/revbayes/revbayes/commit/6028eb2925e2910a839e98060768401843a87362).

The `rb-jupyter` binary must be found using the `which` command or be located using the environment variable, `REVBAYES_JUPYTER_EXECUTABLE`.

### Example notebooks

Notebook demo for simple MCMC analysis [[preview](https://nbviewer.jupyter.org/github/revbayes/revbayes_kernel/blob/master/revbayes_mcmc_demo.ipynb)]
```sh
jupyter notebook revbayes_mcmc_demo.ipynb
```

Notebook demo for jupyter magics (some RevBayes-python-R interoperability) [[preview](https://nbviewer.jupyter.org/github/revbayes/revbayes_kernel/blob/master/revbayes_magic_demo.ipynb)]
```sh
jupyter notebook revbayes_magic_demo.ipynb
```
