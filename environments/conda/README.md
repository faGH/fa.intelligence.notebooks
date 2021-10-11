# conda
## Description
This page describes how to set up any conda environment within this directory.

## Getting Started
- Open a terminal in the root of this directory (or any directory containing conda-compatible yml files).
- Deactivate the current envirnonment: `conda deactivate`
- Create environment from YML file of your choice: `conda env create -f tensorflow-apple-silicon.yml`
- Activate the environment: `conda activate tensorflow-apple-silicon`
- Add Jupyter support to environment: `conda install nb_conda`
- Register the environment with Jupyter with a name of your choice: `python -m ipykernel install --user --name tensorflow-apple-silicon --display-name "Python 3.9 (TF - Apple Metal)"`
  - In order to remove kernels, list them: `jupyter kernelspec list` to find the kernel you would like to remove.
  - Remove the kernel: `jupyter kernelspec uninstall <unwanted-kernel>`
- Fire up Jupyter Notebook to test: `jupyter notebook` or simply use VS Code's built-in capability to execute Jupyter files by opening one up and choosing the Environment we just created as the kernal of choice.

## Contribute
In order to contribute, simply fork the repository, make changes and create a pull request.

## Support
If you enjoy FrostAura open-source content and would like to support us in continuous delivery, please consider a donation via a platform of your choice.

| Supported Platforms | Link |
| ------------------- | ---- |
| PayPal | [Donate via Paypal](https://www.paypal.com/donate/?hosted_button_id=SVEXJC9HFBJ72) |

For any queries, contact dean.martin@frostaura.net.