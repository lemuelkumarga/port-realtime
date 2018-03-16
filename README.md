## Package Requirements

### Mac/Ubuntu Operating System
- Other OS-es have not been tested, and may cause unexpected errors.

### Pandoc 2.1 
- Need to reference googlefonts

## Creating A New Repository from the Template

To create a new project by using this template as skeleton, we need to manually "fork" this template. Extra precaution is also required as the R-template contains links to other repos (submodules).

Please replicate the steps below in Terminal to ensure success.

``` sh
# First: Create an empty repository in github via https://github.com/new

# Clone the newly created empty repo
git clone https://github.com/<username>/<new_repo_project_name>

# Define this clone as a fork of R-template
cd <new_repo_project_name> 
git remote add upstream https://github.com/lemuelkumarga/R-template.git

# Pull all the files from the template
git pull upstream master

# Remove the "Create New Repo from Template section"
sed -i 's/, prepend_mds=c("shared\/md\/requirements.md","shared\/md\/creating.md","shared\/md\/cloning.md")//g' main.Rmd

# Initialize submodules
git submodule init
git submodule update

# When cloned, submodules are detached from the HEAD. We attempt to rectify this issue to prevent problems in git
cd shared
git checkout -b tmp
git checkout master
git merge tmp
git branch -d tmp
cd ..

# Push your changes to the cloud
git push -u origin master

# Return to original folder if desired
cd ..
```

## Cloning the Repository

Cloning the repository is not as straightforward due to the presence of git submodules.

Please replicate the steps below in Terminal to ensure success.

``` sh
# Clone the repo as usual
git clone https://github.com/lemuelkumarga/R-template

# Initialize submodule
cd R-template
git submodule init
git submodule update

# When cloned, submodules are detached from the HEAD. We attempt to rectify this issue to prevent problems in git
cd shared
git checkout -b tmp
git checkout master
git merge tmp
git branch -d tmp

# Return to original folder if desired
cd ../../
```

---
Insert Title Here
================
Lemuel Kumarga

## Problem Description

Insert Problem Description Here.

## Preliminaries

First load the necessary packages for this exercise.

``` r
# Load default settings for R Markdown -- see file for more details
source("shared/defaults.R")

options(stringsAsFactors = FALSE)
packages <- c("dplyr","ggplot2","tidyr","pander")
load_or_install.packages(packages)

data_dir <- "data/"
output_dir <- "output/"

# Load some helper functions
source("shared/helper.R")

si <- sessionInfo()
base_pkg_str <- paste0("Base Packages: ",paste(si[["basePkgs"]], collapse=", "))
attached_pkg_str <- paste0("Attached Packages: ",paste(names(si[["otherPkgs"]]), collapse=", "))
cat(paste0(base_pkg_str,"\n",attached_pkg_str))
```

    ## Base Packages: stats, graphics, grDevices, utils, datasets, base
    ## Attached Packages: tidyr, pander, ggplot2, dplyr, knitr
