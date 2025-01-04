## Technical Report: Search Engine Enhanced Version

## Introduction

This report describes the improvements and changes made to the search engine implementation, with a focus on performance optimization, architecture, and decision reasons.

## System changes

### Crawler

One of the non-mentioned challenges in the technical report was the incorrect webpages with broken pdf files or webpages with incorrect content, to handle that the search engine now catches all errors from indexing pipeline and logs the error messages without interrupting the crawling process overall, because otherwise it will require the manual restarting of the crawling process of the search engine.

To improve the systems performance now instead of directly calling the indexing pipeline callback, crawler creates asynchronous task to index the content of webpages and utilizes response waiting time to index the content of the webpage. Since the network speed is much slower than indexing speed every webpage will be succesuflly indexed, but for safety if the number of not completed tasks is higher than predefined threshold the crawler enforce task waiting. 

### Tokenizers and Indexes

Most of the changes in the tokenization and indexing process are related to improvements in the search algorithm, and mostly changes have been made to the first tokenizer and index pair to maintain an inverted index.

1. Stemming process now included in tokenization, to imporve searching algorithm. So basically it was musthave part for the search engine, because obviously the same words with different ends have the same meaning and must be calculated in the initial score.

2. 2-grams and 3-grams(over words) now also included in the working dictionary. Such technique allows to handle cases where not only words in phrase are important, but the phrase itself is important. For example "Data Science", before we had search over "data" and "science" words, but webpage can contain something like "Data Analytics ... Life Science", and the information will be not that important.

3. The scoring formula have been changed to make the score calculation more efficient, that modification is connected with change in the inverted index storing that will be described later. Now we use something like that:

$$\text{Score}(\text{document}) = \sum\limits_{\text{keyword} \in \text{T}} \sum\limits_{k = 0}^{C(KW, D) - 1} \frac{7}{8} \cdot \frac{1}{8^k} = \sum\limits_{\text{keyword} \in \text{T}} \left(1 - \frac{1}{8^\text{C(KW, D)}}\right)$$

The other changes in indexes and tokenizers are not important, but here I also want to clarify one thing that wasn't described before. Why do we need to use semantic index instead of something classcial method? So the main reason that the main use case of the currently written search engine is to retrieve information from the webpages and get the documents for the Retrieval-Augmented Generation, so the search queries will be not standard queries as in Google, they'll be way longer, to handle long queries I need something that can capture the main semantic meaning and identify useful documents for further work. But that method has strong drawback, the storage usage can be compressed since we're storing a bunch of vectors and can't compress this type of data.

### Database

The database implementation has been slighlty updated. Previously, an index was not created in the database, and that lead to linear time for search and insert operation, but in the new implementation these operations work in log(|Documents|) time, because creating MongoDB indices that lead to the creation of a balanced binary tree data structure. Storing a balanced binary tree with a small constant factor is likely the best approach for performing such queries. However, the main advantage of such approach (it can perform range queries over oredered data) is not necessary for the current tasks, so using a hash table may be more suitable. But since the other parts of the system are linear, the database queries are not a significant performance concern, except for the is_visited(web page) part, so for now it's not important.

The method of storing the inverted index was changed to store the inverted index as postings rather than as a postings list (inverted list). This is because MongoDB handles queries over postings more efficiently than over postings lists. While it may be possible to achieve similar performance with postings lists, the difference is not expected to be significant. For working with postings, the time complexity is O(log(N) + k), where N is the number of postings and k is the number of documents. In the case of postings lists, the most optimal approach works in O(k) using a hash table. However, since k is usually large enough and the number of queries to the collection per search query is small, this difference can be ignored. Also instead of storing the same URL in the posting list multiple times, pairs of (URL, frequency) are now stored. This makes the scoring process faster, and the changes to the scoring formula allow the score to be calculated using fewer operations with this format.

Also to improve the performance of the system, instead of sending individual queries to the database, queries are now grouped and sent together using MongoDB's "bulk_write" operation.

## Performance

The time usage initially required the search engine to spend 22.5 hours to index 8900 web pages. After optimizing the database, the time was reduced to 4.5 hours for the same number of web pages. Introducing asynchronous pipeline code further reduced the time to 2.25 hours.  Potential improvements could bring the time down to 1-1.5 hour, but further optimization is limited due to network speed. 

Becaues of that the logical question arises, whether rewriting the code is necessary if Python can index all web pages within the total request waiting time, implementation on other languages cannot improve the network speed. But atleast the perfomrance for the search queries also need to be considered, and Python is too slow to handle them fastly, so rewriting the code to C++ could be beneficial.