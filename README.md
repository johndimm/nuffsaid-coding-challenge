# Mini search engine to search data on schools
March 2020
John Dimm

https://gitlab.com/hari22/nuffsaid-coding-challenge

## Build
First generate an inverted index from the words in school names, cities, and state abbreviations. 

```
  key: word
  value: list of schools with this word
```

## Query
Given a query, look up each query term in the index to pull its lists of schools.  Scan the lists, pivoting from words to schools.  For each school, get the count of each query term. 

```
  key: school
  value: dictionary with
      key: query term
      value: number of occurrences in this school
```

To generate search results, a raw count of total occurrences of search terms in a school’s text is too easy.  A document with two occurrences of the same query term should rank below a document with two different query terms, although two is still somewhat better than one.

Solved here by ranking schools first by how many query terms they match, and second by the total number of query term occurrences found.  

```
  score = unique_matches * 10 + total_matches
```

## TF-IDF
To use TF-IDF, divide each term’s contribution to the score by the count of schools with that term.  

```
  d = 1.0 / len(self.words[term]) # Use this for TF-IDF ranking
```

The results are mostly the same.  The query “foley high alabama” finds schools with ‘alabama’, instead of ones with ‘foley’ as before.  That looked wrong but it turns out there are only 6 instances of alabama in the corpus and 9 of foley.  TF-IDF is doing its job.  “alabama” is rare because state names are abbreviated in the corpus.

## Next Steps

* track and rank city and name separately
* make use of position and word order
* spell check
* autocomplete

