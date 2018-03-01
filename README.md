# musicRecommender
Program that recommends a music based on user response

Steps:

(1) Users listens at least 2 music files & input Like/Not Like 

(2) Based on the response, scans other music files & recommend another one 

(3) The user will provide the reponse on the new sample, this will keep update the result


Dependancies

1. pydub https://github.com/jiaaro/pydub
2. pyAudioAnalysis https://github.com/tyiannak/pyAudioAnalysis
3. ffmpg http://www.ffmpeg.org if you need to run non .wav files such as mp3

and many others...

Currently developing in window, not testing on other OS.


The algorithm works as following:
1. Slice music segments and extract 34 features from each segments. The features are composed of tempolar components, MFCC & chromatic components. ( Check more on the site of pyAudioAnalysis)
2. The user's choice will label all the segments as positive or negative (abstain will result in simply discarding)
3. Once the algorithm has at least one positive and one negative, it models using the algorithm of choice such as SVM, Gradient Boosting, Random Forest, Extra Trees.
4. The algorithm scans the rest of music file and select the one that has most positive slice components.

5. repeat -> 2 now with one more music data

1st Updated To Add New Features:

1. Give a choice to abstain on a music sample
2. Music Samples are shortened to 1 min (which may be changed in the code)
3. Give users to stop the program 
4. Display the history of the choices made on each music
5. Music files are saved to a file: If a file exists, the program loads the file. If not, read the music file and save it for later.

2nd Update 

1. Adding simulator that produces human like response to the system. MusicUser class has two functions (1) Random response to the music with (Y/N/A) 0.333 probability. Or (2) Load previous classifier to make the decision of the music.  In second case, the model must exist and directory must be specified. Currently, the model name must be 'SVM_RBF_Model'. 

