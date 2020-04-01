import git
#git.Git("./public_data").clone("https://github.com/CSSEGISandData/COVID-19.git")
g = git.cmd.Git("./public_data/COVID-19")
g.pull()


