#coding: utf-8
from flask import Flask, render_template, request, flash, redirect, url_for, session, logging, g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import URLSafeTimedSerializer
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_mail import Mail, Message
from sqlalchemy import Integer, ForeignKey, String, Column, Text
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Sequence
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
import secrets
import os
import spacy
import json
import random
import en_core_web_sm
import models
from spacy.tokens import Doc
from spacy.training import Example
from spacy.util import minibatch, compounding
from pathlib import Path
from functools import wraps

nlp = en_core_web_sm.load()

ner = nlp.get_pipe("ner")

TRAIN_RESUME_DATA =[("Name: Abiral Pandey\nEmail: abiral.pandey88@gmail.com\nPhone: 940-242-3303\nCurrent Location: Woonsocket, Rhode Island\nVisa Status: US Citizen\n\nSUMMARY:\n•\tDynamic individual with 6 years of software development experience in design, development, deployment, maintenance, production and support of web - based and Client-Server business applications using OOP and Java/J2EE technologies.\n•\tExposure to all phases of Software Development Life Cycle(SDLC) using Agile, RUP, Waterfall.\n•\tDesigned and developed web UI screen using Angular-JS.\n•\tDeveloped AngularJS Controllers, Services, filters and directives for various modules in the application.\n•\tKnowledge on ETL tools like Kettle Pentaho and Microsoft SSIS tools.\n•\tCreated custom directives, decorators and services using AngularJS to interface with both RESTful and legacy network services also DOM applications.\n•\tExperience with MVC frameworks like Struts, SPRING and ORM tools like Hibernate.\n•\tExperienced in working with batch jobs using Spring-Batch, Autosys and Quartz.\n•\tWorked extensively with XML related technologies like XML/XSLT to process, validate, parse and extract data from XML using DOM and SAX parsers for DTD and SCHEMAand also worked with JAX-B.\n•\tStrong experience in J2EE technologies like Java Beans, Servlets, JSP (including custom tags), JSTL, JDBC, Struts, Spring, JMS, JNDI and Multithreading.\n•\tExpertise in web development technologies like HTML, DHTML, XHTML, CSS, Java Script, JQuery, JSF, AJAX, Bootstrap JS, Node JS and Angular JS.\n•\tExperienced in RESTful web services using JAX-RS, Jersey framework and SOAP using JAX-WS, Axis-2 framework.\n•\tExpert knowledge over J2EE Design Patterns like MVC, Adapter, Front End Controller, Value object, Singleton, Session Facade, Business Delegate, Factory DAO in designing the architecture of large applications.\n•\tExperience in using Maven and Ant build scripts for the project build automation.\n•\tExperience in using version control and configuration management tools like SVN, Clear Case and CVS.\n•\tExpertise in working with various Application Servers such as IBM WebSphere, JBoss, Glassfish, Oracle WebLogic and Apache Tomcat server.\n•\tGood knowledge in using ’s such as Eclipse, NetBeans, JBuilder, RAD and STS.\n•\tExpertise in working with Relational databases such as Oracle, PostgreSQL, DB2, MySQL and NoSQL database MongoDB.\n•\tExperience in database design using PL/SQL to write Stored Procedures, Functions, Triggers, views and good at writing complex queries for Oracle 10g/11g.\n•\tGood experience in developing test cases with JUnit for Unit testing, Load testing and logging using Log4J.\n•\tExperienced in using Operating Systems like Windows 98 / 2000 / NT / XP, AIX, Sun Solaris.\n•\tProficient in software documentation and technical report writing.\n•\tInvolved in Performance analysis and improvements of the application using tools like Jmeter and using commands on Unix box to resolve deadlocks and improve performance.\n\nTECHNICAL SKILLS:\nProgramming Languages: Java/J2EE, PL/SQL, Unix Shell Scripts\nJava/J2EE Technologies: JavaBeans, collections, Servlets, JSP, JDBC, JNDI, RMI, EJB\nFrameworks: Struts 1.x/2.x, Spring 2.5/3.0, Web Framework, JSF, Hibernate, iBatis, JPA, Axis-2, Jersey\nMethodologies/Design Patterns: OOAD, OOP, UML, MVC, Singleton, DTO Pattern, DAO Pattern, Service Fa ade, Factory Pattern\nBuild Automation: Jenkins, Maven, Ant\nApplication/Web Servers: IBM Web Sphere 6.x/5.x, BEA Web Logic 8.1/9.1, Apache Tomcat 5.x/6.x, JBOSS 4.x/3.x\nXML processing: DTD, Schema, JAX-P (DOM, SAX), JAX-B\nWeb Services: RESTful, SOAP\nWeb Development: HTML, DHTML, XHTML, CSS, Java Script, JQuery, AJAX, LADP, JSF, Bootstrap JS, Node JS, Angular JS\nVersion Control Tools: CVS, Harvest, IBM Clear case, SVN and GIT\nDatabases: Oracle 9i/10g/11g, IBM DB2, SQL Server 2005/2008, PostgreSQL, MySQL, MangoDB\nMessaging Techologies: JMS, IBM MQ\nIDE s: Eclipse, NetBeans, RAD, WSAD\nTesting and Logging Frameworks: Junit, Log4j, Mockito, Finesse Tests\nReporting Tools: Crystal Reports 11, Jasper Reports\nTools: Rational Rose, MS Visio, XML Spy, TOAD\nOperating Systems: Windows 98/2000/NT/XP, AIX, Sun Solaris, HP-UX\nPROFESSIONAL EXPERIENCE:\n\nCVS, Woonsocket, Rhode Island                                 Full Stack Java Developer\nApril 2016 – Present\nResponsibilities:\n•\tInvolved in various stages of Software Development Life Cycle (SDLC) deliverables of the project using the Agile methodology.\n•\tUsed AWS Cloud platform and its features which include EBS, AMI, SNS, RDS, EBS, Cloud Watch, Cloud Trail, Cloud Formation, Cloud Front, S3, and Route53. \n•\tExpertise in building rich, interactive user interfaces using HTML, CSS, JavaScript, jQuery, Node.Js and Angular.Js.\n•\tGathered and clarified requirements with business analyst to feed into high-level customization design, development and installation phases.\n•\tUsed Spring Framework for dependency injection for Action classes using Application Context XML file. \n•\tInvolved in implementation of MVC pattern using JSP and Spring Controller.\n•\tDeveloped business objects using Spring IOC, Spring MVC and Spring AOP. Implemented MVC architecture using JSP Spring, Hibernate and used Spring Framework to initialize managed beans and services.\n•\tImplemented SOA architecture with Web Services using SOAP, JAX-WS, WSDL, UDDI and XML.\n•\tUsed Collections for Model classes in the DAO layer (Data Access Object) Involved in modifying some changes in DAO layer using Hibernate.\n•\tCreated mappings among the relations and written SQL queries using Hibernate.\n•\tImplemented Concurrency, Exception Handling and Collections whenever necessary.\n•\tUsed Entity Beans to persist the data into IBM DB2 database like database access components, Creating Schemas and Tables.\n•\tUsed SQL to perform data mapping and backend testing, also documented all the SQL queries for future testing purpose.\n•\tCreated process flow for deploying application in Web Sphere application server.\n•\tManaged build, reporting and documentation from the project information using Jenkins, Maven Tool and SVN for version control.\n•\tUsed Jenkins for Continuous Integration.\n•\tUsed JUnit for testing and used JIRA for tracking bugs.\n•\tResponsible for the dealing with the problem, bug fixing and troubleshooting.\n Environment: Java, J2EE, HTML, CSS, JavaScript, jQuery, Ajax, Spring, Spring IOC, Spring AOP, Spring MVC, Hibernate, REST, SOAP, XML, Eclipse, PL/SQL, JUnit, Maven Build Tool, DB2, JIRA, Jenkins, SVN and IBM Web Sphere, AngularJS, EBS, AMI, SNS, RDS, Cloud Watch, Cloud Trail, Cloud Formation, Auto scaling\n\nToll Brothers, Horsham Township, Pennsylvania                  Software Engineer\nDecember 2015 -  March 2016\nResponsibilities:\n•\tDeveloped JSP and extensively used tag libraries. \n•\tDesigned the system with OOAD methodology using various design patterns like factory method, Singleton, Adaptor, Template etc. \n•\tImplementing and planning the server-side architecture using Spring and Hibernate \n•\tConfigured the spring framework for entire business logic layer with XML bean configuration files. \n•\tPreparation of Low Level Designing and High Level Designing and relevant documentation. \n•\tExtensively used Spring IOC for Dependency Injection and worked on Custom MVC Frameworks loosely based on Struts \n•\texperienced in build tools like Micro services, Ant, Maven and Gradle tools.\n•\tWrote Controller classes in Spring MVC framework in the web layer. \n•\tProduced the shopping cart on the client Front-end using jQuery, JavaScript, HTML5, CSS3. \n•\tExtensively used Eclipse based STS IDE for building, developing and integrating the application. \n•\tUsed Table per hierarchy inheritance of hibernates and mapped polymorphic associations. \n•\tDeveloped one-much, many-one, one-one annotation based mappings in Hibernate. \n•\tWrote queries Using Cassandra CQL to create, alter, insert and delete elements. \n•\tDeveloped DAO service methods to populate the domain model objects using hibernate. \n•\tUsed java collections API extensively such as Lists, Sets and Maps.  \n•\tWrote DAO classes using spring and Hibernate to interact with database for persistence. \n•\tDeveloped components of web services (JAX-WS, JAX-RPC) end to end, using different JAX-WS standards with clear understanding on WSDL, SOAP using various message patterns  \n•\tPerformed on e-Commerce by using JSF framework and JavaScript, jQuery, HTML5 pages\n•\tWrote and tested Java Beans to retrieve trading data and subscriber's information from MySQL database server,\n•\t Extensive experience in Angular.JS for application implementation, proficient in creating modules, controllers, route-Providers, factory services, ng-repeat, customizable filter, http get/post methods and directives to realize functionalities like REST service with Ajax call , input validations, searchable and sortable contents.  \n•\tImplemented Unit and Integration test cases with JUnit Framework based on Functional Flow. \n•\tUsed tools like My Eclipse IDE, configured and deployed the applications onto Web Logic application server \n•\tConfigured Log4j for logging and debugging \n Environment: Eclipse, Java J2EE, HTML, JSP, JAX RPC, JAXB, CSS3, JavaScript, and jQuery, Spring MVC, Hibernate, RESTful web services, Apache Tomcat7.0, Cucumber, Cassandra, Junit, Jenkins, Maven, GitHub, XML, Log4j, EJB, MySQL, Ajax.\n\nDairy Farmers of America, Kansas City, Missouri                      Java Developer\nNovember 2014 – December 2015\nResponsibilities:\n•\tResponsible for developing use cases, class and sequence diagram for the modules using UML and Rational Rose.\n•\tIdentifying and design of common interfaces across multiple systems or modules of social insurance.\n•\tDeveloped the application using Spring Framework that leverages classical Model View Layer (MVC) architecture. UML diagrams like use cases, class diagrams, interaction diagrams (sequence and collaboration) and activity diagrams were used.\n•\tDeveloped J2EE modules using XMI and CORE JAVA.\n•\tInteraction with Business users for user and system acceptance testing.\n•\tValidated the data against the business rules.\n•\tData access layer is implemented using Hibernate.\n•\tUsed Apache POI to generate Excel documents\n•\tImplemented Struts action classes.\n•\tUsed Spring Security for Authentication and authorization extensively.\n•\tUtilized Eclipse to create JSPs/Servlets/Hibernate that pulled information from a Oracle database and sent to a front end GUI for end users.\n•\tUsed JDBC for Oracle database connection and written number of stored procedures for retrieving the data.\n•\tDeveloped modules for validating the data according to business rules and used Castor to convert data into array of XML strings and XSLT for transformation.\n•\tUsed Hibernate for data persistence.\n•\tDeveloped SOAP based HTTP requests for communicating with Web Services.\n•\tWas involved in the design of multi-tier architecture using EJB, Servlets and JSP.\n•\tUsed Spring Dependency Injection properties to provide loose-coupling between layers.\n•\tCollaborated with Web designers to create the JSP pages, applying HTML, JavaScript, JQuery and Struts Tags.\n•\tExtensively worked on debugging using Logging Frameworks such as Apache Log4j.\n•\tCreated test plans for unit testing to validate component functionality.\nEnvironment: Java 1.4.2, J2EE, Servlets, MVC, Web services, Struts, Spring - Core, MVC, Security, Eclipse, Hibernate, XML, XSLT, EJB, JSP, JDBC, JAX-B, JQuery, JavaScript, HTML, Log4j, Oracle 10g, Apache POI, Caster, XMI.\n\nBank of Utah, Ogden, Utah                                                           J2EE Developer\nMay 2013 – October 2014\n\nResponsibilities:\n•\tDesigned and developed Servlets and JSP, which presents the end user with form to submit the details of the problem.\n•\tCreated SQL statements and triggers for the effective retrieval and storage of data from the database.\n•\tPerformed JUnit testing, proposed and implemented performance enhancements, worked with Oracle databases, running SQL scripts and stored procedures.\n•\tDeveloped Restful based Web Services.\n•\tWas involved in the design of multi-tier architecture using EJB, Servlets and JSP.\n•\tDeveloped Servlets used to store user information in the database, which makes a JDBC-ODBC connection to the database and inserts the details into to the database.\n•\tDesigned and developed a Servlet, which presents the engineer a form to submit solution to particular problem.\n•\tSetting up test environments and configuring various components of the application using JDBC API to establish a connection with oracle database and configuring.\n•\tDesigned and developed a Servlet, which allows the end user to query on the problem, makes a JDBC-ODBC connection to the database and retrieve the details regarding the call number and the status of the submitted problem.\nEnvironment: Java, J2EE, Servlets, JSP, EJB, Custom tags, JDBC, JUNIT, Restful, Data Source, DAO, VO Patterns, Tomcat 5.0, SQL, Oracle 9i, Linux.\n\n\nEpsilon, Irving, Texas                                                         Junior Java Developer\nJanuary 2012 – April 2013\nResponsibilities:\n•\tDesigned the user interfaces using JSP.\n•\tDeveloped Custom tags, JSTL to support custom User Interfaces.\n•\tDeveloped the application using Struts (MVC) Framework.\n•\tImplemented Business processes such as user authentication, Account Transfer using Session EJBs.\n•\tUsed Eclipse to writing the code for JSP, Servlets, Struts and EJBs.\n•\tDeployed the applications on Web Logic Application Server.\n•\tUsed Java Messaging Services (JMS) and Backend messaging for reliable and asynchronous exchange of important information such as payment status report.\n•\tDeveloped the Ant scripts for preparing WAR files used to deploy J2EE components.\n•\tUsed JDBC for database connectivity to Oracle.\n•\tWorked with Oracle Database to create tables, procedures, functions and select statements.\n•\tUsed JUnit Testing, debugging and bug fixing.\n•\tUsed Log4J to capture the log that includes runtime exceptions and developed WAR framework to alert the client and production support in case of application failures.\n•\tWorked in Rational Unified Process (RUP) Methodology.\nEnvironment: Java, J2EE, JSP, JSTL, JDBC, Struts, EJB, JMS, Oracle, HTML, XML, Web Logic, Ant, CVS, Log4J, JUnit, JMS, PL/SQL, JavaScript, Eclipse IDE, UNIX Shell Scripting, Rational Unified Process (RUP).\nEducation: \nBachelor of Computer Science – University of North Texas, Denton, Texas", {'entities': [(176, 218, 'YEARS'), (222, 382, 'RESPONSIBILITIES'), (386, 477, 'RESPONSIBILITIES'), (481, 534, 'RESPONSIBILITIES'), (538, 642, 'RESPONSIBILITIES'), (674, 688, 'SKILLS'), (693, 713, 'SKILLS'), (848, 864, 'SKILLS'), (884, 898, 'SKILLS'), (912, 918, 'SKILLS'), (923, 932, 'SKILLS'), (996, 1008, 'SKILLS'), (1010, 1017, 'SKILLS'), (1022, 1028, 'SKILLS'), (1056, 1080, 'SKILLS'), (1318, 1322, 'SKILLS'), (1431, 1436, 'SKILLS'), (1438, 1443, 'SKILLS'), (1450, 1461, 'SKILLS'), (1476, 1480, 'SKILLS'), (1496, 1503, 'SKILLS'), (1508, 1518, 'SKILLS'), (1482, 1494, 'SKILLS'), (1776, 1787, 'SKILLS'), (1873, 1876, 'SKILLS'), (1967, 1997, 'SKILLS'), (2213, 2221, 'SKILLS'), (2223, 2231, 'SKILLS'), (2233, 2236, 'SKILLS'), (2241, 2244, 'SKILLS'), (2311, 2321, 'SKILLS'), (2338, 2343, 'SKILLS'), (2353, 2360, 'SKILLS'), (2576, 2588, 'SKILLS'), (2590, 2602, 'SKILLS'), (2651, 2668, 'SKILLS'), (2737, 2759, 'SKILLS'), (2764, 2788, 'SKILLS'), (3601, 3606, 'SKILLS'), (3608, 3613, 'SKILLS'), (3620, 3631, 'SKILLS'), (3641, 3645, 'SKILLS'), (3672, 3679, 'SKILLS'), (3681, 3691, 'SKILLS'), (3658, 3670, 'SKILLS'), (3384, 3387, 'SKILLS'), (3066, 3075, 'SKILLS'), (3818, 3828, 'SKILLS'), (3880, 3883, 'SKILLS'), (3896, 3904, 'SKILLS'), (3906, 3909, 'SKILLS'), (4083, 4100, 'SKILLS'), (4304, 4428, 'RESPONSIBILITIES'), (4432, 4583, 'RESPONSIBILITIES'), (4588, 4685, 'RESPONSIBILITIES'), (4707, 4846, 'RESPONSIBILITIES'), (4850, 4950, 'RESPONSIBILITIES'), (4955, 5028, 'RESPONSIBILITIES'), (5032, 5102, 'RESPONSIBILITIES'), (5104, 5227, 'RESPONSIBILITIES'), (5231, 5316, 'RESPONSIBILITIES'), (5320, 5456, 'RESPONSIBILITIES'), (5460, 5536, 'RESPONSIBILITIES'), (5540, 5618, 'RESPONSIBILITIES'), (5622, 5742, 'RESPONSIBILITIES'), (5746, 5862, 'RESPONSIBILITIES'), (5866, 5945, 'RESPONSIBILITIES'), (5949, 6074, 'RESPONSIBILITIES'), (6078, 6117, 'RESPONSIBILITIES'), (6121, 6175, 'RESPONSIBILITIES'), (6179, 6255, 'RESPONSIBILITIES'), (6748, 6873, 'RESPONSIBILITIES'), (6878, 6959, 'RESPONSIBILITIES'), (6963, 7060, 'RESPONSIBILITIES'), (7065, 7151, 'RESPONSIBILITIES'), (7320, 7323, 'SKILLS'), (7549, 7552, 'SKILLS'), (7545, 7548, 'SKILLS'), (7869, 7951, 'RESPONSIBILITIES'), (7956, 8022, 'RESPONSIBILITIES'), (8028, 8114, 'RESPONSIBILITIES'), (8119, 8288, 'RESPONSIBILITIES'), (8293, 8375, 'RESPONSIBILITIES'), (8378, 8486, 'RESPONSIBILITIES'), (8491, 8522, 'RESPONSIBILITIES'), (8523, 8820, 'RESPONSIBILITIES'), (8947, 8950, 'SKILLS'), (9460, 9552, 'RESPONSIBILITIES'), (9556, 9654, 'RESPONSIBILITIES'), (9899, 9945, 'RESPONSIBILITIES'), (9949, 10019, 'RESPONSIBILITIES'), (10023, 10068, 'RESPONSIBILITIES'), (10072, 10120, 'RESPONSIBILITIES'), (10124, 10167, 'RESPONSIBILITIES'), (10170, 10203, 'RESPONSIBILITIES'), (10207, 10276, 'RESPONSIBILITIES'), (10280, 10419, 'RESPONSIBILITIES'), (10423, 10527, 'RESPONSIBILITIES'), (10531, 10686, 'RESPONSIBILITIES'), (10690, 10725, 'RESPONSIBILITIES'), (10729, 10799, 'RESPONSIBILITIES'), (10803, 10884, 'RESPONSIBILITIES'), (10888, 10972, 'RESPONSIBILITIES'), (10976, 11082, 'RESPONSIBILITIES'), (11086, 11163, 'RESPONSIBILITIES'), (11167, 11238, 'RESPONSIBILITIES'), (12022, 12103, 'RESPONSIBILITIES'), (12107, 12269, 'RESPONSIBILITIES'), (12273, 12382, 'RESPONSIBILITIES'), (12386, 12546, 'RESPONSIBILITIES'), (13067, 13105, 'RESPONSIBILITIES'), (13132, 13136, 'SKILLS'), (13232, 13327, 'RESPONSIBILITIES'), (13402, 13459, 'RESPONSIBILITIES'), (13463, 13613, 'RESPONSIBILITIES'), (13631, 13634, 'SKILLS'), (13891, 14056, 'RESPONSIBILITIES'), (14144, 14148, 'SKILLS'), (14204, 14207, 'SKILLS'), (14261, 14264, 'SKILLS'), (14320, 14360, 'EDUCATION')]})]

ner.add_label('SKILLS')
ner.add_label('YEARS')
ner.add_label('RESPONSIBILITIES')
ner.add_label('EDUCATION')

pipe_exceptions = ["ner"]
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

with nlp.disable_pipes(*unaffected_pipes):
    for iteration in range(4):
        random.shuffle(TRAIN_RESUME_DATA)
        for raw_text,entity_offsets in TRAIN_RESUME_DATA:
            resume=nlp.make_doc(raw_text)
            nlp.update([Example.from_dict(resume,entity_offsets)])

resume = nlp("""Anudeep
Sr Java Programmer
anudeepreddynallamada@gmail.com


PROFESSIONAL SUMMARY:
•	IT professional with 8+ years of IT experience in designing and developing N-tier applications based on OOPS (Object Oriented Programming), Internet and Intranet, Client-Server Architecture using Java/J2EE and supporting technologies.
•	 Strong Experience in developing user interfaces with HTML, DHTML, XML and CSS. 
•	Experienced in processing, validating, parsing and extracting data from .xml file. 
•	 Worked with scripting languages like JavaScript, JQuery. 
•	 Well versed in MVC (Model View Controller) architecture using Spring, JSF and implementing JSTL (JSP Standard Tag Library), custom tag development and tiles. 
•	 Experience in JSP, Java Beans and Servlets for developing applications using MVC architecture. 
•	 Good exposure in implementing web services-WSDL using SOAP protocol. 
•	 Experienced in Persistence Framework like Hibernate ORM (Object Relational Mapping) in a typical n-tier architecture. 
•	Experienced in build tools like ANT and Maven. 
•	Experienced in using testing Frameworks like JUnit and JMockit. 
•	Experienced in using logging tools like Intellij and Log4j. 
•	Hands on experience on Web/Application servers such as Apache Tomcat, JBoss, WebLogic and Web Sphere. 
•	Experienced in developing various UML designs like class diagrams, cases and sequence diagrams using Rational Rose. 
•	Worked on different platforms like Windows 2003 Server, Windows 2000 Professional, Windows XP, Windows […] UNIX and LINUX. 
•	Experience in using UML like Rational Rose and MS Visio 
•	Well versed in using version control tools like SVN, Clear Case and CVS. 
•	Strong experience in using IDEs like Eclipse, NetBeans and RAD
•	Developed projects and products using Agile Methodology, SDLC (Software development life cycle), from initiation, planning, designing, execution, implementation and Maintenance.
EDUCATION:
Bachelor of Engineering in Computer Science and Engineering        JNTU, Hyderabad, India.     2009
TECHNICAL SKILLS:

Languages	C, C++, JAVA/J2EE, PL/SQL, Shell script, UNIX commands.
Java Technologies	Core Java, J2EE, JSP, Servlet, JDBC, JMS, JavaBeans, JNDI, Java Mail, Java1.8.
Web Technologies	AngularJS, jQuery, JavaScript, HTML, DHTML, XML, 
Cascading Style Sheets (CSS), XSLT.
XML Technologies	XML Schema, DTD, JAXP, SAX and DOM parsers.
IDEs / Tools
	Eclipse, NetBeans, Red Hat Developer Studio, RAD, WSAD. / TOAD, Maven, XmlSpy, Ant, PL/SQ L Developer, JUnit, iReport.
Operating Systems	Windows 95/98/NT/2000/XP, Sun Solaris 9/10, Red Hat Linux 9.
Design Patterns	MVC, DAO, DTO, Front Controller, Session Façade, Business Delegate, Observer, Singleton, View Helper, Decorator, Factory Pattern, POM, object pool
Databases and Tools	Oracle8 / 9i /10g,11g, HSQL, Sybase, MySQL, MSSQL, MongoDB, SQL Server, IBM DB2, Toad for SQL Server.
Frameworks	Struts, Spring (Dependency Injection, Spring Core, Spring MVC, Spring AOP, Spring DAO, Spring IOC, Spring JDBC, Spring with Hibernate), Hibernate, DWR, Log4j.
Web service specifications and Implementations	JAX-RPC, JAX-WS, JAX-RS, ESB, Axis, JWSDP, RESTful webservices.
Methodologies	Agile, Scrum, Test Driven Development.
Scripting/GUI Tools	HTML5, DHTML, DOJO, JSON, JavaScript, CSS3, Shell Script, Dreamweaver, MS FrontPage, VBScript, JSTL, JSP, NodeJS
Additional Skills	Elasticsearch, Logstash, Kibana, Graphana, Git, Bitbucket, Maven, Jenkins.

PROFESSIONAL EXPERIENCE:

WIND STREAM COMMUNICATION, DALLAS, TX                                                                SEP-2016 -TILL DATE
Role: Sr Java Programmer
Responsibilities:
• Involved in the application development using Java platform. Model View Control (MVC) structure implementation. 
• Responsible for providing the client-side JavaScript validations and usage of HTML, JavaScript, XML, JSP, CSS as per the requirements to enhance the Portal UI. 
• Used Spring Core for Dependency Injection. 
• Mapping of ORM objects to tables using the Hibernate as the persistence framework. 
• Involved in different service classes, used across the framework. 
• Implementation of Web Services using Axis for the integration of different systems 
• Developed applications using J2EE technologies like Spring Boot, Spring MVC on the business layer and the persistent layer using Hibernate as ORM tool. 
• Testing of Web Services using the Postman. 
• Used HTML, CSS, Spring MVC, JSP, and jQuery, JavaScript, Angular.js in the development and the designing the     UI. 
• Gradient effects through the development of the CSS style sheets. Developed navigation, icons and layouts. 
• Code review and configuration build management for the application using Maven. 
• Implementation of business logic, validation Frame Work using Spring Web flow and Spring MVC. 
• Implemented Web tier of the application through the usage of Spring MVC framework. 
• Implementation of clean separation of layers through the usage of different design patterns like Factory pattern, Singleton and DAO pattern. 
• Serialization in the flattening of the objects. 
• Used core java concepts like Collections while developing server-side services. 
• Data storage using DB2 and used PL/SQL for queries. 
• Worked with IBM Web Sphere Application Server Developer Tools for Eclipse by using lightweight set of tools to assemble, develop and deploy Java EE, Web 2.0, and mobile applications. 
• Involved with GUI using JSP, Java Script and HTML. 
• Involved in using continuous integration tool (CI/CD) Jenkins. Created builds using Maven and pulled the project code from GitHub repositories. 
• Experience with Garbage collection and multithreading. 
• Experience with Concurrency, Exception Handling, File handling
Environment: HTML, CSS, XML, SOAP, Hibernate, Java,J2EE,Java Script,MySQL DB, Spring Boot, PL/SQL, Log4j, JQuery, Angular JS, Eclipse, IBM Web Sphere Application server.
 
IBM DALLAS,TEXASSEP 2015–AUG 2016
Role: Sr Java Programmer
Responsibilities:
•	Involved in SDLC Requirements gathering, Analysis, Design, Development and Testing of application using AGILE methodology (SCRUM).
•	Designed APIs and analytics using IBM Cloud. Built mobile backend services, powerful app management, and insights into app usage using IBM mobile first.
•	Designed DOM based interactive to reprogram selected links and adopted WCAG 2.0 standards for HTML and XHTML and W3C standards for CSS as well.
•	Have achieved proficiency in Unit Test, Mock, Test Driven Development etc.
•	Implemented client-side Interface using React JS. Worked on Redux.
•	Design, develop and test HTML, CSS, jQuery and React.JS that meets accessibility and web browser standards for car dealerships websites. 
•	Installed, configured and Administered WebSphere Commerce Server 6.0 on Windows and Linux platform.
•	Involved in Stopping/Starting & Monitoring the logs for Application Server Instances.
•	Implemented Horizontal and Vertical Clustering, Performance tuning and troubleshooting of IBM WebSphere Application Server 6.0/6.1.
•	Installed EARs, WARs and configured application specific JVM settings, Web container parameters using the Admin Console and WSCP/WSadmin scripts.
•	Migrated existing applications from WebSphere V6.0 to V7.0.
•	Involved in issues like Application not responding. Application Deployment Errors, Wrong Database host name, Server Hung due to out of memory or thread hanging, Owner ship issue.
•	Created sites to organize client contracts and to summarize monthly financial data using React.js, Ember.js, D3.js and MySql.
•	Created web services and desktop applications to access and display data needed by support teams using, Ajax, JavaScript, jQuery, React.js, Angular.js, Node.js, Java, CSS and HTML.
•	Built data visualizations to monitor file server load, Web server speed, Data Processing using D3.js, jQuery and MySql.
•	Prepared exhaustive test cases to comprehensively test functionality and code.
•	Creating Java code and modifying the existing code to match with the front JavaScript files.
•	Created an on -the-fly configuration changes set up, with application saved in Node.js.

Environment: Java, JSP, Spring (MVC and Core), JSON, Servlets, Webservices(RESTful), Web Logic Application server, WebSphere Application Server 6.0/6.1/7.0, Websphere Portal Server 6.0/6.1, Websphere Commerce Server 6.0, Apache 2.0.47, IHS 6.0/6.1

ACADEMIC BANK KANSAS CITY,MO                                              AUG 2014 – AUG 2015
Role: Java Programmer
Responsibilities:
•	JSF Portal Framework at Presentation Tier and Faces Servlet acts as the Front Controller.
•	Actively participated and mentoring in requirements gathering, analysis, design, and development and testing phases.
•	Worked one-on-one with client to develop layout, color scheme for his website and implemented it into a final interface design with the HTML5/CSS3 & JavaScript using Dreamweaver. 
•	Developed CSS3 style sheets to give gradient effects. Developed page layouts, navigation and icons. Applied industry best practices and standards when project requirements were lagging.
•	Created Images, Logos and Icons that are used across the web pages using Adobe Flash and Photoshop.
•	Designed Frontend with in object oriented JavaScript framework like Angular.JS, Node.js and Ext.JS.
•	Used EXTJS for building rich internet applications, backbone JS & Require JS to optimize in-browser use and to load the module and to improve the Speed.
•	Working on all the latest technologies like HTML5, CSS3, etc. Tackled various issues related browser compatibility to accommodate these advanced and fast technologies
•	Troubleshoot Admin Server start-up issues, Java code defects after deployment, and class path issues by checking the JVM logs, plug-in logs and the Webserver logs
•	Worked closely with developers to define and configured application Servers, Virtual Hosts, Web Applications, Web resources, Servlets, JDBC drivers and Servlet Engines-as well as deployment of EJBs across multiple instances of WebSphere.
•	Maintained security, tuning and clustering on Web Sphere Application Server using IBM Web seal Tivoli Access Manager.
•	Monitored the logs for Application Server Instances.
•	Updated application code from JDK 1.3 to 1.4 using WSAD, RAD and redeployed in a clustered environment.
•	Design and develop solutions using C, C++, Multi-Threaded, Shell Scripting.
•	Debugged the application using Firebug to traverse the documents and manipulated the Nodes using DOM and DOM Functions using Firefox and IE Developer Tool bar for IE. 
•	Used JavaScript and XML to update a portion of a web page thus reducing bandwidth usage and load time and add modal dialog in web pages to get user input and requests.
•	Used Soap over Http and Soap over JMS for communication between components.
•	Worked with the team of architects and back-end Developers to gather requirements and enhance the application functionality and add new features. 
Environment:HTML5, CSS3, JavaScript, jQuery, DOM, DML, DHTML, EXT JS, Angular.js, Node.js, Backbone.js, Require.js, Adobe Flash, Photoshop, Dreamweaver, XML, Apache, SOAP, Internet Explorer, Firefox, Chrome, Oracle, Windows, C, C++, Agile Methodology.
VALUE LABS, HYDERABAD, INDIA                                                                                      JUNE 2012 – JULY2014
Role: Java Programmer


Responsibilities:
•	Utilized the base UML methodologies and Use cases modeled by architects to develop the front-end interface. The class, sequence and state diagrams were developed using Microsoft Visio.
•	Created User Interface (UI) to gather data and communicate with Business Layer by using Swing, HTML, JSP, JSP Tags Lib, JSTL and Java Script.
•	Utilized AJAX to increase web page’s interactivity, speed and functionality.
•	Implemented MVC architecture using Spring 2.5 MVC framework and enhanced the design using Stateless Session Beans for the Middle Tier Development
•	Utilized WSDL and SOAP to implement Web Services to optimize performance by using remote model applications.
•	Used JSF framework for implementing the Web tier of the application.
•	Designed and implemented complex multi-application flow through integration implemented using XML, XSL and JMS configurations.
•	Implemented Object-relation mapping in the persistence layer using hibernate frame work in conjunction with Spring Aspect Oriented Programming (AOP) functionality.
•	Used CVS as a documentation repository and version controlling tool.
•	Used ANT scripts for build creation and to push onto various environments.
•	Used JUnit 4.2 for extensive functional and unit testing code.
•	Used Log4j for logging and debugging.

Environment: Core Java, JDK 1.5, J2EE 5, HTML, CSS 2.1, JSP 2.1, JSF 1.2, JNDI, AJAX, Swing, Spring 2.5, Hibernate 3.0, JMS 1.1, SOAP UI, WSDL, UML, XML, XSLT, Windows XP, ANT, UNIX, Log4J, MVC Design Pattern, DAO, Eclipse IDE.

AJR INFOTECH, HYDERABAD, INDIA                                                                              AUG-2009 – JUNE-2012
Role: Java Developer 

Responsibilities: 

•	Worked on writing Java code for extracting backend data from the main frames.
•	Instantiated business objects with IOC pattern using spring framework and for Dependency Injection.
•	Implemented Object-relation mapping in the persistence layer using Hibernate frame work in conjunction with spring functionality.
•	Agile process is used for tracking and developing the application.
•	Development and Integration of the Application using Eclipse IDE and used StarTeam as Version Control Tool.
•	Implemented the integration with the back-end system with web services using Axis and SOAP
•	Utilized JUnit test cases for all the developed modules. 
•	Extensive experience in different IDEs like RAD, Eclipse, NetBeans.	

Environment: Java, J2EE, Spring Framework, HTML, JavaScript, Hibernate, Eclipse IDE, Star Team, Axis, SOAP, JUnit, RAD, Eclipse, NetBeans.
.




""")

for ent in resume.ents:
   print(ent.label_, ent.text)

ENV = 'dev'
   
app= Flask(__name__)

app.config['SECRET_KEY'] = 'super secret key'

app.config['MAIL_SERVER'] = 'smtp-relay.sendinblue.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mantvydas.luksas@gmail.com'
app.config['MAIL_PASSWORD'] = 'URG02hNB5pq4Zt7b'

mail = Mail(app)

e = URLSafeTimedSerializer(app.config['SECRET_KEY'])

if ENV == 'prod':
     app.debug = True
     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testing@localhost/postgres'
else:
     app.debug = False
     try:
        url = 'postgres://kdtfxcdxnpszrq:c8dccd8f82d7b2f33d7da031caaf9e791ded57472c9ef082c7870b5527cc7a6e@ec2-34-252-251-16.eu-west-1.compute.amazonaws.com:5432/da7ukihqat8bgm'
        url = url.split('postgres://')[1]
        engine = create_engine('postgresql+psycopg2://{}'.format(url), 
                           convert_unicode=True, encoding='utf8')
        db = scoped_session(sessionmaker(autocommit=False,
                                autoflush=False, bind=engine))
        
        models.Base.query = db.query_property()
     except:
        print('Something wrong with database url')
   

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/registration_landing')
def registration_landing():

    return render_template('registration_landing.html')

@app.route('/login/')
def login():

    if 'candidate' in session:
        return redirect(url_for('information'))
    elif 'employer' in session:
        return redirect(url_for('work_information'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():

    session.pop('candidate', None)
    session.pop('employer', None)
    session.pop('logged_in', None)

    session.clear()

    flash("You have been successfully logged out", "success")
    
    return redirect(url_for('login'))

@app.route('/', methods=['POST'])
def change():
    
        return render_template('index.html', user=session)

@app.route('/')
def index():

    #for token in doc:
      #  print(token.text)

    return render_template('index.html', user=session)

@app.route('/search')
def search():

    return render_template('search.html', user=session)

@app.route('/employers')
def employers():
    
    
    return render_template('employers.html', user=session)

@app.route('/choice')
def choice():

    return render_template('choice.html', user=session)

@app.route('/contact', methods=["POST", "GET"])
def contact():

    if request.method == "POST":

        subject = request.form["subject"]
        first_name = request.form["first"]
        last_name = request.form["last"]
        email = request.form["email"]
        phone = request.form["phone"]
        enquiry = request.form["message"]

        message = Message(subject, sender=email, recipients=["worknowapp88@gmail.com"])

        complete_message = "New Enquiry Received:\n\nName: \n" + first_name + " " + last_name + "\n\nEmail: \n" + email + "\n\nPhone: \n" + phone + "\n\nMessage: \n" + enquiry 

        message.html = complete_message

        mail.send(message)

        flash('Thank you, your message has been sent', 'form_feedback')
        return redirect(url_for('contact'))

    return render_template('contact.html', user=session)
@app.route('/employer_registration/')
def employer_registration():
    
    return render_template('employer_registration.html')

@app.route('/candidate_registration/')
def candidate_registration():
    
    return render_template('candidate_registration.html')

def send_reset_email_candidate(user):
    token = user.get_reset_token()

    message = Message('Password Reset for WorkNow', sender="noreply@work-now.herokuapp.com", recipients=[user.email])

    link = url_for('new_password_candidate', token=token, _external=True)

    message.html = render_template('forgot_email.html', link=link)
    mail.send(message)

def send_reset_email_employer(user):
    token = user.get_reset_token()

    message = Message('Password Reset for WorkNow', sender="noreply@work-now.herokuapp.com", recipients=[user.email])

    link = url_for('new_password_employer', token=token, _external=True)

    message.html = render_template('forgot_email.html', link=link)

    mail.send(message)
    
    
@app.route('/email_request/', methods=["POST", "GET"])
def email_request():

    flag = 0

    if 'logged_in' in session:
        return redirect(url_for("search"))

    if request.method == 'POST':
        forgot_email = request.form['forgot_email']
      
        try:
            
            candidate = models.Candidates.query.filter_by(email=forgot_email).first()
            send_reset_email_candidate(candidate)
            flash('An email has been sent to reset password', 'success')
            return redirect(url_for('login'))
        except:
            flag = 1
        try: 
            employer = models.Employers.query.filter_by(email=forgot_email).first()
            send_reset_email_employer(employer)
            flash('An email has been sent to reset password', 'success')
            return redirect(url_for('login'))

        except:
            flag = 1

    if flag == 1:

        flash("Invalid Email", "fail")
        return redirect(url_for('email_request'))

    return render_template('email_request.html')

@app.route('/new_password_candidate/<token>', methods=["POST", "GET"])
def new_password_candidate(token):

    if 'logged_in' in session:
        return redirect(url_for("search"))

    candidate = Candidates.verify_reset_token(token)

    if candidate is None: 
        flash("Invalid or expired token", "fail")
        return redirect(url_for('email_request'))

    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm']

        if password == confirm_password:
            candidate.password = sha256_crypt.encrypt(str(confirm_password))

            db.commit()
            flash('Your password has been updated', 'success')
            return redirect(url_for('login'))

        else:
            flash('Passwords do not match', 'fail')
            return render_template('new_password.html', token=token)
    
    return render_template('new_password.html', token=token)


@app.route('/new_password_employer/<token>', methods=["POST", "GET"])
def new_password_employer(token):

    if 'logged_in' in session:
        return redirect(url_for("search"))

    employer = models.Employers.verify_reset_token(token)

    if employer is None: 
        flash("Invalid or expired token", "fail")
        return redirect(url_for('email_request'))

    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm']

        if password == confirm_password:
            candidate.password = sha256_crypt.encrypt(str(confirm_password))

            db.commit()
            flash('Your password has been updated', 'success')
            return redirect(url_for('login'))

        else:
            flash('Passwords do not match', 'fail')
            return render_template('new_password.html', token=token)
    
    return render_template('new_password.html', token=token)

@app.route('/login_submit', methods=['GET', 'POST'])
def login_submit():

    if  request.method == 'POST':
            submitted_email = request.form['email']
            submitted_password = request.form['password']

            flag = 0

            try:
                    candidate = models.Candidates.query.filter_by(email=submitted_email).first()

                    password = candidate.password

                    first_name = candidate.firstname

                    last_name = candidate.lastname

                    profile = candidate.profile

                    email = candidate.email

                    phone = candidate.phone

                    if candidate.confirm_email == False:
                         
                         s = Serializer(app.config['SECRET_KEY'], 1800)

                         token = s.dumps({"email_id": email}).decode('utf-8')

                         message = Message("Confirm Email for WorkNow", sender="noreply@work-now.herokuapp.com", recipients=[email])

                         link =  url_for('confirm_email_candidate', email=email, token=token, _external=True)

                         message.html = render_template('confirm_email.html', link=link)

                         mail.send(message)

                         flash("Please Confirm Email", "fail")
                         return redirect(url_for('login'))

                    if sha256_crypt.verify(submitted_password, password):
                        
                        session.pop('candidate', None)

                        session.pop('last', None)

                        session['candidate'] = first_name

                        session['last'] = last_name

                        session['profile'] = profile

                        session['email'] = email

                        session['phone'] = phone

                        session['logged_in'] = True

                        return redirect(url_for('information'))
                    else:
                        flash("Invalid Password", "fail")
                        return redirect(url_for('login'))
            except:
                    flag = 1;

            try:
                   employer = models.Employers.query.filter_by(email=submitted_email).first() 

                   password = employer.password

                   company_name = employer.company

                   email = employer.email

                   phone = employer.phone
                   
                   profile = employer.profile

                   id = employer.employer_id

                   if employer.confirm_email == False:

                        s = Serializer(app.config['SECRET_KEY'], 1800)

                        token = s.dumps({"email_id": email}).decode('utf-8')

                        message = Message("Confirm Email for WorkNow", sender="noreply@work-now.herokuapp.com", recipients=[email])

                        link =  url_for('confirm_email_employer', email=email, token=token, _external=True)

                        message.html = render_template('confirm_email.html', link=link)

                        mail.send(message)
                        flash("Please confirm your email", "fail")
                        return redirect(url_for('login'))

                   if sha256_crypt.verify(submitted_password, password):

                       session.pop('employer', None)

                       session['employer'] = company_name

                       session['email'] = email

                       session['phone'] = phone

                       session['profile'] = profile 

                       session['id'] = id

                       session['logged_in'] = True

                       return redirect(url_for('work_information'))
                        
                   else:
                        flash("Invalid Password", "fail")
                        return redirect(url_for('login'))
            except:
                    flag = 1;

            if flag == 1:
                
                flash("User does not exist", "fail")
                return redirect(url_for('login'))

    return render_template('login.html')

def is_logged_in_candidate(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'candidate' in session:
            return f(*args, **kwargs)
        else:
            flash('Please login as a candidate account', 'fail')
            return redirect(url_for('login'))
    return wrap

def is_logged_in_employer(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'employer' in session:
            return f(*args, **kwargs)
        else:
            flash('Please login as an employer account', 'fail')
            return redirect(url_for('login'))
    return wrap

@app.route('/candidate_submit', methods=['GET', 'POST'])
def candidate_submit():

    if  request.method == 'POST':
            first_name = request.form['first']
            last_name = request.form['last']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']
            confirm = request.form['confirm']

            if password == confirm:
                stored_password = sha256_crypt.hash(str(password))

                data = models.Candidates(first_name, last_name, phone, email, stored_password)

                data.profile = "Please add your own description in account settings"

                s = Serializer(app.config['SECRET_KEY'], 1800)

                token = s.dumps({"email_id": email}).decode('utf-8')

                message = Message("Confirm Email for WorkNow", sender="noreply@work-now.herokuapp.com", recipients=[email])

                link =  url_for('confirm_email_candidate', email=email, token=token, _external=True)

                message.html = render_template('confirm_email.html', link=link)

                try:
                    db.add(data)
                    db.commit()
                    mail.send(message)
                except:
                    flash("User Already Exists", "fail")
                    return redirect(url_for('candidate_registration'))

                flash("Registered, email confirmation link sent", "success")
                return redirect(url_for('login'))
            else:
                flash("Error: Passwords don't match", "fail")
                return redirect(url_for('candidate_registration'))

@app.route('/confirm_email_candidate/<email>/<token>')
def confirm_email_candidate(email, token):

    

    try:

        s = Serializer(app.config['SECRET_KEY'], 1800)

        email_id = s.loads(token)['email_id']

        candidate = models.Candidates.query.filter_by(email=email_id).first()

        candidate.confirm_email = True

        db.commit()

        flash('Email confirmed', 'success')
        return redirect(url_for('login'))

    except:

         s = Serializer(app.config['SECRET_KEY'], 1800)

         new_token = s.dumps({"email_id": email}).decode('utf-8')
         message = Message("Confirm Email for WorkNow", sender="noreply@work-now.herokuapp.com", recipients=[email])

         link =  url_for('confirm_email_candidate', email=email, token=new_token, _external=True)

         message.html = render_template('confirm_email.html', link=link)
         
         mail.send(message)

         flash("Token is expired, check email for new one", "fail")
         return redirect(url_for('login'))

@app.route('/confirm_email_employer/<email>/<token>')
def confirm_email_employer(email, token):

    try:

        s = Serializer(app.config['SECRET_KEY'], 1800)

        email_id = s.loads(token)['email_id']

        employer = models.Employers.query.filter_by(email=email_id).first()

        employer.confirm_email = True

        db.commit()

        flash('Email confirmed', 'success')
        return redirect(url_for('login'))

    except:
        
         s = Serializer(app.config['SECRET_KEY'], 1800)

         new_token = s.dumps({"email_id": email}).decode('utf-8')

         message = Message("Confirm Email for WorkNow", sender="noreply@work-now.herokuapp.com", recipients=[email])

         link =  url_for('confirm_email_employer', email=email, token=new_token, _external=True)

         message.html = render_template('confirm_email.html', link=link)
                
         mail.send(message)

         flash("Token is expired, check email for new one", "fail")
         return redirect(url_for('login'))

@app.route('/delete_candidate/', methods=["POST", "GET"])
@is_logged_in_candidate
def delete_candidate():

    if request.method == 'POST':

        return redirect(url_for("confirm_delete_candidate"))
    return redirect(url_for('candidate_settings'))


@app.route('/confirm_delete_candidate/', methods=["POST", "GET"])
@is_logged_in_candidate
def confirm_delete_candidate():

    if request.method == 'POST':

        if request.form['confirm'] == 'Yes':
            candidate = models.Candidates.query.filter_by(email=session['email']).first()
            
            db.delete(candidate)
            db.commit()
            session.pop('candidate', None)
            session.pop('employer', None)
            session.pop('logged_in', None)

            session.clear()


            flash("Account has been deleted", "success")
            return redirect(url_for('login'))
        else:
            return redirect(url_for("candidate_settings"))
    return render_template('delete_landing_candidate.html')

@app.route('/delete_employer/', methods=["POST", "GET"])
@is_logged_in_employer
def delete_employer():

    if request.method == 'POST':

        return redirect(url_for("confirm_delete_employer"))
    return redirect(url_for('candidate_settings'))


@app.route('/confirm_delete_employer/', methods=["POST", "GET"])
@is_logged_in_employer
def confirm_delete_employer():

    if request.method == 'POST':

        if request.form['confirm'] == 'Yes':
            employer = models.Employers.query.filter_by(email=session['email']).first()
            
            db.delete(employer)
            db.commit()
            
            session.pop('candidate', None)
            session.pop('employer', None)
            session.pop('logged_in', None)

            session.clear()

            flash("Account has been deleted", "success")
            return redirect(url_for('login'))
        else:
            return redirect(url_for("employer_settings"))
    return render_template('delete_landing_employer.html')

@app.route('/candidate_result/')
@is_logged_in_employer
def candidate_result():

    employer = models.Employers.query.filter_by(email=session["email"]).first()
    image_file = url_for('static', filename='profile_pics/' + employer.image_file)

    return render_template('candidate_result.html', user=session, image_file=image_file)


@app.route('/adverts/')
@is_logged_in_employer
def adverts():

    employer = models.Employers.query.filter_by(email=session["email"]).first()

    image_file = url_for('static', filename='profile_pics/' + employer.image_file)

    adverts = models.Adverts.query.filter_by(employer_id=employer.employer_id).all()

    return render_template('adverts.html', user=session, image_file=image_file, adverts=adverts)

def save_picture(form_picture):

    random_hex = secrets.token_hex(8)

    _, f_ext = os.path.splitext(form_picture.filename)

    image_fn = random_hex + f_ext

    picture_path = os.path.join(app.root_path, 'static/profile_pics', image_fn)

    form_picture.save(picture_path)

    return image_fn

def save_resume(form_resume):

    random_hex = secrets.token_hex(8)

    _, f_ext = os.path.splitext(form_resume.filename)

    resume_fn = random_hex + f_ext

    resume_path = os.path.join(app.root_path, 'static/resumes', resume_fn)

    form_resume.save(resume_path)

    return resume_fn

@app.route('/employer_settings/', methods=['GET', 'POST'])
@is_logged_in_employer
def employer_settings():

    employer = models.Employers.query.filter_by(email=session["email"]).first()

    form = ImageForm()

    if form.validate_on_submit():
       if form.picture.data:

          picture_file = save_picture(form.picture.data)
            
          employer = models.Employers.query.filter_by(email=session["email"]).first()

          employer.image_file = picture_file

          db.commit()

          session.pop("picture", None)

          session["picture"] = picture_file

          flash("Picture Updated", "success")
          return redirect(url_for('employer_settings'))
    
    image_file = url_for('static', filename='profile_pics/' + employer.image_file)
    return render_template('employer_settings.html', user=session, form=form, image_file=image_file)

@app.route('/upload_password/', methods=['GET', 'POST'])
def upload_password():

    if request.method == 'POST':

        try:

            candidate = models.Candidates.query.filter_by(email=session['email']).first()

            password = request.form['password']

            candidate.password = sha256_crypt.encrypt(str(password))

            db.commit()

            flash("Successfully changed password", "success")
            return redirect(url_for('candidate_settings'))

        except:
            
            pass

        try:

            employer = models.Employers.query.filter_by(email=session['email']).first()

            password = request.form['password']

            employer.password = sha256_crypt.encrypt(str(password))

            db.commit()

            flash("Successfully changed password", "success")
            return redirect(url_for('employer_settings'))

        except:

            pass

    return render_template('login.html')

@app.route('/upload_description/', methods=['GET', 'POST'])
def upload_description():

    if request.method == 'POST':

        try:

            candidate = models.Candidates.query.filter_by(email=session['email']).first()

            new_description = request.form['description']

            candidate.profile = new_description

            db.commit()

            session.pop('profile', None)

            session['profile'] = new_description 

            flash("Successfully saved your job description", "success")
            return redirect(url_for('candidate_settings'))

        except:
            
            pass

        try:

            employer = models.Employers.query.filter_by(email=session['email']).first()

            new_description = request.form['description']

            employer.profile = new_description

            db.commit()

            session['profile'] = new_description 

            flash("Successfully saved your job description", "success")
            return redirect(url_for('employer_settings'))

        except:

            pass

    return render_template('login.html')

@app.route('/post_job/', methods=['GET', 'POST'])
@is_logged_in_employer
def post_job():

    employer = models.Employers.query.filter_by(email=session["email"]).first()
    image_file = url_for('static', filename='profile_pics/' + employer.image_file)

    form = InterviewForm()

    if form.validate_on_submit():

        salary = request.form['salary']
        position = request.form['position']
        experience = request.form['experience']
        candidatesNumber = request.form['candidatesNumber']
        description = request.form['description']
        interview_date = form.entryDate.data
        interview_time = form.entryTime.data
        location = request.form['location']

        job = position.lower()
        
        employer = models.Employers.query.filter_by(email=session['email']).first()

        id = int(employer.employer_id)       

        advert = models.Adverts(salary, job, experience, location, description, candidatesNumber, interview_date, interview_time, id)

        db.add(advert)

        db.commit()

        experience_years = str(experience) + " years"

        text_to_be_analyzed = str(position) + " " + experience_years + " " + str(description)

        job = models.Jobs(text_to_be_analyzed)

        db.add(job)

        db.commit()

        flash("Advert successfully added to your current adverts", "success")
        return redirect(url_for('post_job'))

    return render_template('post_job.html', user=session, image_file=image_file, form=form)

@app.route('/search_results', methods=['GET', 'POST'])
def search_results():

    if request.method == 'POST' or request.method == 'GET':
       
       try:

            location_query = request.form['category']

       except: 
           flash("Please select a location", "result_feedback")
           return redirect(url_for('search'))

       try: 
           query = request.form['search_query']
           if query == "Search Job Position":
                query = None
           
       except:
           query = None

       if location_query == "Any" and query == None:

           adverts = models.Adverts.query.all()
           
       elif location_query == "Any" and query != None:

           print("here")
           adverts = models.Adverts.query.filter(Adverts.position.contains(query)).all()
       
       elif location_query != "Any" and query == None:

           adverts = models.Adverts.query.filter_by(location=location_query).all()

       elif location_query != "Any" and query != None:
           
           adverts = models.Adverts.query.filter(Adverts.location.contains(location_query), Adverts.position.contains(query)).all()
      
       employers = []

       if not adverts:
           flash("No results found", "result_feedback")
           return redirect(url_for('search'))
       else:

           image_dictionary = {}

           image_dictionary.clear()
            
           for advert in adverts:

               employer = models.Employers.query.filter_by(employer_id=advert.employer_id).first()

               image_dictionary[advert.employer_id] = employer.image_file

           return render_template('search_results.html', user=session, adverts=adverts, employers=employers, images=image_dictionary)

   
@app.route('/job_apply', methods=['GET', 'POST'])
@is_logged_in_candidate
def job_apply():

    id = request.form['advert_id']

    advert = models.Adverts.query.filter_by(advert_id=id).first()

    employer = models.Employers.query.filter_by(employer_id=advert.employer_id).first()

    image_file = employer.image_file

    return render_template('job_apply.html', user=session, advert=advert, employer=employer, image_file=image_file)

@app.route('/candidate_settings/', methods=['GET', 'POST'])
@is_logged_in_candidate
def candidate_settings():

    candidate = models.Candidates.query.filter_by(email=session["email"]).first()

    form = ImageForm()

    resumeForm = ResumeForm()

    if form.validate_on_submit():
       if form.picture.data:

          picture_file = save_picture(form.picture.data)
            
          candidate = models.Candidates.query.filter_by(email=session["email"]).first()

          candidate.image_file = picture_file

          db.commit()

          flash('Picture updated', 'success')
          return redirect(url_for('candidate_settings'))

    if resumeForm.validate_on_submit():
       if resumeForm.resume.data:

          resume_file = save_resume(resumeForm.resume.data)
            
          candidate = models.Candidates.query.filter_by(email=session["email"]).first()

          candidate.resume = resume_file

          db.commit()

          flash('Resume updated', 'success')

          return redirect(url_for('candidate_settings'))
   
    image_file = url_for('static', filename='profile_pics/' + candidate.image_file)

    return render_template('candidate_settings.html', user=session, form=form, resumeForm=resumeForm, image_file=image_file)

@app.route('/upload_resume/', methods=['GET', 'POST'])
@is_logged_in_candidate
def upload_resume():

    form = ResumeForm()

    if form.validate_on_submit():
       if form.resume.data:

          resume_file = save_resume(form.resume.data)
            
          candidate = models.Candidates.query.filter_by(email=session["email"]).first()

          candidate.resume_file = resume_file

          db.commit()

          flash('Resume updated', 'success')
          return redirect(url_for('candidate_settings'))
   

@app.route('/submissions/')
@is_logged_in_candidate
def submissions():

    candidate = models.Candidates.query.filter_by(email=session["email"]).first()
    image_file = url_for('static', filename='profile_pics/' + candidate.image_file)

    return render_template('submissions.html', user=session, image_file=image_file)

@app.route('/employer_information', methods=["POST", "GET"])
@is_logged_in_candidate
def employer_information():

    if request.method == "POST":

        id = request.form["advert_id"]

        advert = models.Adverts.query.filter_by(advert_id=id).first()
        
        employer = models.Employers.query.filter_by(employer_id=advert.employer_id).first()

        image_file = employer.image_file

        return render_template('employer_information.html', user=session, advert=advert, employer=employer, image_file=image_file)

@app.route('/candidate_apply', methods=["POST", "GET"])
@is_logged_in_candidate
def candidate_apply():

    if request.method == 'POST':

        advert_id = request.form["advert_id"]

        candidate = models.Candidates.query.filter_by(email=session["email"]).first()

        job = models.Jobs.query.filter_by(job_id=advert_id)

        if(candidate.resume == None):
            flash("Please upload your resume", "result_feedback")
            return redirect(url_for('search'))

        #submission = Submission()

        flash("You have successfully applied", "result_feedback")
        return redirect(url_for('search'))

    else:
        return redirect(url_for('search'))

@app.route('/employer_submit', methods=['GET', 'POST'])
def employer_submit():

    if  request.method == 'POST':
    
            email = request.form['email']
            company = request.form['company']
            phone = request.form['phone']
            password = request.form['password']
            confirm = request.form['confirm']

            format_company = company.upper()

            if password == confirm:
                stored_password = sha256_crypt.encrypt(str(password))

                data = models.Employers(email, format_company, phone, stored_password)

                token = e.dumps(email, salt='email-confirm')

                message = Message("Confirm Email for WorkNow", sender="noreply@work-now.herokuapp.com", recipients=[email])

                link =  {url_for('confirm_email_employer', email=email, token=token, _external=True)}

                message.html = render_template('confirm_email.html', link=link)

                try:
                    db.add(data)
                    db.commit()
                    mail.send(message)
                   
                except:
                    flash("Employer Already Exists", "fail")
                    return redirect(url_for('employer_registration'))

                flash("Registered, email confirmation link sent", "success")
                return redirect(url_for('login'))
            else:
                flash("Error: Passwords don't match", "fail")
                return redirect(url_for('employer_registration'))

@app.route('/password_request/', methods=['GET', 'POST'])
def password_submit():

    if  request.method == 'POST':
            email = request.form['email']
            
            if password == confirm:
                stored_password = sha256_crypt.encrypt(str(password))
                flash("Thank you for registering", "success")
                return redirect(url_for('login'))
            else:
                flash("Error: Passwords don't match", "fail")
                return redirect(url_for('candidate_registration'))

@app.route('/information/')
@is_logged_in_candidate
def information():

   candidate = models.Candidates.query.filter_by(email=session["email"]).first()
   image_file = url_for('static', filename='profile_pics/' + candidate.image_file)

   if candidate.resume != None:

        resume_file = url_for('static', filename='resumes/' + candidate.resume)
        return render_template('information.html', user=session, image_file=image_file, resume_file=resume_file)
   else: 
        return render_template('information.html', user=session, image_file=image_file)

@app.route('/work_information/')
@is_logged_in_employer
def work_information():
    employer = models.Employers.query.filter_by(email=session["email"]).first()
    image_file = url_for('static', filename='profile_pics/' + employer.image_file)

    return render_template('work_information.html', user=session, image_file = image_file)

if __name__ == '__main__':
    models.Base.metadata.create_all(bind=engine)
    app.run()

    