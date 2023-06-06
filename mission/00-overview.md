## Use Case
Assessing risk or criticality often requires manual input from experts and rarely benefits
from past assessments. This makes the overall process time-consuming and potentially leads
to inconsistency over time. To digitize the computation of the criticality, we propose a
machine learning (ML) service for criticality assessments in this mission. The
assessments that are used throughout this mission are exemplary and based on restaurant
inspections where a health inspector, the expert, screens a restaurant and protocols
violations. In the end the inspector comes up with a suitable score for the
restaurant. The provided data comes from a publicly available dataset
(Restaurant Scores - LIVES Standard in San Francisco published by Public Health) which has
been restructured to fit the ML approach of multi-output-regression. Since the SAP Data Attribute Recommendation service
(DAR) does not support multi-output-regression yet, this mission showcases a solution
leveraging SAP AI Core and open source. The approach of this mission can be easily adapted
to similar kinds of criticality assessments.
 
This mission is based on a real customer use case about criticality assessments which is currently in productization.

## Current Position - What is the challenge?
Organizations can have complex rules for their criticality assessments. Many times, the
assessment is dominated by manual input, which is prone to errors and can be time-consuming.
Besides that, due to individual approaches of different processors, inconsistencies can
arise over the time, yielding different results for similar inputs.

## Destination - What is the outcome?
The solution uses ML to assist the processor of criticality assessments by translating descriptions and details of a criticality assessment to multiple scores necessary to conclude the assessment.

## How You Get There - What is the solution?
A machine learning service that leverages the capabilities of SAP Business Technology Platform
(SAP AI Core and SAP AI Launchpad). The service assesses the criticality based on the descriptions of the criticality
assessment itself. In this case the descriptions are the violations the
inspector protocols during the inspections. Since the descriptions consist of unstructured
text, they first will be transformed to vectors, so-called embeddings. Finally,
a multi-output-regression can be performed to determine multiple scores.