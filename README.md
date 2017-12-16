Script to fetch author information from PubMed
 - There is a lot of space for improvement

Useful to triage a somewhat large number of authors, intended to save time when looking into university departments

Usage:

python fetch_pubmed.py --author-name "$(cat INPUTS/list_of_UMiamiOH_DepBio.txt)" --additional-fields "AD:Brazil;AD:Miami" > OUTPUTS/list_of_UMiamiOH_DepBio.txt.output

Requirements:
 - BioPython
 - argparse
 - RAKE
