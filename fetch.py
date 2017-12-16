import scholarly
import argparse


def read_args():
    '''
    read arguments for script
    '''

    global author_name
    parser = argparse.ArgumentParser(description='task automation ' +
                                     'with BAM')
    parser.add_argument('--author-name',
                        help='author name to be searched',
                        required=True)
    args = parser.parse_args()
    author_name = args.author_name
    return

def dummy_function(params):
    '''
    Find all files with an extension within a project
    @args api: api instance with user logged in
    @args project: project instance
    @args extension: extension for finding files
    @return my_files: all files with a particular extension
    '''

    return params


def main(author_name):
    # Initialize api instance
    print author_name
    search_query = scholarly.search_author(author_name)
    author = next(search_query)
    print author
    author_fill = author.fill()
    pub = [pub.bib['title'] for pub in author_fill.publications]
    print pub

    return

if __name__ == "__main__":
    read_args()
    main(author_name)

