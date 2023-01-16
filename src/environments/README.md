# environments
## Description
This page describes how to set up Windows and Mac environments for working with this repo.

In addition, this directory provides various conda environments that can be used cross-platform to work with various libraries and versioning restrictions that may come with them. For this you can refer to the [conda](./conda/README.md) page.

## Getting Started
### MiniForge (conda)
#### Windows
- Install Miniforge from [their GitHub page](https://github.com/conda-forge/miniforge). In our case [Miniforge3-Windows-x86_64](https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe).
  - Be sure to tick the option to add MiniForge to your system PATH.
#### Apple Silicon
- Install Homebrew (https://brew.sh)
- Install XCode
- Install XCode command line tools: `xcode-select --install`
- Install Miniforge via Homebrew: `brew install miniforge`

### Next Steps
- Install [Python 3.X from here](https://www.python.org/downloads/).
- Install [Visual Studio Code from here](https://code.visualstudio.com/download).
- Install Jupiter with the command `conda install -y jupyter` via a fresh terminal session.
- [Start setting up conda environments of your choice](./conda/README.md).
- Start Experimenting
  - With Visual Studio Code, open the root of this repo (folder). Specifically the folder / directory where '.vscode' lives.
    - Install the extensions that VS Code suggests if you like. This should be an automated prompt.
  - [Run this notebook to check library versions post-setup](./scripts/check_version.ipynb).
  - Now you can run any notebooks just like you did the above. Remember to choose your environment that you registered in the setup stage, as your Python interpreter of choice.

## Contribute
In order to contribute, simply fork the repository, make changes and create a pull request.

## Support
If you enjoy FrostAura open-source content and would like to support us in continuous delivery, please consider a donation via a platform of your choice.

| Supported Platforms | Link |
| ------------------- | ---- |
| PayPal | [Donate via Paypal](https://www.paypal.com/donate/?hosted_button_id=SVEXJC9HFBJ72) |

For any queries, contact dean.martin@frostaura.net.