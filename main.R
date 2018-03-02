
# Initialization ----
## ---- init

# Load default settings for R Markdown -- see file for more details
source("shared/defaults.R")

options(stringsAsFactors = FALSE)
packages <- c("dplyr","ggplot2","tidyr","pander")
load_or_install.packages(packages)

data_dir <- "data/"
output_dir <- "output/"

# Load some helper functions
source("shared/helper.R")

## ---- end-of-init