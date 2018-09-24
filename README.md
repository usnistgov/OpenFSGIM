# OpenFSGIM
A repository of software components for representing ASHRAE 201 Facility Smart Grid Information Model

## Background
September 24, 2018

Communication of measured and forecasted weather data is important for many diverse Smart Grid applications. In fact, there are use cases that illustrate the benefits of weather data exchange. Today there are multiple Standards Setting Organizations (SSOs) with weather information exchange related standards development efforts. These efforts are uncoordinated and can benefit from efforts to ensure coverage and interoperability for the wide range of Smart Grid measured and forecasted weather information exchange requirements.  This task order addresses one particular use case, addressing the implementation of the American Society of Heating, Refrigerating and Air-Conditioning Engineers (ASHRAE) Facility Smart Grid Information Model (FSGIM), with particular focus on its weather model, “FSGIMWeather”.

In 2016 NIST contracted with ESTA International to construct a profile of FSGIM to make the semantic model in the standard available for software development realizations of the standard. This repository contains the artifacts of that project.

Included in these artifacts are a set of schemas that can be used for software development, and, two sample software applications that allow for NOAA weather data to be fetched and converted to FSGIM XML format, and, can act as a client to an FSGIM server that might serve up FSGIM data. No FSGIM server, however, was constructed at this time.

## Some Details

The Green Button set of technologies are based on the RESTful API and third party authorization governed exchanges of energy usage information. Underlying this technology is a basic approach to exposing any complex data source using this web service approach.

For Green Button, the principle data structures that are termed “Resources” are UsagePoint, MeterReading, IntervalBlock, ReadingType, & UsageSummary. There are a few others as well. For FSGIMWeather, the similar aggregations of information are FSGIMWeatherForecast, FSGIMWeatherObservation, FSGIMWeatherBase, and potentially Phenomenon (perhaps modeled as a SubstitutionGroup in XMLSchema or alternatively Choice), FSGIMPrecipitation, FSGIMSolar, and FSGIMWind. FSGIMWeather will also require LocalTimeParameters from FSGIM which conveys local timezone information so that client applications can convert UTC to local time for presentation to users. 

What is unique about “Resources” in the Green Button model is that they are concrete data structures that are modest in size and can be used as the target of a URL to use REST services to retrieve them.  Note that these resources are built on classes that have associations with many other classes. Those other classes that are not Resources themselves appear aggregated in the containing Resource class.

It is desired to capture in the resource definitions all the optional and required attributes in the model, including those inherited from the external standards where needed. It is not desired to coerce these data structures to look like the Green Button resources. The FSGIMWeather resources are to be captured in their original form, structure, and multiplicities.

## What's in This Project
This project is the result of a realization of these goals to make an XML Schema representation of the FSGIM standard for use in implementing RESTful APIs for data exchange based on the standard.

The goal of the profile is to refine the canonical model in the ASHRAE standard for the purpose of generating a conformant XML Schema syntactical representation of the semantic model.

The profile was selected to meet the minimum conformance blocks identified in the standard.

Additionally, a subset for the FSGIMWeather was created and a client application developed that can acquire weather information from NOAA on locations throughout the United States and produce schema compliant FSGIMWeather XML data.

## Folders

* Documents -- Contains documents describing the project deliverables
* Schemas -- Contains schemas generated from the UML model
* Source -- Contains source code for a NOAA client and a sample FSGIM client both written in Python
* UML -- The UML Profile of the FSGIM standard
 