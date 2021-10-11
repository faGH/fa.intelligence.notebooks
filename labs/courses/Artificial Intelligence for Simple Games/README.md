# Artificial Intelligence for Simple Games
## Setup
### Macbook M1 (Apple Metal)
#### Installation
- Install Homebrew (https://brew.sh)
- Install XCode
- Install XCode command line tools: `xcode-select --install`
- Install Miniforge via Homebrew: `brew install miniforge`
- Install Jupiter: `conda install -y jupyter`
#### Setup Environment
- Deactivate the current envirnonment: `conda deactivate`
- Create environment from YML file: `conda env create -f tensorflow-apple-metal.yml`
- Activate the environment: `conda activate tensorflow-apple-metal`
- Add Jupyter support to environment: `conda install nb_conda`
- Register the environment with Jupyter: `python -m ipykernel install --user --name tensorflow-apple-metal --display-name "Python 3.9 (TF - Apple Metal)"`
- Fire up Jupyter Notebook to test: `jupyter notebook` or simply use VS Code's built-in capability to execute Jupyter files by opening one up and choosing the Environment we just created as the kernal of choice.

### Course Dependencies
- Install Anaconda for your operating system.
- Create a new environment by running `conda create -n aigames python=3.6`