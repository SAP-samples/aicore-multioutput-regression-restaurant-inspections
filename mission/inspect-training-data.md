# Inspect Data for Training and Samples for later validation

## Background information about the data

In San Francisco, California (USA) Health Inspectors conduct *inspections* of the local
restaurants. For each inspection the inspector comes up with an *inspection score* that
represents the health conditions of the respective restaurant. The higher the score, the
better the conditions, and the lower the risk associated with eating at this restaurant.

## Content of the data
 
The data is stored as a CSV (comma-separated values) file and captures the following information:
 
1. Business zip code: The zip code represents the area in which the restaurant is
   located
2. Violations: A text description of the violations the inspector found during the restaurant inspection
3. Score: The overall inspection score based on the whole inspection
4. Lowest Score: The lowest partial score of all the partial scores that contribute to the overall inspection score
 
These four data columns are preprocessed, and used to train the
model. To see the preprocessing stepsm go to this [card](inspect-train-serve-impl.md). To download the
CSV file that contains the data described above, click [here]().