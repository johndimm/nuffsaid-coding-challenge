import csv
import time
from count_schools import read_data

# Header and first line of data:
# NCESSCH,LEAID,LEANM05,SCHNAM05,LCITY05,LSTATE05,LATCOD,LONCOD,MLOCALE,ULOCALE,status05
# 010000200277,0100002,ALABAMA YOUTH SERVICES,SEQUOYAH SCHOOL - CHALKVILLE CAMPUS,PINSON,AL,33.674697,-86.627775,3,41,1

SCHOOL='SCHNAM05'
CITY='LCITY05'
STATE='LSTATE05'
REQUESTED_HITS=3

class School_search:

    def __init__(self):
        #
        # The index tells you which schools 
        # have a given word in their name, city, or state.
        # The states are abbreviated in this data.
        #
        self.data = read_data()

        self.words = dict()
        for idx in range(len(self.data)):
            line = self.data[idx]

            def add(field):
                for word in self.tokenize(line[field]):
                    if not word in self.words:
                        self.words[word] = []
                    # The identifier for a school is its index in the self.data array.
                    self.words[word].append(idx) 
            add(SCHOOL)
            add(CITY)
            add(STATE)

    def tokenize(self, buf):
        return buf.split(' ')

    def candidate_schools(self, query):  
        #
        # Make a query-specific inverted index.
        # For every school that matches a term of the query
        # store the term and the number of times it appears.
        #
        candidates = dict()
        query_terms = self.tokenize(query.upper())  # Source data happens to be UPPER CASE.
        for term in query_terms:
            if term in self.words:
                for idx in self.words[term]:
                    # idx is the index of this school in the self.data array.
                    if not idx in candidates:
                        # Add this school.  An array might be faster but uglier.
                        candidates[idx] = dict() 
                        
                    school = candidates[idx]    
                    if not term in school:
                        school[term] = 0 
                    school[term] += 1    
        return candidates

    def score_schools(self, candidates):    
        scores = dict()
        for idx in candidates:
            unique_matches = 0 
            total_matches = 0
            school = candidates[idx]
            for term in school:
                d = 1.0  # / len(self.words[term])                  # Use this for TF-IDF ranking

                # print ("idx: %d, term: %s, idf:%f, count: %d, df:%d" % 
                #  (idx, term, d, candidates[idx][term],len(self.words[term])))

                total_matches += school[term] * d
                unique_matches += d

            #
            # The most important thing is how many query terms are covered.
            # But a school gets some additional credit for having the same term twice.    
            #   
            scores[idx] = unique_matches * 10 + total_matches

        return scores   

    def perform_query(self, query):
        candidates = self.candidate_schools(query)
        scores = self.score_schools(candidates)

        results = []    
        rank = 0
        for idx in sorted(scores, key=lambda item: scores[item], reverse=True)[:REQUESTED_HITS]:
            r = self.data[idx]
            rank += 1
            results.append("%i. %s\n%s, %s" % (rank, r[SCHOOL], r[CITY], r[STATE]))

        return (len(candidates), results)

    def search_schools(self, _query):
        query = _query.strip()
        print ('\n' + query)
        print ('>>> school_search.search_schools("%s")' % query)

        t0 = time.time()
        (candidates, results) = self.perform_query(query)
        t1 = time.time()

        print ('Results for "%s" (search took: %fs, candidates: %s)' % (query, t1 - t0, candidates))
        for result in results:
            print (result) 
    
    def query_loop(self):
        while True:
            query = input('\nsearch schools: ')
            if len(query.strip()) == 0:
                # Stop if the user just hits return.
                return
            else:
                self.search_schools(query)

    def example_queries(self):
        queries = [
            'elementary school highland park',
            'jefferson belleville',
            'riverside school 44',
            'granada charter school',
            'foley high alabama',
            'KUSKOKWIM']
        for query in queries:
            self.search_schools(query)

# Search function for use in programs that import this module.
def search_schools(query):
    school_search.search_schools(query)

def example_queries():
    school_search.example_queries()

# Create an instance of this class.
school_search = School_search()

if __name__ == "__main__":
    school_search.example_queries()
    school_search.query_loop()
