# Automated Testing

## Introduction

For Python projects, you can write automated tests to evaluate your code. For this project, it is a little more
complicated because the program relies on specific input files. I will be using the `pytest` library to write these
test cases. Hopefully, in the future, we can integrate a CI/CD tool (GitHub Actions) to automatically run these test cases for each
commit or pull request.
   
## Getting Started

Since this will require the use of the `pytest` library, it is a good idea to create a virtual environment for this
project. We can do this with the following code in the command line or via the settings in your IDE:

For Windows:

```cmd
py -m venv env
.\env\Scripts\activate
pip install pytest
```

For Mac/*nix:

```shell
python3 -m venv env
source env/bin/activate
pip3 install pytest
```

## Test Cases

- convert time string to military time
