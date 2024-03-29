# Onboarding New IT Members
Author: Carmen Alia Arias -- Class of 2024 (with help of ChatGPT)

## Introduction

Welcome to our project! This document will guide you through setting up your development environment, understanding our codebase, and getting started with Python programming. Whether you're new to Python or just new to our project, this guide will help you get up to speed.

## Table of Contents

1. [Getting Started](#1-getting-started)
   - 1.1. [Prerequisites](#11-prerequisites)
   - 1.2. [Setting Up Git & GitHub](#12-setting-up-git--github)
   - 1.3. [Installing Python & PyCharm](#13-installing-python--pycharm)
   - 1.4. [Cloning the Repositoy](#14-cloning-the-repository)
        * 1.4.1. [Using the Command Line](#141-using-the-commandline)
        * 1.4.2. [Using the PyCharm](#142-using-pycharm)
   - 1.5. [Setting Up a Virtual Environment](#15-setting-up-a-virtual-environment)
        * 1.5.1. [Using the Command Line](#151-using-the-commandline)
        * 1.5.2.[Using PyCharm](#152-using-pycharm)
        
2. [Development Workflow](#2-development-workflow)
   - 2.1. [Branching Strategy](#21-branching-strategy)
   - 2.2. [Creating a Branch and Saving Changes](#22-creating-a-branch-and-saving-changes)
        *2.2.1. [Using the Command Line](#221-using-the-command-line)
        *2.1.2. [Using PyCharm](#222-using-pycharm)
   - 2.3. [Your First Pull Request](#22-your-first-pull-request-pr)
   

3. [Getting Help and Learning Resources](#3-getting-help-and-learning-resources)
   - 3.1. [Git & GitHub Resources](#31-git--github-resources)

---

## 1. Getting Started

### 1.1. Prerequisites

Before you start, ensure you meet the following prerequisites:

- A computer running Windows, macOS, or Linux.
- An internet connection.
- A GitHub account ([GitHub Sign-up](https://github.com/)).
- Have access to the VSVS repository

    If you don't have acces right now, then request to be added to the [VSVS Organization and repo](https://github.com/Vanderbilt-Student-Volunteers-Science)


***Recommendation*** **: If you are creating a new GitHub account use your personal email, because you will probably be using this after you leave Vanderbilt.**

*Optional but recommended:* Sign up for the GitHub student developer pack [here](https://education.github.com/pack). This includes cool perks like free access to GitHub CoPilot!!!

### 1.2. Setting Up Git & GitHub

If you're new to Git and GitHub, follow these steps to set up your Git environment and link it to your GitHub account:

- **Install Git**: Download and install Git from [Git Downloads](https://git-scm.com/downloads). For complete instructions refer to [this](https://github.com/git-guides/install-git).


- **Configure Git**: Open a terminal or command prompt and set your name and email using the following commands:

  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "your.email@example.com"
  ``
  
### 1.3. Installing Python & PyCharm

We use Python for our project. Download and install Python by visiting [Python Downloads](https://www.python.org/downloads/). Ensure you select the option to add Python to your system's PATH during installation.

You are free to use any Python development environment or text editor. However, if you're new to Python we recommend using PyCharm.

You can download PyCharm Community Edition (FREE) from the official website [here](https://www.jetbrains.com/pycharm/download/).

If you are struggling [this](https://www.guru99.com/how-to-install-python.html) guide is worth looking at.

### 1.4. Cloning the Repository

#### 1.4.1. Using the Command Line

1. Before you clone the repository, navigate to the directory where you want to store the local copy of the repository.

    Use `cd` command.For example, if you want to create a new folder named "VSVS_project" on your desktop and navigate into it:

    ```bash
    cd Desktop
    mkdir VSVS_project
    cd VSVS_project
    ```
2. Clone our project repository from GitHub using the following command:

    ```bash
    git clone https://github.com/Vanderbilt-Student-Volunteers-Science/New_VSVS_Scheduler.git
    ```

#### 1.4.2. Using PyCharm

Alternatively, you can use PyCharm's GUI to clone the repository:
1. Open PyCharm.
2. Click on "File" in the top menu.
3. Select "New" and then "Project from Version Control."
4. Choose "Git."
5. In the "URL" field, enter `https://github.com/Vanderbilt-Student-Volunteers-Science/New_VSVS_Scheduler.git`
6. Choose the directory where you want to save the repository in the "Directory" field.
7. Click the "Clone" button.

### 1.5. Setting Up a Virtual Environment

To manage project dependencies and isolate your development environment, create a virtual environment. For further reading/help on the virtual environment this [blogpost](https://frankcorso.dev/setting-up-python-environment-venv-requirements.html) is really helpful!


#### 1.5.1. Using the Command Line

 1. Open a terminal/command prompt in your project directory and run:

    ```bash
    python -m venv .venv
    ```

2. Activate the virtual environment
    - On Windows:

        ```bash
        venv\Scripts\activate
        ```
    - On macOS:

        ```bash
        source venv/bin/activate
        ```
3. Install Dependencies:

    - Install project dependencies from the `requirements.txt` file that can be found under the `docs` folder. 

        ```bash
        pip install -r docs/requirements.txt
        ```
4. Create a .gitignore file. 
    -  This file tells Git what contents from the folder should not be tracked. This is important so you don't push these files to the repository. 

        ```bash
        touch .gitignore
        ```
    
    - Add the following to your .gitignore file (you can simply open it as a text file):

        ```bash
        .venv
        data/
        results/
        ```
    - Remember to save and close the file

    ***IT IS IMPERATIVE THAT YOU INCLUDE THE `/data` & `results/`!!!! OTHERWISE PRIVATE INFORMATION ABOUT VOLUNTEERS WILL BE MADE PUBLICLY AVAILABLE ON THE INTERNET***

#### 1.5.2. Using PyCharm

Installing Dependencies

1. Open PyCharm.
2. Open your project.
3. Go to "File" > "Settings" (Windows/Linux) or "PyCharm" > "Preferences" (macOS).
4. In the settings/preferences window, navigate to "Project" > "Python Interpreter."
5. Click the "Install Requirements" button, represented by a + sign.
6. In the "Install Packages" dialog, locate and select the docs/requirements.txt file from your project directory.
7. Click "Install" to install the project's dependencies.


Adding files to .gitignore 

1. Go "File" > "Settings" (Windows/Linux) or "PyCharm" > "Preferences" (macOS).
2. In the settings/preferences window, navigate to "Version Control" > "Ignored Files."
3. Click the "+ Add" button.
4. In the dialog that appears, enter .venv/ and click "OK."
5. Click "Apply" or "OK" to save your changes.

Do this again for the following files too:
>data/ \
>results/

***IT IS IMPERATIVE THAT YOU INCLUDE THE `/data` & `results/`!!!! OTHERWISE PRIVATE INFORMATION ABOUT VOLUNTEERS WILL BE MADE PUBLICLY AVAILABLE ON THE INTERNET***

## 2. Development Workflow

### 2.1. Branching Strategy 

***The single most important thing to remember: NEVER push your changes directly to the `main` branch***

**Our Philosophy**: The goal is to have an always working version of our code on the `main` branch.  

- You always want to make your own branch that is based on `main` and make your changes there. 
- Once you are satisfied you create a pull request (PR) that merges your branch with the `main` branch. 
- Everyone will have a chance to review your code, make suggestions, and approve the PR.  
- Once approved your changes will officially be part of `main`!

**Naming Convention of Branches**: To keep everyone on the same page, we should all be naming our branches based on the feature/issue that we are working on and with our initials so that people know who's branch it is. (i.e. If John Doe is working on fixing the travel time his branch might be called `Travel_Time_Fix_JD`)  

This is a great overview of our workflow:

### 2.2. Creating a Branch and Saving Changes

#### 2.2.1 Using the Command Line
Open a terminal/command prompt within the project folder/directory.

1. Create a new branch using naming conventions (here we'll just use 'new-feature' for demonstration purposes):

    ```bash
    git checkout -b feature/new-feature
    ```
2. After making changes to your code, use the following command to stage your changes for commit:

    ```bash
    git add .
    ```
    You can also stage individual files by replacing . with the file names.

3. Once your changes are staged, commit them with a meaningful message:

    ```bash
    git commit -m "Describe your changes here"
    ```

4. To push your changes to the remote repository, use the following command (replace 'new-feature' with your branch name):

    ```bash
    git push origin new-feature
    ```

    *Note: You only need to include the word ***origin*** when you are pushing your branch to remote for the first time. After that you can simply type:*

    ```bash
    git push
    ```

#### 2.2.2. Using PyCharm

1. Open PyCharm.
2. Make sure your project is open and active.
3. In the top menu, go to "VCS" > "Git" > "Branches."
4. In the "Branches" dialog, click the "+ New Branch" button.
5. Enter a descriptive name for your new branch (e.g., new-feature). Optionally, you can choose to check out the new branch immediately by selecting the "Check out" option.
6. Click the "Create" button.

After making changes to your code, PyCharm will detect the modifications.
- In the left-hand sidebar, you'll see a list of changed files. Check the box next to each file you want to stage.

- Alternatively, you can right-click on a file and select "Git" > "Add" to stage it.

With your changes staged, go to "VCS" > "Commit" in the top menu.In the Commit dialog, enter a commit message describing your changes.Click the "Commit" button.

After committing your changes, go to "VCS" > "Git" > "Push" in the top menu.In the Push dialog, ensure your branch is selected, and click the "Push" button.


### 2.3. Your First Pull Request (PR)

If you've never created a pull request before or made a branch or anything like that, then I recommend that you go through this [tutorial](https://github.com/skills/introduction-to-github) from GitHub.

1. Make a new branch based off `main` on your local computer. Name it according to convention.
2. Go to the file `docs/authors.txt` and add your name on a new line.
3. Commit the changes.
4. Create a PR.
5. Wait for your PR to be approved by others and then you can complete the PR and merge your changes to `main`.
  
 Congrats! Your officially part of VSVS IT committee. 

## 3. Getting Help and Learning Resources

### 3.1. Git & GitHub Resources

- If you're new to git and/or github please read the following [blogpost](https://www.freecodecamp.org/news/learn-the-basics-of-git-in-under-10-minutes-da548267cc91/) from freecodecamp. 

    By the end you should understand: 
    * What is a repository/repo?  
    * What does it mean to modify, commit, or stage a change?
    * What is a remote repo vs a local repo?

- Follow [this](https://github.com/skills/introduction-to-github) hands-on mini-tutorial for an introduction to github including how to make a repo, commit, and push changes.
