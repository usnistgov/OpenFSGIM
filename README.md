# OpenFSGIM
A repository of software components for representing ASHRAE 201 Facility Smart Grid Information Model

## Background
September 24, 2018

In 2016 NIST contracted with ESTA International to support implementation of the American Society of Heating, Refrigerating and Air-Conditioning Engineers (ASHRAE) Facility Smart Grid Information Model (FSGIM), with particular focus on its weather model, “FSGIMWeather”. The project goals included constructing a profile of FSGIM to make the semantic model in the standard available for software development realizations of the standard. This repository contains the artifacts of that project. Communication of measured and forecasted weather data is important for many diverse Smart Grid applications. The ESTA project focused on the weather model component of FSGIM as a unifying model to support the exchange of weather information among different weather exchange standards. 

In FSGIMWeather, the principle resource aggregations of information are FSGIMWeatherForecast, FSGIMWeatherObservation, FSGIMWeatherBase, and potentially Phenomenon (perhaps modeled as a SubstitutionGroup in XMLSchema or alternatively Choice), FSGIMPrecipitation, FSGIMSolar, and FSGIMWind. FSGIMWeather also requires LocalTimeParameters from FSGIM which conveys local timezone information so that client applications can convert UTC to local time for presentation to users. These resources are concrete data structures that are modest in size and can be used as the target of a URL to use REST services to retrieve them.  These resources are built on classes that have associations with many other classes, and those other classes appear aggregated in the containing resource class. A goal of the ESTA project was to capture in the resource definitions all the optional and required attributes in the model, including those inherited from the external standards where needed. The FSGIMWeather resources were to be captured in their original form, structure, and multiplicities.

## What's in This Project
This project is the result of a realization of the goal to construct a profile of FSGIM, including an XML Schema representation of the FSGIM standard for use in implementing RESTful APIs for data exchange based on the standard. The goal of the profile is to refine the canonical model in the ASHRAE standard for the purpose of generating a conformant XML Schema syntactical representation of the semantic model. The profile was selected to meet the minimum conformance blocks identified in the standard. This repository includes a set of schemas that can be used for software development, and two sample software applications. The first client application can acquire weather information from NOAA at locations throughout the United States and produce schema-compliant FSGIMWeather XML data.  The second application can act as a client to an FSGIM server that might serve up FSGIM data. No FSGIM server, however, was constructed at this time.

## Folders

* Documents -- Contains documents describing the project deliverables
* Schemas -- Contains schemas generated from the UML model
* Source -- Contains source code for a NOAA client and a sample FSGIM client both written in Python
* UML -- The UML Profile of the FSGIM standard
 
