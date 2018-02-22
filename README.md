Preliminaries
-------------

First load the necessary packages for this exercise.

    # Load default settings for R Markdown -- see file for more details
    source("shared/defaults.R")

    options(stringsAsFactors = FALSE)
    packages <- c("dplyr","ggplot2","tidyr")
    load_or_install.packages(packages)

    data_dir <- "data/"

    si <- sessionInfo()
    base_pkg_str <- paste0("Base Packages: ",paste(si[["basePkgs"]], collapse=", "))
    attached_pkg_str <- paste0("Attached Packages: ",paste(names(si[["otherPkgs"]]), collapse=", "))
    cat(paste0(base_pkg_str,"\n",attached_pkg_str))

    ## Base Packages: stats, graphics, grDevices, utils, datasets, methods, base
    ## Attached Packages: tidyr, ggplot2, dplyr, knitr
