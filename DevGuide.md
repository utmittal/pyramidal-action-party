# Guide for Developers
Hey crew! I've put together a little guide for proposed best development practices, based largely on things I learned in my internship. Have a read and let me know if you disagree with anything.

## Communication
Slack, baby.

## Code style and quality
### Style
We want to be able to show off our code and not look like trash, so try as hard as possible to conform to the [PEP8 style guide](https://www.python.org/dev/peps/pep-0008/). If you develop using PyCharm, style analysis should be enabled automatically, so get rid of those grey squiggly underlines. If you use Spyder, you can enable this (note I haven't seen how well it works):

Tools > Preferences > Editor > Real-time code style analysis

### Comments and var/function names
Please err on the side of comment abundance, especially if you're doing something complicated. PEP8 recommends underscore_variable_names not camelCase, so stick with those; and please no ambiguous junk names.

### Code checking
For mutual learning, error-checking and best practice, all pull requests should be reviewed and merged by somebody else.

## Task management
All tasks are tracked via issues/cards. Navigate to Projects > Kanban. There are 4 sections:
- **Analysis**: The home for all brand new issues, decisions to be made, protyping etc.
- **To Do**: Issues that are well understood. Provide as much detail as possible.
- **In Progress**: Once a task is assigned to you and you've started on it, move the card here.
- **Done**: Only move the card here once you've submitted a pull request and it's been merged.

### Labels
It's helpful to label cards as often as possible. Common and useful labels include:
- **feature**
- **bug**
- **decision**
- **prototype**
- **help wanted**: If you get stuck. Probably we'll discuss problems more in Slack, but can't hurt to add this tag if something's giving you a bad time, in case others are looking about for something to do

## Version control
### Branches
The project is currently split between a Dev branch (localhost-based; we'll be using this for some time) and a Production branch (which we'll fire up once we're ready to start cloud hosting). As y'all probably know, serious projects usually also have a Staging branch that sits between Dev and Production, but I don't think we'll need this.

Do not develop code on Dev or directly push changes here! Whenever you accept a new card, pull the Dev branch to your local machine so you have the latest changes, then create a new branch, which should be named according to the number and title of the card. E.g. for issue #1 "Initial wireframe for page layout and data to display", a good branch name might be "1_initial_wireframe".

### Commits
Pretty please read the [Seven Rules to a great git commit](https://chris.beams.io/posts/git-commit/).
Most importantly: Simple short header line, use imperative tense, more detail in the body if needed.

Happy hunting and thanks for reading!
