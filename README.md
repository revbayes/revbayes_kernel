# revbayes_kernel
A Jupyter kernel for RevBayes

Install

```sh
sudo python3 setup.py install
python3 -m revbayes_kernel.install
```

The kernel creates a REPLWrapper for the binary `rb-jupyter`, which is compiled by running `./projects/cmake/build.sh -jupyter true` in (added to development in commit [6028eb2](https://github.com/revbayes/revbayes/commit/6028eb2925e2910a839e98060768401843a87362)).

To see a demo notebook
```sh
jupyter notebook revbayes_notebook.ipynb
```
