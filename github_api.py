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

def request_url(url_repos_prs):

    r = requests.get(url_repos_prs)
    request_repos_prs = r.json()
    return request_repos_prs

def print_top_ranking_repos(top_n, repos):
    """
    Print the results of the top ranking (highest) for the stars and forks in the repos for an organization.

    Parameters:
    organization (str): Receive the Organization from command line
    top_n (int): Receive value of the the top N

    Returns:
    list_sort_stars (list): Top-N repos by number of stars.
    list_sort_forks (list): Top-N repos by number of forks.

    """

    #lists
    list_sort_stars =[]
    list_sort_forks = []

    for repo in repos:
        stars_count = repo['name'], repo['stargazers_count']
        forks_count = repo['name'], repo['forks_count']
        list_sort_stars.append(stars_count)
        list_sort_forks.append(forks_count)
    #print(list_sort_stars)

    heapSort(list_sort_stars)
    print('Top-N repos by number of stars {}'.format(list_sort_stars[:top_n]))

    heapSort(list_sort_forks)
    print('Top-N repos by number of forks {}'.format(list_sort_forks[:top_n]))

def print_top_ranking_prs_cp(organization, top_n, repos):
    """
    Print the results of the top ranking (highest) by number of Pull Requests and contribution percentage at organization.

    Parameters:
    organization (str): Receive the Organization from command line
    top_n (int): Receive value of the the top N

    Returns:
    list_pull_requests (list): Top-N repos by number of Pull Requests (PRs).
    list_contribution_percentage (list): Top-N repos by contribution percentage (PRs/forks).

    """

    #list
    list_pull_requests =[]
    list_contribution_percentage = []

    for repo in repos:
        repo_name = repo['name']

        url_prs = 'https://api.github.com/repos/{}/{}/pulls'.format(organization, repo_name)
        prs_count = len(request_url(url_prs))

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


"""
call setup
usage: python script_name.py -o <organization> -n <top number>
eg: python3 github_api.py -o twitter -n 5
"""

if __name__ == "__main__":
    args = get_arguments()
    organization=args.organization
    top_number=args.top_number

    if top_number <= 0 :
        print('Top N must be greater than 0')

        import sys
        sys.exit("Error message")

    # repos
    url_repos = 'https://api.github.com/orgs/{}/repos'.format(organization)
    repos_list = request_url(url_repos)

    print_top_ranking_repos(top_number, repos_list)
    print_top_ranking_prs_cp(organization, top_number, repos_list)

