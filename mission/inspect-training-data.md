# Inspect Data for Training and Samples for later validation

## Background information about the data

In San Francisco, California (USA) Health Inspectors conduct *inspections* of the local
restaurants. For each inspection the inspector comes up with an *inspection score* that
represents the health conditions of the respective restaurant. The higher the score the
better are the conditions and as such the risk associated with eating at this restaurant
decreases.

## Content of the data
 
The data is stored as a CSV (comma-separated values) file and captures the following information:
 
1. Business postal code: The postal code represents the area in which the restaurant is
   located.
2. A text description of the violations the inspector found during the restaurant inspection
3. The overall inspection score based on the whole inspection
4. The lowest partial score of all the partial scores that contribute to the overall inspection score
 
One preprocesses these four data columns and uses the result as training data to train the
model. To see what the preprocessing steps are, go to this [card](inspect-train-serve-impl.md). To download the
CSV file that contains the data described above, click [here]().