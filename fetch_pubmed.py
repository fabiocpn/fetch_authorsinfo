import argparse
from Bio import Entrez
from Bio import Medline
import RAKE

MAX_COUNT = 500

def read_args():
    '''
    read arguments for script
    '''

    global author_name,additional_fields
    parser = argparse.ArgumentParser(description='task automation ' +
                                     'with BAM')
    parser.add_argument('--author-name',
                        help='author name to be searched',
                        required=True)
    parser.add_argument('--additional-fields',
            help='extra pubmed fields and serches. FORMAT=FIELD:STRING',
                        required=False)
    args = parser.parse_args()
    author_name = args.author_name
    additional_fields = args.additional_fields
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


def main(author_name,additional_fields):
    # Initialize api instance
    authors = author_name.split(";")
    if ( additional_fields ):
        search_tuples = additional_fields.split(";")
    else:
        search_tuples = []

    for name in authors:
        TERM = name+"[AU]"
    
        #print('Getting {0} publications containing {1}...'.format(MAX_COUNT, TERM))
        Entrez.email = 'fabiocpn@gmail.com'
        h = Entrez.esearch(db='pubmed', retmax=MAX_COUNT, term=TERM)
        result = Entrez.read(h)

        n_publications = result['Count']
        ids = result['IdList']
        h = Entrez.efetch(db='pubmed', id=ids, rettype='medline', retmode='text')
        records = Medline.parse(h)
    
        abstracts = []
        NSC = 0
        additional_fields_count = [0] * len(search_tuples)
        for record in records:
            abstract = record.get('AB', '?')
            abstracts.append(abstract)
            journal = record.get('TA','?')
            if ( journal == "Nature" or journal == "Science" or journal == "Cell" ):
                NSC = NSC + 1
 
            field_index=0
            for search_tuple in search_tuples: 
                search_tokens = search_tuple.split(":")
                field_value = record.get(search_tokens[0],'?')
#                print "==>"+ search_tokens[1] + " " + field_value
                if ( field_value.find(search_tokens[1]) != -1):
                   additional_fields_count[field_index]=additional_fields_count[field_index] + 1
                field_index = field_index + 1

        #r = Rake("SmartStoplist.txt", 3, 3, 2) 
        Rake = RAKE.Rake(RAKE.SmartStopList())
            #r = Rake(<language>)
        #keywords = Rake.run(". ".join(titles),minCharacters = 1, maxWords = 3, minFrequency = 3) 
        keywords = Rake.run(". ".join(abstracts),minCharacters = 1, maxWords = 2, minFrequency = 3) 
        keywords_list = []
        count_keywords = 0
        for key in keywords:
            keywords_list.append(key[0])
            count_keywords = count_keywords + 1
            if ( count_keywords >= 12 ):
                break
    
        print name+"\t"+n_publications+"\t"+str(NSC)+"\t"+"\t".join(str(x) for x in additional_fields_count)+"\t\""+", ".join(keywords_list)+"\""
    
    return

if __name__ == "__main__":
    read_args()
    main(author_name,additional_fields)

