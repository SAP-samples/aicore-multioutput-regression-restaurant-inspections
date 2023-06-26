## Use Case
Assessing risk or criticality often requires manual input from experts and rarely benefits
from past assessments. This makes the overall process time-consuming and can lead
to inconsistency over time. To automate the computation of criticality, we propose a
machine learning (ML) service for criticality assessments in this mission. The
assessments used are examples based on restaurant
inspections where a health inspector - the expert - screens a restaurant and protocol
violations. The inspector then calculates a suitable score for the
restaurant. The data provided comes from a publicly available dataset
(Restaurant Scores - LIVES Standard in San Francisco published by Public Health) which has
been restructured to fit the ML approach of multi-output-regression. Since the SAP Data Attribute Recommendation service
(DAR) does not support multi-output-regression yet, this mission showcases a solution
leveraging SAP AI Core and open source. The approach of this mission can be easily adapted
to similar kinds of criticality assessments.
 
This mission is based on a real customer use case about criticality assessments which is currently in productization.

## Current Position - What is the challenge?
Organizations can have complex rules for their criticality assessments. Often, information that the
assessment needs is mostly input manually, which is prone to errors and can be time-consuming.
Besides that, due to individual approaches of different processors, inconsistencies can
arise over the time, yielding different results for similar inputs.

## Destination - What is the outcome?
The solution uses ML to assist the expert inspector, to conclude the criticality assessment. It does this by translating descriptions and details of a criticality assessment into multiple scores, automating the workflow and reducing manually lead inconsistencies.

## How You Get There - What is the solution?
A machine learning service that leverages the capabilities of SAP Business Technology Platform
(SAP AI Core and SAP AI Launchpad). The service assesses the criticality based on the descriptions of the criticality
assessment itself. In this case the descriptions are the violations the
inspector protocols during inspections. Since the descriptions consist of unstructured
text, they first will be transformed to vectors, so-called embeddings. Finally,
a multi-output-regression can be performed to determine multiple scores.