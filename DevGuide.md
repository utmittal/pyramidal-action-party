# Guide for Developers
Hey crew! I've put together a little guide for proposed best development
practices, based largely on things I learned in my internship. Have a read and
let me know if you disagree with anything.


## Communication
Slack, baby.


## Dev environment
A great way to manage your pip packages is with `pyenv` and `pip-tools`  

### Pyenv
`Pyenv` allows you to maintain multiple python installations on your machine at 
once (including virtual installations), automatically switch between them for
different projects, and have the right packages/versions installed for each.

This step is optional though recommended.

    # Install pyenv
    $ pip install pyenv

    # Create a virtual environment which will manage pip packages for this
    project
    $ pyenv virtualenv 3.6.3 pyramidal      #or whatever you want to call it

    # Set pyenv to use this virtual env for the project
    $ cd pyramidal-action-party/
    $ pyenv local pyramidal

Now all packages and commands executed relevant to the project will be locked 
to a virtual instance of Python version 3.6.3, and all packages installed for
it.

### Pip-tools
`pip-tools` is a super handy way to automate packages management for a project
and quickly install everything you need to get up and going.

    $ pip install pip-tools
    
`pip-tools` will look for the file 'requirements.in', where all necessary
packages for the current project should be listed. `pip-tools` can use this to
derive a list of all dependency packages, and save it as requirements.txt

    $ pip-compile [-U]

Including the -U flag will update to the latest version of all packages.
This may be good, but may also break everything. Now install dependencies:

    $ pip install -r requirements.txt
    
    # To uninstall extraneous pip packages which may be polluting your virtual
    python env:
    pip-sync

You should now be good to run all code for the project.


## Running the app
To launch the local server, once your dev environment is set up, simply 
execute `python app.py` from the root directory, then navigate to
http://127.0.0.1:8050 to view the page.


## Code style and quality

### Style
We want to be able to show off our code and not look like trash, so try as hard
as possible to conform to the 
[PEP8 style guide](https://www.python.org/dev/peps/pep-0008/). If you develop
using PyCharm, style analysis should be enabled automatically, so make sure
there are no grey squiggly underlines. If you use Spyder, you can enable this:

`Tools > Preferences > Editor > Real-time code style analysis`

`assert` statements are always smiled upon to increase code robustness, as are 
test (see section below).

### Comments and var/function names
Please err on the side of too many than insufficient comments, especially if 
you're doing something complicated. PEP8 recommends snake_case not camelCase.

### Code checking
For mutual learning, error-checking and safety, it's best not to merge your own
pull requests (in the worst case you'll temporarily break the Dev branch for
everyone). Instead, all pull requests should be reviewed and merged into Dev by
somebody else, with feedback given if they find any issues.


## Task management
All tasks are tracked via issues/cards. Navigate to `Projects > Kanban`. There
are 6 sections which cards progress through:
- **Analysis**: The home for all brand new issues, decisions to be made, 
protyping etc.
- **To Do**: Issues that are well understood. Provide as much detail as 
possible.
- **Doing**: Once a task is assigned to you and you've started on it, move the 
card here.
- **Testing**: Upon testing further changes may be needed (use same branch)
- **Deployment**: At the moment, we can probably skip this. It will ultimately 
mean merging to production
- **Done**: Only move the card here once you've submitted a pull request and 
it's been merged.

### Labels
It's helpful to label cards wherever possible. The first 5 are mostly mutually
exclusive:
- **feature**
- **bug**
- **decision**
- **prototype**
- **documentation**: there shouldn't be tooo much of this because we're AGILE! 
(maybe?!)
- **help wanted**: If you get stuck, signal for backup. Probably we'll discuss 
problems more in Slack, but can't hurt to add this tag


## Version control
### Git
Time to get real comfortable with git! If you mess something out, never fear, 
it's (almost) always reversible, and surely at least one of us can figure it 
out. Commands like `revert`, `fetch` and `stash` are worth getting familiar 
with :-)

### Branches
The project is currently split between a dev branch (localhost-based; we'll be 
using this for some time) and a production branch (which we'll fire up once 
we're ready to start cloud hosting). As y'all probably know, serious projects
usually also have a staging branch that sits between dev and production, but I
don't think we'll need this. Note also that master is not being used.

To pull remote branches to your local machine:  

`git fetch` &nbsp;&nbsp;&nbsp;&nbsp; # Update the local list of remote branches 
(no output given)  
`git branch -r` &nbsp;&nbsp;&nbsp; # List all remote branches  
`git checkout <remote branch name>`

Do not develop code on dev or directly push changes there! Whenever you accept
a new card, re-pull the dev branch to your local machine so you have the latest
changes, check it out then create a new local branch, which should be named 
according to the number and title of the card. E.g. for issue #2 "Integrate 
basic Twitter search API calling", I did:

```
git checkout dev
git pull
  
# Create and checkout a new branch
git checkout -b 2_twitter_search_initial  
```
You now have a safe local branch to develop your code. 

### Commits
Pretty please read the 
[Seven Rules to a great git commit](https://chris.beams.io/posts/git-commit/).  
Most importantly:
- Concise one-line description of *added functionality*
- Use imperative tense
- Add more detail in the body if needed

### Testing
Testing is the bomb. I don't see us being motivated enough to do it much. If 
you can be arsed writing a test or two that's GREAT (ideally before beginning 
your coding).  

There's a list on the Kanban board for testing after the "Doing" stage, so you 
can move your card here once you've got a basic implementation seeming to work. 
It's reasonable to commit after the Donig stage and again after testing (if 
there are any changes or additional tests).

### Merging Code
Once you've finished with the card and testing, time to push it to the remote 
repo and create a pull request.  

```
git add .
git commit
# Write a great commit using rules above
git push --set-upstream origin <local branch name>
git checkout dev
```
Don't forget to switch back to dev, or your next branch will be based off the 
branch your just pushed, which still needs to be reviewed.

You can now navigate your browser to the repo, and in the "Your recently pushed
branches:" section at the top you should see your branch. Click "Compare and 
pull request".  

**Make sure to change the 'base' branch to 'dev'!**  
The compare branch should be the one you just pushed.

If your git commit was decent you shouldn't have to change the title or
comment (though you're welcome to).  

It's best practice to have someone else review and merge your code. In the 
panel on the right there are options to add **Reviewers** and **Assignees**.
It's a 
[little unclear](https://github.com/blog/2291-introducing-review-requests) what 
the difference is between the two, so I'd suggest just add at least one person 
as an Assignee. (Reviewers are a recent addition to the GitHub platform)

It's nice if you also select a label indicating what the pull request is, 
though not essential.

Finally, return to the Kanban board and move your card into the "Deployment" 
list. It should sit here until eventually merged onto the production branch. 

### Reviewing Pull Requests
On the GitHub repo, click 'Pull requests' to see pending requests and the 
assignee. It probably mostly won't matter who reviews any particular pull
request (as long as it's not the same person who made it), so please review and 
merge  whenever you see requests waiting around.  

Click a request. Check at the top next to the green "Open" logo and make sure 
they're merging into dev (or production, as appropriate).  

Click the "Files changed" tab and scroll down to see all the added and deleted 
lines in the commit. If there are any obvious problems click "Review changes" 
and leave a comment. You can also move the card back into "Doing" or "Testing" 
on the Kanban board.  

Realistically though there's no great way to tell if the changes will 
break everything, so usually just navigate back to the "Conversation" tab and 
scroll down to click "Merge pull request".

Hopefully the person who made the commit will have been fairly diligent, and 
will have vaguely tested that their code isn't too deadly.


## Databases
If/when we come to integrating a database, best practice/necessity is to use [schema migrations](https://en.wikipedia.org/wiki/Schema_migration). Make sure you grok that when the time comes that you need to.


### Happy hunting and thanks for reading!
