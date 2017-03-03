try:
    from ipykernel.kernelapp import IPKernelApp
except ImportError:
    from IPython.kernel.zmq.kernelapp import IPKernelApp
from .kernel import RevBayesKernel
IPKernelApp.launch_instance(kernel_class=RevBayesKernel)
