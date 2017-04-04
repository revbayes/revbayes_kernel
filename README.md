# revbayes_kernel
A Jupyter kernel for RevBayes

Installing revbayes_kernel

```sh
sudo python3 setup.py install
python3 -m revbayes_kernel.install
```

The kernel creates a REPLWrapper for the binary `rb-jupyter`, which is compiled by running `./projects/cmake/build.sh -jupyter true` in (added to development in commit [6028eb2](https://github.com/revbayes/revbayes/commit/6028eb2925e2910a839e98060768401843a87362)).

Notebook demo for simple MCMC analysis
```sh
jupyter notebook revbayes_mcmc_demo.ipynb
```

Notebook demo for jupyter magics (some RevBayes-python interoperability)
```sh
jupyter notebook revbayes_magic_demo.ipynb
```
