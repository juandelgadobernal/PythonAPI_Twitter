import requests     # lib request end point
import argparse     # lib command line

# To heapify subtree rooted at index i.
# n is size of heap

def heapify(arr, n, i):
    """
    To heapify subtree rooted at index i.

    Parameters:
    arr (arr):
    n (): n is the size of the heap
    i():  i si the index in teh array

    Returns:

    """

    smallest = i  # Initialize largest as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2

    # See if left child of root exists and is
    # greater than root
    if l < n and arr[l][1] < arr[smallest][1]:
        smallest = l

        # See if right child of root exists and is
    # greater than root
    if r < n and arr[r][1] < arr[smallest][1]:
        smallest = r

        # Change root, if needed
    if smallest != i:
        arr[i], arr[smallest] = arr[smallest], arr[i]  # swap

        # Heapify the root.
        heapify(arr, n, smallest)

    # The main function to sort an array of given size

def heapSort(arr):
    """
    Main function to do heap sort

    Parameters:
    arr (arr):

    Returns:

    """

    n = len(arr)

    # Build a maxheap.
    # Since last parent will be at ((n//2)-1) we can start at that location.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # One by one extract elements
    for i in range(n - 1, -1, -1):
        arr[0], arr[i] = arr[i], arr[0]  # swap
        heapify(arr, i, 0)

    # Driver code to test above

def make_url_repos(organization):
    """
    Returns all the repositories for an organization.

    Parameters:
    organization (str): Receive the Organization from command line

    Returns:
    repos (json): Json with all the repositories of the organization
    """

    repos_txt = 'repos'
    url_repos = 'https://api.github.com/orgs/{}/{}'.format(organization,repos_txt)
    r = requests.get(url_repos)
    repos = r.json()

    return repos

def make_url_pulls(organization, repo_name):
    """
    Returns the pull request for all the repositories of an organization.

    Parameters:
    organization (str): Receive the Organization from command line
    repo_name (str): Receive the name of the repository

    Returns:
    repos_pull_request (json): Json with the pull request for all the repositories of an organization.

    """

    pulls_txt = 'pulls'
    url_prs = 'https://api.github.com/repos/{}/{}/{}'.format(organization,repo_name,pulls_txt)
    r2 = requests.get(url_prs)
    repos_pull_request = r2.json()

    return repos_pull_request

def top_ranking_repos(organization, top_n):
    """
    Print the results of the top ranking (highest) for the stars and forks in the repos for an organization.

    Parameters:
    organization (str): Receive the Organization from command line
    top_n (int): Receive value of the the top N

    Returns:
    list_sort_stars (list): Top-N repos by number of stars.
    list_sort_forks (list): Top-N repos by number of forks.

    """

    repos = make_url_repos(organization)

    #lists
    list_sort_stars =[]
    list_sort_forks = []

    for repo in repos:
        stars_count = repo['name'], repo['stargazers_count']
        forks_count = repo['name'], repo['forks_count']
        list_sort_stars.append(stars_count)
        list_sort_forks.append(forks_count)

    heapSort(list_sort_stars)
    print('Top-N repos by number of stars {}'.format(list_sort_stars[:top_n]))

    heapSort(list_sort_forks)
    print('Top-N repos by number of forks {}'.format(list_sort_forks[:top_n]))

def pull_request_count(organization,repo_name):
    """
    Return the total of pull requests counted in the repos for an organization.

    Parameters:
    organization (str): Receive the Organization from command line
    repo_name (str): Receive the name of the repository

    Returns:
    prs_count (int): The total of PRs for a repo

    """

    repos_pull_request = make_url_pulls(organization,repo_name)

    #print(len(repos_pull_request))
    prs_count= len(repos_pull_request)

    return prs_count

def top_ranking_prs_cp(organization, top_n):
    """
    Print the results of the top ranking (highest) by number of Pull Requests and contribution percentage at organization.

    Parameters:
    organization (str): Receive the Organization from command line
    top_n (int): Receive value of the the top N

    Returns:
    list_pull_requests (list): Top-N repos by number of Pull Requests (PRs).
    list_contribution_percentage (list): Top-N repos by contribution percentage (PRs/forks).

    """

    repos = make_url_repos(organization)

    #list
    list_pull_requests =[]
    list_contribution_percentage = []

    for repo in repos:
        repo_name = repo['name']
        prs_count = pull_request_count(organization, repo_name)
        pull_request_total_count = repo['name'], prs_count
        list_pull_requests.append(pull_request_total_count)
        try:
            #contributionPer = (repo['forks_count']/prs_count)
            contribution_percentage = repo['name'],(repo['forks_count']/prs_count)
            list_contribution_percentage.append(contribution_percentage)
        except ZeroDivisionError:
            pass

        #print('repo name {}, stars {}, forks {}, PRS {}, CP % {}'.format(repo['name'], repo['stargazers_count'], repo['forks_count'],prs_count, contributionPer ))

    heapSort(list_pull_requests)
    print('Top-N repos by number of Pull Requests (PRs) {}'.format(list_pull_requests[:top_n]))

    heapSort(list_contribution_percentage)
    print('Top-N repos by contribution percentage (PRs/forks) {}'.format(list_contribution_percentage[:top_n]))

def get_arguments():
    """
    Parse the commandline arguments from the user

    Parameters:
    organization (str): Receive the Organization from command line
    top_n (int): Receive value of the the top N from command line

    Returns:
    Top-N repos by number of stars.
    Top-N repos by number of forks.
    Top-N repos by number of Pull Requests (PRs).
    Top-N repos by contribution percentage (PRs/forks).

    """
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-o', '--organization', help = 'the organization', required=True)
    parser.add_argument('-n', '--top_number', type=int, help = 'the top N number', required=True)
    return parser.parse_args()

top_ranking_repos('twitter',5)
top_ranking_prs_cp('twitter',5)
"""
call setup for neoworks
usage:
python script_name.py -s <organization> -n <top number>
eg:
python twitter.py -o twitter -n 5

""

if __name__ == "__main__":
    args = get_arguments()

    orga=args.organization
    topNumber=args.top_number

    try:
        top_ranking_repos(orga,topNumber)
    except Exception as ex:
        print(ex)
    finally:
        print("------------- END-------------------------------------------")
"""