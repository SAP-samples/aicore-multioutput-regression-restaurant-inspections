# Learn about the goal and outcome of the mission

The goal of this mission is to digitize *risk assessments* in order to assist
inspectors in coming up with risk scores for restaurants as part of
restaurant inspections.

To do so you will leverage the *SAP AI Core* service that is part of the service portfolio
of SAP Business Technology Platform (SAP BTP) together with open source software like
Docker and scikit-learn. You will train a *multi-output-regression* machine learning (ML)
model and deploy it in the form of an inference service on SAP BTP.

This service assists the inspectors in that it proposes a suitable risk score for the
inspected restaurant. The score that the model computes is based on input data about the
inspection in question and on past risk assessments which the model has been trained on.

Therefore, the outcome of the mission is a deployed inference service whose trained model
can compute risk scores for risk assessments in the context of restaurant inspections. One can send requests
with data about an inspection to the service in order to receive a risk score predicted by the model.
More importantly the code that is used throughout this mission can be adapted to other
similar kinds of risk assessments.