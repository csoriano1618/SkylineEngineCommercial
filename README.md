Copyright 2014 Carlos Soriano Sánchez <carlos.soriano89@gmail.com>

Commercial City Simulation
==================================================

Contribution Guides
--------------------------------------
1. See code already done for style guidelines.
2. Ask for a review of your code before commiting.
3. Ensure all works with the new changes before asking review.


Environments in which to use Commercial City Simulation
--------------------------------------
Research environments.

What you need to build Commercial City Simulation
--------------------------------------

In order to build Commercial City Simulation you need
- python 2.7
- SkylineEngine
- numpy


How to build Commercial City Simulation
----------------------------
Just execute the main.py file.


Running the Unit Tests
--------------------------------------

TODO


Essential Git
-------------

As the source code is handled by the version control system Git, it's useful to know some features used.

### cleaning ###

If you want to purge your working directory back to the status of upstream, following commands can be used (remember everything you've worked on is gone after these):

```bash
git reset --hard upstream/master
git clean -fdx
```

### rebasing ###

For rebasing to your local branch use:
```bash
git pull --rebase
```


### handling merge conflicts ###

If you're getting merge conflicts when merging, instead of editing the conflicted files manually, you can use the feature
`git mergetool`. You can use a tool like meld to help you with conflicts.

