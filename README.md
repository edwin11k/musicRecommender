# musicRecommender
Program that recommends a music based on user response

Steps:

(1) Users listens at least 2 music files & input Like/Not Like 

(2) Based on the response, scans other music files & recommend another one 

(3) The user will provide the reponse on the new sample, this will keep update the result


Dependancies

1. pydub https://github.com/jiaaro/pydub
2. pyAudioAnalysis https://github.com/tyiannak/pyAudioAnalysis

and many others...

Currently developing in window, not testing on other OS.


The algorithm works as following:
1. Slice music segments and extract 34 features from each segments. The features are composed of tempolar components, MFCC & chromatic components. ( Check more on the site of pyAudioAnalysis)
2. The user's choice will label all the segments as positive or negative (abstain will result in simply discarding)
3. Once the algorithm has at least one positive and one negative, it models using the algorithm of choice such as SVM, Gradient Boosting.
4. The algorithm scans the rest of music file and select the one that has most positive slice components.

