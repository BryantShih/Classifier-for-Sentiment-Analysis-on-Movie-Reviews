Programming Language: Python 2.7.3
External Library: NLTK (just using in preprocessing)

How to run it:

./train training_set.csv model_file: 
training_set.csv is the input, and model_file is the output which contains 
the serialized trained model. 
Notice: because I use pickle to output the 
model, please name the model_file in file type .pkl For example, model.pkl 
is a valid file name for model. 

./test model _file testing_set.csv prediction_file: the first two parameters are input 
to the program and the last one is the output file. The model _file is the trained 
model, test set.csv is the input test set, and prediction _file is a line separated 
.csv file with example id and one class label per line in the same order of the test 
set.
Notice: model_file is also a .pkl file mentioned above. And prediction_file is a 
.csv file.
