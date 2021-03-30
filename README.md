# Python API Twitter

Using any JVM language or Python, build a command line tool that analyzes the popularity of an organization’s GitHub repos.  The tool should report statistics for the following four dimensions:
* Top-N repos by number of stars.
* Top-N repos by number of forks.
* Top-N repos by number of Pull Requests (PRs).
* Top-N repos by contribution percentage (PRs/forks).

The tool should accept at least two arguments: GitHub organization and N.
For example : organization=Twitter and N=10

The following links could be helpful:
Github API: http://developer.github.com/v3/
List an organization’s repos: http://developer.github.com/v3/repos/#list-organization-repositories
List pull requests: http://developer.github.com/v3/pulls/Rate limits on API: https://developer.github.com/v3/#rate-limiting

# How to run

 usage: python script_name.py -o <organization> -n <top number>
 
 eg: python3 github_api.py -o twitter -n 5
 
 # Libs
 
requests   
argparse     
