# Onboarding New Members

### Objectives:


- Install Python & PyCharm
- Set up Git/GitHub
- Setup your environment
- Clone the VSVS repository


## Install Python/PyCharm


The following [guide](https://www.guru99.com/how-to-install-python.html)

Otherwise, just google "python" and install the latest version for your computer. Do the same thing for Pycharm and get the community edition (the free plan).


## Getting Started with Git/GitHub


1. If you're new to git and/or github please read the following [blogpost](https://www.freecodecamp.org/news/learn-the-basics-of-git-in-under-10-minutes-da548267cc91/) from freecodecamp. 

    By the end you should understand: 
    - What is a repository/repo?  
    - What does it mean to modify, commit, or stage a change?
    - What is a remote repo vs a local repo?

2. Install Git. For complete instructions refer to [this](https://github.com/git-guides/install-git).

3. Create a Github account [here](https://github.com/) if you don't have one.  ***Recommendation*** **: use your personal email when you create it, because you will probably be using this after you leave Vanderbilt.**

4. Follow [this](https://github.com/skills/introduction-to-github) hands-on mini-tutorial for an introduction to github about how to make a repo, commit, and push changes.

5. Request to be added to the [VSVS Organization and repo](https://github.com/Vanderbilt-Student-Volunteers-Science
).

6. *Optional but recommended:* Sign up for the GitHub student developer pack [here](https://education.github.com/pack). This includes cool perks like free access to GitHub CoPilot!!!


## Setting Up Your Environment


1. **Clone the VSVS repo**: Open a window for your terminal on your computer and navigate to the folder that you would like to save the VSVS codebase on. The image below demonstrates how to clone the repo into a folder callde VSVS, using the command line.

2. **Verify it worked**: To verify that this worked, you can navigate into the folder and see that the repo was stored inside as shown in the image below.

3. **Create a virtual environment for the project**: This will have the necessary requirements for the code to be able to run/work. Make sure that you are still in the correct folder in the terminal. Create a virtual environment by typing the following into your terminal: `python -m venv .myvenv`. This will install your virtual environment into a folder called `.myvenv`.

4. **Activate the virtual environment**: This can be done by navigating into the repo folder on your machine. On Windows, on the terminal you type the following command: `.myvenv\Scripts\activate`.
For further reading/help on the virtual environment this [blogpost](https://frankcorso.dev/setting-up-python-environment-venv-requirements.html
) is really helpful!

5. **Install the requirements**: On the terminal, navigate to the folder that contains the requirements.txt file. Then type the following command: `pip install -r requirements.txt`

6. **Create a .gitignore file**: Your computer might already automatically create a .gitignore file for you. Otherwise create a file in the VSVS repo on your computer and call it: *.gitignore*. The contents of your .gitignore file should be the following (you might also have other filenames that were automatically added by your computer):
>.venv/  
>data/VSVS.db  
>results/

***IT IS IMPERATIVE THAT YOU INCLUDE THE `/data/VSVS.db` & `results/`!!!! OTHERWISE PRIVATE INFORMATION ABOUT VOLUNTEERS WILL BE MADE PUBLICLY AVAILABLE ON THE INTERNET***


## Making Contributions


***The single most important thing to remember: NEVER push your changes directly to the `main` branch***

**Our Philosophy**: The goal is to have an always working version of our code on the `main` branch.  

You always want to make your own branch that is based on `main` and make your changes there. Once you are satisfied you create a pull request (PR) that merges your branch with the `main` branch. Everyone will have a chance to review your code, make suggestions, and approve the PR.  Once approved your changes will officially be part of `main`!

**Naming Convention of Branches**: To keep everyone on the same page, we should all be naming our branches based on the feature/issue that we are working on and with our initials so that people know who's branch it is. (i.e. If John Doe is working on fixing the travel time his branch might be called `Travel_Time_Fix_JD`)  

This is a great overview of our workflow:


### Your First PR
If you've never created a pull request before or made a branch or anything like that, then I recommend that you go through this [tutorial](https://github.com/skills/introduction-to-github) from GitHub.

1. Make a new branch based off `main` on your local computer. Name it according to convention.
2. Go to the file `docs/authors.txt` and add your name on a new line.
3. Commit the changes.
4. Create a PR.
5. Wait for your PR to be approved by others and then you can complete the PR and merge your changes to `main`.
  
 Congrats! Your officially part of VSVS IT committee. 



