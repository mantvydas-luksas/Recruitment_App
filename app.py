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
from tqdm import tqdm
import spacy
import en_core_web_sm
from spacy.tokens import Doc
from spacy.training import Example
from spacy.util import minibatch, compounding
from spacy.training import Example
from spacy.scorer import Scorer
from spacy.tokens import DocBin
import secrets
import os
import json
import time
import random
import models
import forms
from pathlib import Path
from functools import wraps

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

software_resumes = en_core_web_sm.load()

ner = software_resumes.get_pipe("ner")

TRAIN_SOFTWARE_RESUME_DATA = [("Name: Abiral Pandey\nEmail: abiral.pandey88@gmail.com\nPhone: 940-242-3303\nCurrent Location: Woonsocket, Rhode Island\nVisa Status: US Citizen\n\nSUMMARY:\n•\tDynamic individual with 6 years of software development experience in design, development, deployment, maintenance, production and support of web - based and Client-Server business applications using OOP and Java/J2EE technologies.\n•\tExposure to all phases of Software Development Life Cycle(SDLC) using Agile, RUP, Waterfall.\n•\tDesigned and developed web UI screen using Angular-JS.\n•\tDeveloped AngularJS Controllers, Services, filters and directives for various modules in the application.\n•\tKnowledge on ETL tools like Kettle Pentaho and Microsoft SSIS tools.\n•\tCreated custom directives, decorators and services using AngularJS to interface with both RESTful and legacy network services also DOM applications.\n•\tExperience with MVC frameworks like Struts, SPRING and ORM tools like Hibernate.\n•\tExperienced in working with batch jobs using Spring-Batch, Autosys and Quartz.\n•\tWorked extensively with XML related technologies like XML/XSLT to process, validate, parse and extract data from XML using DOM and SAX parsers for DTD and SCHEMAand also worked with JAX-B.\n•\tStrong experience in J2EE technologies like Java Beans, Servlets, JSP (including custom tags), JSTL, JDBC, Struts, Spring, JMS, JNDI and Multithreading.\n•\tExpertise in web development technologies like HTML, DHTML, XHTML, CSS, Java Script, JQuery, JSF, AJAX, Bootstrap JS, Node JS and Angular JS.\n•\tExperienced in RESTful web services using JAX-RS, Jersey framework and SOAP using JAX-WS, Axis-2 framework.\n•\tExpert knowledge over J2EE Design Patterns like MVC, Adapter, Front End Controller, Value object, Singleton, Session Facade, Business Delegate, Factory DAO in designing the architecture of large applications.\n•\tExperience in using Maven and Ant build scripts for the project build automation.\n•\tExperience in using version control and configuration management tools like SVN, Clear Case and CVS.\n•\tExpertise in working with various Application Servers such as IBM WebSphere, JBoss, Glassfish, Oracle WebLogic and Apache Tomcat server.\n•\tGood knowledge in using ’s such as Eclipse, NetBeans, JBuilder, RAD and STS.\n•\tExpertise in working with Relational databases such as Oracle, PostgreSQL, DB2, MySQL and NoSQL database MongoDB.\n•\tExperience in database design using PL/SQL to write Stored Procedures, Functions, Triggers, views and good at writing complex queries for Oracle 10g/11g.\n•\tGood experience in developing test cases with JUnit for Unit testing, Load testing and logging using Log4J.\n•\tExperienced in using Operating Systems like Windows 98 / 2000 / NT / XP, AIX, Sun Solaris.\n•\tProficient in software documentation and technical report writing.\n•\tInvolved in Performance analysis and improvements of the application using tools like Jmeter and using commands on Unix box to resolve deadlocks and improve performance.\n\nTECHNICAL SKILLS:\nProgramming Languages: Java/J2EE, PL/SQL, Unix Shell Scripts\nJava/J2EE Technologies: JavaBeans, collections, Servlets, JSP, JDBC, JNDI, RMI, EJB\nFrameworks: Struts 1.x/2.x, Spring 2.5/3.0, Web Framework, JSF, Hibernate, iBatis, JPA, Axis-2, Jersey\nMethodologies/Design Patterns: OOAD, OOP, UML, MVC, Singleton, DTO Pattern, DAO Pattern, Service Fa ade, Factory Pattern\nBuild Automation: Jenkins, Maven, Ant\nApplication/Web Servers: IBM Web Sphere 6.x/5.x, BEA Web Logic 8.1/9.1, Apache Tomcat 5.x/6.x, JBOSS 4.x/3.x\nXML processing: DTD, Schema, JAX-P (DOM, SAX), JAX-B\nWeb Services: RESTful, SOAP\nWeb Development: HTML, DHTML, XHTML, CSS, Java Script, JQuery, AJAX, LADP, JSF, Bootstrap JS, Node JS, Angular JS\nVersion Control Tools: CVS, Harvest, IBM Clear case, SVN and GIT\nDatabases: Oracle 9i/10g/11g, IBM DB2, SQL Server 2005/2008, PostgreSQL, MySQL, MangoDB\nMessaging Techologies: JMS, IBM MQ\nIDE s: Eclipse, NetBeans, RAD, WSAD\nTesting and Logging Frameworks: Junit, Log4j, Mockito, Finesse Tests\nReporting Tools: Crystal Reports 11, Jasper Reports\nTools: Rational Rose, MS Visio, XML Spy, TOAD\nOperating Systems: Windows 98/2000/NT/XP, AIX, Sun Solaris, HP-UX\nPROFESSIONAL EXPERIENCE:\n\nCVS, Woonsocket, Rhode Island                                 Full Stack Java Developer\nApril 2016 – Present\nResponsibilities:\n•\tInvolved in various stages of Software Development Life Cycle (SDLC) deliverables of the project using the Agile methodology.\n•\tUsed AWS Cloud platform and its features which include EBS, AMI, SNS, RDS, EBS, Cloud Watch, Cloud Trail, Cloud Formation, Cloud Front, S3, and Route53. \n•\tExpertise in building rich, interactive user interfaces using HTML, CSS, JavaScript, jQuery, Node.Js and Angular.Js.\n•\tGathered and clarified requirements with business analyst to feed into high-level customization design, development and installation phases.\n•\tUsed Spring Framework for dependency injection for Action classes using Application Context XML file. \n•\tInvolved in implementation of MVC pattern using JSP and Spring Controller.\n•\tDeveloped business objects using Spring IOC, Spring MVC and Spring AOP. Implemented MVC architecture using JSP Spring, Hibernate and used Spring Framework to initialize managed beans and services.\n•\tImplemented SOA architecture with Web Services using SOAP, JAX-WS, WSDL, UDDI and XML.\n•\tUsed Collections for Model classes in the DAO layer (Data Access Object) Involved in modifying some changes in DAO layer using Hibernate.\n•\tCreated mappings among the relations and written SQL queries using Hibernate.\n•\tImplemented Concurrency, Exception Handling and Collections whenever necessary.\n•\tUsed Entity Beans to persist the data into IBM DB2 database like database access components, Creating Schemas and Tables.\n•\tUsed SQL to perform data mapping and backend testing, also documented all the SQL queries for future testing purpose.\n•\tCreated process flow for deploying application in Web Sphere application server.\n•\tManaged build, reporting and documentation from the project information using Jenkins, Maven Tool and SVN for version control.\n•\tUsed Jenkins for Continuous Integration.\n•\tUsed JUnit for testing and used JIRA for tracking bugs.\n•\tResponsible for the dealing with the problem, bug fixing and troubleshooting.\n Environment: Java, J2EE, HTML, CSS, JavaScript, jQuery, Ajax, Spring, Spring IOC, Spring AOP, Spring MVC, Hibernate, REST, SOAP, XML, Eclipse, PL/SQL, JUnit, Maven Build Tool, DB2, JIRA, Jenkins, SVN and IBM Web Sphere, AngularJS, EBS, AMI, SNS, RDS, Cloud Watch, Cloud Trail, Cloud Formation, Auto scaling\n\nToll Brothers, Horsham Township, Pennsylvania                  Software Engineer\nDecember 2015 -  March 2016\nResponsibilities:\n•\tDeveloped JSP and extensively used tag libraries. \n•\tDesigned the system with OOAD methodology using various design patterns like factory method, Singleton, Adaptor, Template etc. \n•\tImplementing and planning the server-side architecture using Spring and Hibernate \n•\tConfigured the spring framework for entire business logic layer with XML bean configuration files. \n•\tPreparation of Low Level Designing and High Level Designing and relevant documentation. \n•\tExtensively used Spring IOC for Dependency Injection and worked on Custom MVC Frameworks loosely based on Struts \n•\texperienced in build tools like Micro services, Ant, Maven and Gradle tools.\n•\tWrote Controller classes in Spring MVC framework in the web layer. \n•\tProduced the shopping cart on the client Front-end using jQuery, JavaScript, HTML5, CSS3. \n•\tExtensively used Eclipse based STS IDE for building, developing and integrating the application. \n•\tUsed Table per hierarchy inheritance of hibernates and mapped polymorphic associations. \n•\tDeveloped one-much, many-one, one-one annotation based mappings in Hibernate. \n•\tWrote queries Using Cassandra CQL to create, alter, insert and delete elements. \n•\tDeveloped DAO service methods to populate the domain model objects using hibernate. \n•\tUsed java collections API extensively such as Lists, Sets and Maps.  \n•\tWrote DAO classes using spring and Hibernate to interact with database for persistence. \n•\tDeveloped components of web services (JAX-WS, JAX-RPC) end to end, using different JAX-WS standards with clear understanding on WSDL, SOAP using various message patterns  \n•\tPerformed on e-Commerce by using JSF framework and JavaScript, jQuery, HTML5 pages\n•\tWrote and tested Java Beans to retrieve trading data and subscriber's information from MySQL database server,\n•\t Extensive experience in Angular.JS for application implementation, proficient in creating modules, controllers, route-Providers, factory services, ng-repeat, customizable filter, http get/post methods and directives to realize functionalities like REST service with Ajax call , input validations, searchable and sortable contents.  \n•\tImplemented Unit and Integration test cases with JUnit Framework based on Functional Flow. \n•\tUsed tools like My Eclipse IDE, configured and deployed the applications onto Web Logic application server \n•\tConfigured Log4j for logging and debugging \n Environment: Eclipse, Java J2EE, HTML, JSP, JAX RPC, JAXB, CSS3, JavaScript, and jQuery, Spring MVC, Hibernate, RESTful web services, Apache Tomcat7.0, Cucumber, Cassandra, Junit, Jenkins, Maven, GitHub, XML, Log4j, EJB, MySQL, Ajax.\n\nDairy Farmers of America, Kansas City, Missouri                      Java Developer\nNovember 2014 – December 2015\nResponsibilities:\n•\tResponsible for developing use cases, class and sequence diagram for the modules using UML and Rational Rose.\n•\tIdentifying and design of common interfaces across multiple systems or modules of social insurance.\n•\tDeveloped the application using Spring Framework that leverages classical Model View Layer (MVC) architecture. UML diagrams like use cases, class diagrams, interaction diagrams (sequence and collaboration) and activity diagrams were used.\n•\tDeveloped J2EE modules using XMI and CORE JAVA.\n•\tInteraction with Business users for user and system acceptance testing.\n•\tValidated the data against the business rules.\n•\tData access layer is implemented using Hibernate.\n•\tUsed Apache POI to generate Excel documents\n•\tImplemented Struts action classes.\n•\tUsed Spring Security for Authentication and authorization extensively.\n•\tUtilized Eclipse to create JSPs/Servlets/Hibernate that pulled information from a Oracle database and sent to a front end GUI for end users.\n•\tUsed JDBC for Oracle database connection and written number of stored procedures for retrieving the data.\n•\tDeveloped modules for validating the data according to business rules and used Castor to convert data into array of XML strings and XSLT for transformation.\n•\tUsed Hibernate for data persistence.\n•\tDeveloped SOAP based HTTP requests for communicating with Web Services.\n•\tWas involved in the design of multi-tier architecture using EJB, Servlets and JSP.\n•\tUsed Spring Dependency Injection properties to provide loose-coupling between layers.\n•\tCollaborated with Web designers to create the JSP pages, applying HTML, JavaScript, JQuery and Struts Tags.\n•\tExtensively worked on debugging using Logging Frameworks such as Apache Log4j.\n•\tCreated test plans for unit testing to validate component functionality.\nEnvironment: Java 1.4.2, J2EE, Servlets, MVC, Web services, Struts, Spring - Core, MVC, Security, Eclipse, Hibernate, XML, XSLT, EJB, JSP, JDBC, JAX-B, JQuery, JavaScript, HTML, Log4j, Oracle 10g, Apache POI, Caster, XMI.\n\nBank of Utah, Ogden, Utah                                                           J2EE Developer\nMay 2013 – October 2014\n\nResponsibilities:\n•\tDesigned and developed Servlets and JSP, which presents the end user with form to submit the details of the problem.\n•\tCreated SQL statements and triggers for the effective retrieval and storage of data from the database.\n•\tPerformed JUnit testing, proposed and implemented performance enhancements, worked with Oracle databases, running SQL scripts and stored procedures.\n•\tDeveloped Restful based Web Services.\n•\tWas involved in the design of multi-tier architecture using EJB, Servlets and JSP.\n•\tDeveloped Servlets used to store user information in the database, which makes a JDBC-ODBC connection to the database and inserts the details into to the database.\n•\tDesigned and developed a Servlet, which presents the engineer a form to submit solution to particular problem.\n•\tSetting up test environments and configuring various components of the application using JDBC API to establish a connection with oracle database and configuring.\n•\tDesigned and developed a Servlet, which allows the end user to query on the problem, makes a JDBC-ODBC connection to the database and retrieve the details regarding the call number and the status of the submitted problem.\nEnvironment: Java, J2EE, Servlets, JSP, EJB, Custom tags, JDBC, JUNIT, Restful, Data Source, DAO, VO Patterns, Tomcat 5.0, SQL, Oracle 9i, Linux.\n\n\nEpsilon, Irving, Texas                                                         Junior Java Developer\nJanuary 2012 – April 2013\nResponsibilities:\n•\tDesigned the user interfaces using JSP.\n•\tDeveloped Custom tags, JSTL to support custom User Interfaces.\n•\tDeveloped the application using Struts (MVC) Framework.\n•\tImplemented Business processes such as user authentication, Account Transfer using Session EJBs.\n•\tUsed Eclipse to writing the code for JSP, Servlets, Struts and EJBs.\n•\tDeployed the applications on Web Logic Application Server.\n•\tUsed Java Messaging Services (JMS) and Backend messaging for reliable and asynchronous exchange of important information such as payment status report.\n•\tDeveloped the Ant scripts for preparing WAR files used to deploy J2EE components.\n•\tUsed JDBC for database connectivity to Oracle.\n•\tWorked with Oracle Database to create tables, procedures, functions and select statements.\n•\tUsed JUnit Testing, debugging and bug fixing.\n•\tUsed Log4J to capture the log that includes runtime exceptions and developed WAR framework to alert the client and production support in case of application failures.\n•\tWorked in Rational Unified Process (RUP) Methodology.\nEnvironment: Java, J2EE, JSP, JSTL, JDBC, Struts, EJB, JMS, Oracle, HTML, XML, Web Logic, Ant, CVS, Log4J, JUnit, JMS, PL/SQL, JavaScript, Eclipse IDE, UNIX Shell Scripting, Rational Unified Process (RUP).\nEducation: \nBachelor of Computer Science – University of North Texas, Denton, Texas", {'entities': [(176, 218, 'YEARS'), (222, 382, 'RESPONSIBILITIES'), (386, 477, 'RESPONSIBILITIES'), (481, 534, 'RESPONSIBILITIES'), (538, 642, 'RESPONSIBILITIES'), (674, 688, 'SKILLS'), (693, 713, 'SKILLS'), (848, 864, 'SKILLS'), (884, 898, 'SKILLS'), (912, 918, 'SKILLS'), (923, 932, 'SKILLS'), (996, 1008, 'SKILLS'), (1010, 1017, 'SKILLS'), (1022, 1028, 'SKILLS'), (1056, 1080, 'SKILLS'), (1318, 1322, 'SKILLS'), (1431, 1436, 'SKILLS'), (1438, 1443, 'SKILLS'), (1450, 1461, 'SKILLS'), (1476, 1480, 'SKILLS'), (1496, 1503, 'SKILLS'), (1508, 1518, 'SKILLS'), (1482, 1494, 'SKILLS'), (1776, 1787, 'SKILLS'), (1873, 1876, 'SKILLS'), (1967, 1997, 'SKILLS'), (2213, 2221, 'SKILLS'), (2223, 2231, 'SKILLS'), (2233, 2236, 'SKILLS'), (2241, 2244, 'SKILLS'), (2311, 2321, 'SKILLS'), (2338, 2343, 'SKILLS'), (2353, 2360, 'SKILLS'), (2576, 2588, 'SKILLS'), (2590, 2602, 'SKILLS'), (2651, 2668, 'SKILLS'), (2737, 2759, 'SKILLS'), (2764, 2788, 'SKILLS'), (3601, 3606, 'SKILLS'), (3608, 3613, 'SKILLS'), (3620, 3631, 'SKILLS'), (3641, 3645, 'SKILLS'), (3672, 3679, 'SKILLS'), (3681, 3691, 'SKILLS'), (3658, 3670, 'SKILLS'), (3384, 3387, 'SKILLS'), (3066, 3075, 'SKILLS'), (3818, 3828, 'SKILLS'), (3880, 3883, 'SKILLS'), (3896, 3904, 'SKILLS'), (3906, 3909, 'SKILLS'), (4083, 4100, 'SKILLS'), (4304, 4428, 'RESPONSIBILITIES'), (4432, 4583, 'RESPONSIBILITIES'), (4588, 4685, 'RESPONSIBILITIES'), (4707, 4846, 'RESPONSIBILITIES'), (4850, 4950, 'RESPONSIBILITIES'), (4955, 5028, 'RESPONSIBILITIES'), (5032, 5102, 'RESPONSIBILITIES'), (5104, 5227, 'RESPONSIBILITIES'), (5231, 5316, 'RESPONSIBILITIES'), (5320, 5456, 'RESPONSIBILITIES'), (5460, 5536, 'RESPONSIBILITIES'), (5540, 5618, 'RESPONSIBILITIES'), (5622, 5742, 'RESPONSIBILITIES'), (5746, 5862, 'RESPONSIBILITIES'), (5866, 5945, 'RESPONSIBILITIES'), (5949, 6074, 'RESPONSIBILITIES'), (6078, 6117, 'RESPONSIBILITIES'), (6121, 6175, 'RESPONSIBILITIES'), (6179, 6255, 'RESPONSIBILITIES'), (6748, 6873, 'RESPONSIBILITIES'), (6878, 6959, 'RESPONSIBILITIES'), (6963, 7060, 'RESPONSIBILITIES'), (7065, 7151, 'RESPONSIBILITIES'), (7320, 7323, 'SKILLS'), (7549, 7552, 'SKILLS'), (7545, 7548, 'SKILLS'), (7869, 7951, 'RESPONSIBILITIES'), (7956, 8022, 'RESPONSIBILITIES'), (8028, 8114, 'RESPONSIBILITIES'), (8119, 8288, 'RESPONSIBILITIES'), (8293, 8375, 'RESPONSIBILITIES'), (8378, 8486, 'RESPONSIBILITIES'), (8491, 8522, 'RESPONSIBILITIES'), (8523, 8820, 'RESPONSIBILITIES'), (8947, 8950, 'SKILLS'), (9460, 9552, 'RESPONSIBILITIES'), (9556, 9654, 'RESPONSIBILITIES'), (9899, 9945, 'RESPONSIBILITIES'), (9949, 10019, 'RESPONSIBILITIES'), (10023, 10068, 'RESPONSIBILITIES'), (10072, 10120, 'RESPONSIBILITIES'), (10124, 10167, 'RESPONSIBILITIES'), (10170, 10203, 'RESPONSIBILITIES'), (10207, 10276, 'RESPONSIBILITIES'), (10280, 10419, 'RESPONSIBILITIES'), (10423, 10527, 'RESPONSIBILITIES'), (10531, 10686, 'RESPONSIBILITIES'), (10690, 10725, 'RESPONSIBILITIES'), (10729, 10799, 'RESPONSIBILITIES'), (10803, 10884, 'RESPONSIBILITIES'), (10888, 10972, 'RESPONSIBILITIES'), (10976, 11082, 'RESPONSIBILITIES'), (11086, 11163, 'RESPONSIBILITIES'), (11167, 11238, 'RESPONSIBILITIES'), (12022, 12103, 'RESPONSIBILITIES'), (12107, 12269, 'RESPONSIBILITIES'), (12273, 12382, 'RESPONSIBILITIES'), (12386, 12546, 'RESPONSIBILITIES'), (13067, 13105, 'RESPONSIBILITIES'), (13132, 13136, 'SKILLS'), (13232, 13327, 'RESPONSIBILITIES'), (13402, 13459, 'RESPONSIBILITIES'), (13463, 13613, 'RESPONSIBILITIES'), (13631, 13634, 'SKILLS'), (13891, 14056, 'RESPONSIBILITIES'), (14144, 14148, 'SKILLS'), (14204, 14207, 'SKILLS'), (14261, 14264, 'SKILLS'), (14320, 14360, 'EDUCATION')]})]

TEST_SOFTWARE_RESUME_DATA = [("Name: Abiral Pandey\nEmail: abiral.pandey88@gmail.com\nPhone: 940-242-3303\nCurrent Location: Woonsocket, Rhode Island\nVisa Status: US Citizen\n\nSUMMARY:\n•\tDynamic individual with 6 years of software development experience in design, development, deployment, maintenance, production and support of web - based and Client-Server business applications using OOP and Java/J2EE technologies.\n•\tExposure to all phases of Software Development Life Cycle(SDLC) using Agile, RUP, Waterfall.\n•\tDesigned and developed web UI screen using Angular-JS.\n•\tDeveloped AngularJS Controllers, Services, filters and directives for various modules in the application.\n•\tKnowledge on ETL tools like Kettle Pentaho and Microsoft SSIS tools.\n•\tCreated custom directives, decorators and services using AngularJS to interface with both RESTful and legacy network services also DOM applications.\n•\tExperience with MVC frameworks like Struts, SPRING and ORM tools like Hibernate.\n•\tExperienced in working with batch jobs using Spring-Batch, Autosys and Quartz.\n•\tWorked extensively with XML related technologies like XML/XSLT to process, validate, parse and extract data from XML using DOM and SAX parsers for DTD and SCHEMAand also worked with JAX-B.\n•\tStrong experience in J2EE technologies like Java Beans, Servlets, JSP (including custom tags), JSTL, JDBC, Struts, Spring, JMS, JNDI and Multithreading.\n•\tExpertise in web development technologies like HTML, DHTML, XHTML, CSS, Java Script, JQuery, JSF, AJAX, Bootstrap JS, Node JS and Angular JS.\n•\tExperienced in RESTful web services using JAX-RS, Jersey framework and SOAP using JAX-WS, Axis-2 framework.\n•\tExpert knowledge over J2EE Design Patterns like MVC, Adapter, Front End Controller, Value object, Singleton, Session Facade, Business Delegate, Factory DAO in designing the architecture of large applications.\n•\tExperience in using Maven and Ant build scripts for the project build automation.\n•\tExperience in using version control and configuration management tools like SVN, Clear Case and CVS.\n•\tExpertise in working with various Application Servers such as IBM WebSphere, JBoss, Glassfish, Oracle WebLogic and Apache Tomcat server.\n•\tGood knowledge in using ’s such as Eclipse, NetBeans, JBuilder, RAD and STS.\n•\tExpertise in working with Relational databases such as Oracle, PostgreSQL, DB2, MySQL and NoSQL database MongoDB.\n•\tExperience in database design using PL/SQL to write Stored Procedures, Functions, Triggers, views and good at writing complex queries for Oracle 10g/11g.\n•\tGood experience in developing test cases with JUnit for Unit testing, Load testing and logging using Log4J.\n•\tExperienced in using Operating Systems like Windows 98 / 2000 / NT / XP, AIX, Sun Solaris.\n•\tProficient in software documentation and technical report writing.\n•\tInvolved in Performance analysis and improvements of the application using tools like Jmeter and using commands on Unix box to resolve deadlocks and improve performance.\n\nTECHNICAL SKILLS:\nProgramming Languages: Java/J2EE, PL/SQL, Unix Shell Scripts\nJava/J2EE Technologies: JavaBeans, collections, Servlets, JSP, JDBC, JNDI, RMI, EJB\nFrameworks: Struts 1.x/2.x, Spring 2.5/3.0, Web Framework, JSF, Hibernate, iBatis, JPA, Axis-2, Jersey\nMethodologies/Design Patterns: OOAD, OOP, UML, MVC, Singleton, DTO Pattern, DAO Pattern, Service Fa ade, Factory Pattern\nBuild Automation: Jenkins, Maven, Ant\nApplication/Web Servers: IBM Web Sphere 6.x/5.x, BEA Web Logic 8.1/9.1, Apache Tomcat 5.x/6.x, JBOSS 4.x/3.x\nXML processing: DTD, Schema, JAX-P (DOM, SAX), JAX-B\nWeb Services: RESTful, SOAP\nWeb Development: HTML, DHTML, XHTML, CSS, Java Script, JQuery, AJAX, LADP, JSF, Bootstrap JS, Node JS, Angular JS\nVersion Control Tools: CVS, Harvest, IBM Clear case, SVN and GIT\nDatabases: Oracle 9i/10g/11g, IBM DB2, SQL Server 2005/2008, PostgreSQL, MySQL, MangoDB\nMessaging Techologies: JMS, IBM MQ\nIDE s: Eclipse, NetBeans, RAD, WSAD\nTesting and Logging Frameworks: Junit, Log4j, Mockito, Finesse Tests\nReporting Tools: Crystal Reports 11, Jasper Reports\nTools: Rational Rose, MS Visio, XML Spy, TOAD\nOperating Systems: Windows 98/2000/NT/XP, AIX, Sun Solaris, HP-UX\nPROFESSIONAL EXPERIENCE:\n\nCVS, Woonsocket, Rhode Island                                 Full Stack Java Developer\nApril 2016 – Present\nResponsibilities:\n•\tInvolved in various stages of Software Development Life Cycle (SDLC) deliverables of the project using the Agile methodology.\n•\tUsed AWS Cloud platform and its features which include EBS, AMI, SNS, RDS, EBS, Cloud Watch, Cloud Trail, Cloud Formation, Cloud Front, S3, and Route53. \n•\tExpertise in building rich, interactive user interfaces using HTML, CSS, JavaScript, jQuery, Node.Js and Angular.Js.\n•\tGathered and clarified requirements with business analyst to feed into high-level customization design, development and installation phases.\n•\tUsed Spring Framework for dependency injection for Action classes using Application Context XML file. \n•\tInvolved in implementation of MVC pattern using JSP and Spring Controller.\n•\tDeveloped business objects using Spring IOC, Spring MVC and Spring AOP. Implemented MVC architecture using JSP Spring, Hibernate and used Spring Framework to initialize managed beans and services.\n•\tImplemented SOA architecture with Web Services using SOAP, JAX-WS, WSDL, UDDI and XML.\n•\tUsed Collections for Model classes in the DAO layer (Data Access Object) Involved in modifying some changes in DAO layer using Hibernate.\n•\tCreated mappings among the relations and written SQL queries using Hibernate.\n•\tImplemented Concurrency, Exception Handling and Collections whenever necessary.\n•\tUsed Entity Beans to persist the data into IBM DB2 database like database access components, Creating Schemas and Tables.\n•\tUsed SQL to perform data mapping and backend testing, also documented all the SQL queries for future testing purpose.\n•\tCreated process flow for deploying application in Web Sphere application server.\n•\tManaged build, reporting and documentation from the project information using Jenkins, Maven Tool and SVN for version control.\n•\tUsed Jenkins for Continuous Integration.\n•\tUsed JUnit for testing and used JIRA for tracking bugs.\n•\tResponsible for the dealing with the problem, bug fixing and troubleshooting.\n Environment: Java, J2EE, HTML, CSS, JavaScript, jQuery, Ajax, Spring, Spring IOC, Spring AOP, Spring MVC, Hibernate, REST, SOAP, XML, Eclipse, PL/SQL, JUnit, Maven Build Tool, DB2, JIRA, Jenkins, SVN and IBM Web Sphere, AngularJS, EBS, AMI, SNS, RDS, Cloud Watch, Cloud Trail, Cloud Formation, Auto scaling\n\nToll Brothers, Horsham Township, Pennsylvania                  Software Engineer\nDecember 2015 -  March 2016\nResponsibilities:\n•\tDeveloped JSP and extensively used tag libraries. \n•\tDesigned the system with OOAD methodology using various design patterns like factory method, Singleton, Adaptor, Template etc. \n•\tImplementing and planning the server-side architecture using Spring and Hibernate \n•\tConfigured the spring framework for entire business logic layer with XML bean configuration files. \n•\tPreparation of Low Level Designing and High Level Designing and relevant documentation. \n•\tExtensively used Spring IOC for Dependency Injection and worked on Custom MVC Frameworks loosely based on Struts \n•\texperienced in build tools like Micro services, Ant, Maven and Gradle tools.\n•\tWrote Controller classes in Spring MVC framework in the web layer. \n•\tProduced the shopping cart on the client Front-end using jQuery, JavaScript, HTML5, CSS3. \n•\tExtensively used Eclipse based STS IDE for building, developing and integrating the application. \n•\tUsed Table per hierarchy inheritance of hibernates and mapped polymorphic associations. \n•\tDeveloped one-much, many-one, one-one annotation based mappings in Hibernate. \n•\tWrote queries Using Cassandra CQL to create, alter, insert and delete elements. \n•\tDeveloped DAO service methods to populate the domain model objects using hibernate. \n•\tUsed java collections API extensively such as Lists, Sets and Maps.  \n•\tWrote DAO classes using spring and Hibernate to interact with database for persistence. \n•\tDeveloped components of web services (JAX-WS, JAX-RPC) end to end, using different JAX-WS standards with clear understanding on WSDL, SOAP using various message patterns  \n•\tPerformed on e-Commerce by using JSF framework and JavaScript, jQuery, HTML5 pages\n•\tWrote and tested Java Beans to retrieve trading data and subscriber's information from MySQL database server,\n•\t Extensive experience in Angular.JS for application implementation, proficient in creating modules, controllers, route-Providers, factory services, ng-repeat, customizable filter, http get/post methods and directives to realize functionalities like REST service with Ajax call , input validations, searchable and sortable contents.  \n•\tImplemented Unit and Integration test cases with JUnit Framework based on Functional Flow. \n•\tUsed tools like My Eclipse IDE, configured and deployed the applications onto Web Logic application server \n•\tConfigured Log4j for logging and debugging \n Environment: Eclipse, Java J2EE, HTML, JSP, JAX RPC, JAXB, CSS3, JavaScript, and jQuery, Spring MVC, Hibernate, RESTful web services, Apache Tomcat7.0, Cucumber, Cassandra, Junit, Jenkins, Maven, GitHub, XML, Log4j, EJB, MySQL, Ajax.\n\nDairy Farmers of America, Kansas City, Missouri                      Java Developer\nNovember 2014 – December 2015\nResponsibilities:\n•\tResponsible for developing use cases, class and sequence diagram for the modules using UML and Rational Rose.\n•\tIdentifying and design of common interfaces across multiple systems or modules of social insurance.\n•\tDeveloped the application using Spring Framework that leverages classical Model View Layer (MVC) architecture. UML diagrams like use cases, class diagrams, interaction diagrams (sequence and collaboration) and activity diagrams were used.\n•\tDeveloped J2EE modules using XMI and CORE JAVA.\n•\tInteraction with Business users for user and system acceptance testing.\n•\tValidated the data against the business rules.\n•\tData access layer is implemented using Hibernate.\n•\tUsed Apache POI to generate Excel documents\n•\tImplemented Struts action classes.\n•\tUsed Spring Security for Authentication and authorization extensively.\n•\tUtilized Eclipse to create JSPs/Servlets/Hibernate that pulled information from a Oracle database and sent to a front end GUI for end users.\n•\tUsed JDBC for Oracle database connection and written number of stored procedures for retrieving the data.\n•\tDeveloped modules for validating the data according to business rules and used Castor to convert data into array of XML strings and XSLT for transformation.\n•\tUsed Hibernate for data persistence.\n•\tDeveloped SOAP based HTTP requests for communicating with Web Services.\n•\tWas involved in the design of multi-tier architecture using EJB, Servlets and JSP.\n•\tUsed Spring Dependency Injection properties to provide loose-coupling between layers.\n•\tCollaborated with Web designers to create the JSP pages, applying HTML, JavaScript, JQuery and Struts Tags.\n•\tExtensively worked on debugging using Logging Frameworks such as Apache Log4j.\n•\tCreated test plans for unit testing to validate component functionality.\nEnvironment: Java 1.4.2, J2EE, Servlets, MVC, Web services, Struts, Spring - Core, MVC, Security, Eclipse, Hibernate, XML, XSLT, EJB, JSP, JDBC, JAX-B, JQuery, JavaScript, HTML, Log4j, Oracle 10g, Apache POI, Caster, XMI.\n\nBank of Utah, Ogden, Utah                                                           J2EE Developer\nMay 2013 – October 2014\n\nResponsibilities:\n•\tDesigned and developed Servlets and JSP, which presents the end user with form to submit the details of the problem.\n•\tCreated SQL statements and triggers for the effective retrieval and storage of data from the database.\n•\tPerformed JUnit testing, proposed and implemented performance enhancements, worked with Oracle databases, running SQL scripts and stored procedures.\n•\tDeveloped Restful based Web Services.\n•\tWas involved in the design of multi-tier architecture using EJB, Servlets and JSP.\n•\tDeveloped Servlets used to store user information in the database, which makes a JDBC-ODBC connection to the database and inserts the details into to the database.\n•\tDesigned and developed a Servlet, which presents the engineer a form to submit solution to particular problem.\n•\tSetting up test environments and configuring various components of the application using JDBC API to establish a connection with oracle database and configuring.\n•\tDesigned and developed a Servlet, which allows the end user to query on the problem, makes a JDBC-ODBC connection to the database and retrieve the details regarding the call number and the status of the submitted problem.\nEnvironment: Java, J2EE, Servlets, JSP, EJB, Custom tags, JDBC, JUNIT, Restful, Data Source, DAO, VO Patterns, Tomcat 5.0, SQL, Oracle 9i, Linux.\n\n\nEpsilon, Irving, Texas                                                         Junior Java Developer\nJanuary 2012 – April 2013\nResponsibilities:\n•\tDesigned the user interfaces using JSP.\n•\tDeveloped Custom tags, JSTL to support custom User Interfaces.\n•\tDeveloped the application using Struts (MVC) Framework.\n•\tImplemented Business processes such as user authentication, Account Transfer using Session EJBs.\n•\tUsed Eclipse to writing the code for JSP, Servlets, Struts and EJBs.\n•\tDeployed the applications on Web Logic Application Server.\n•\tUsed Java Messaging Services (JMS) and Backend messaging for reliable and asynchronous exchange of important information such as payment status report.\n•\tDeveloped the Ant scripts for preparing WAR files used to deploy J2EE components.\n•\tUsed JDBC for database connectivity to Oracle.\n•\tWorked with Oracle Database to create tables, procedures, functions and select statements.\n•\tUsed JUnit Testing, debugging and bug fixing.\n•\tUsed Log4J to capture the log that includes runtime exceptions and developed WAR framework to alert the client and production support in case of application failures.\n•\tWorked in Rational Unified Process (RUP) Methodology.\nEnvironment: Java, J2EE, JSP, JSTL, JDBC, Struts, EJB, JMS, Oracle, HTML, XML, Web Logic, Ant, CVS, Log4J, JUnit, JMS, PL/SQL, JavaScript, Eclipse IDE, UNIX Shell Scripting, Rational Unified Process (RUP).\nEducation: \nBachelor of Computer Science – University of North Texas, Denton, Texas", {'entities': [(176, 218, 'YEARS'), (222, 382, 'RESPONSIBILITIES'), (386, 477, 'RESPONSIBILITIES'), (481, 534, 'RESPONSIBILITIES'), (538, 642, 'RESPONSIBILITIES'), (674, 688, 'SKILLS'), (693, 713, 'SKILLS'), (848, 864, 'SKILLS'), (884, 898, 'SKILLS'), (912, 918, 'SKILLS'), (923, 932, 'SKILLS'), (996, 1008, 'SKILLS'), (1010, 1017, 'SKILLS'), (1022, 1028, 'SKILLS'), (1056, 1080, 'SKILLS'), (1318, 1322, 'SKILLS'), (1431, 1436, 'SKILLS'), (1438, 1443, 'SKILLS'), (1450, 1461, 'SKILLS'), (1476, 1480, 'SKILLS'), (1496, 1503, 'SKILLS'), (1508, 1518, 'SKILLS'), (1482, 1494, 'SKILLS'), (1776, 1787, 'SKILLS'), (1873, 1876, 'SKILLS'), (1967, 1997, 'SKILLS'), (2213, 2221, 'SKILLS'), (2223, 2231, 'SKILLS'), (2233, 2236, 'SKILLS'), (2241, 2244, 'SKILLS'), (2311, 2321, 'SKILLS'), (2338, 2343, 'SKILLS'), (2353, 2360, 'SKILLS'), (2576, 2588, 'SKILLS'), (2590, 2602, 'SKILLS'), (2651, 2668, 'SKILLS'), (2737, 2759, 'SKILLS'), (2764, 2788, 'SKILLS'), (3601, 3606, 'SKILLS'), (3608, 3613, 'SKILLS'), (3620, 3631, 'SKILLS'), (3641, 3645, 'SKILLS'), (3672, 3679, 'SKILLS'), (3681, 3691, 'SKILLS'), (3658, 3670, 'SKILLS'), (3384, 3387, 'SKILLS'), (3066, 3075, 'SKILLS'), (3818, 3828, 'SKILLS'), (3880, 3883, 'SKILLS'), (3896, 3904, 'SKILLS'), (3906, 3909, 'SKILLS'), (4083, 4100, 'SKILLS'), (4304, 4428, 'RESPONSIBILITIES'), (4432, 4583, 'RESPONSIBILITIES'), (4588, 4685, 'RESPONSIBILITIES'), (4707, 4846, 'RESPONSIBILITIES'), (4850, 4950, 'RESPONSIBILITIES'), (4955, 5028, 'RESPONSIBILITIES'), (5032, 5102, 'RESPONSIBILITIES'), (5104, 5227, 'RESPONSIBILITIES'), (5231, 5316, 'RESPONSIBILITIES'), (5320, 5456, 'RESPONSIBILITIES'), (5460, 5536, 'RESPONSIBILITIES'), (5540, 5618, 'RESPONSIBILITIES'), (5622, 5742, 'RESPONSIBILITIES'), (5746, 5862, 'RESPONSIBILITIES'), (5866, 5945, 'RESPONSIBILITIES'), (5949, 6074, 'RESPONSIBILITIES'), (6078, 6117, 'RESPONSIBILITIES'), (6121, 6175, 'RESPONSIBILITIES'), (6179, 6255, 'RESPONSIBILITIES'), (6748, 6873, 'RESPONSIBILITIES'), (6878, 6959, 'RESPONSIBILITIES'), (6963, 7060, 'RESPONSIBILITIES'), (7065, 7151, 'RESPONSIBILITIES'), (7320, 7323, 'SKILLS'), (7549, 7552, 'SKILLS'), (7545, 7548, 'SKILLS'), (7869, 7951, 'RESPONSIBILITIES'), (7956, 8022, 'RESPONSIBILITIES'), (8028, 8114, 'RESPONSIBILITIES'), (8119, 8288, 'RESPONSIBILITIES'), (8293, 8375, 'RESPONSIBILITIES'), (8378, 8486, 'RESPONSIBILITIES'), (8491, 8522, 'RESPONSIBILITIES'), (8523, 8820, 'RESPONSIBILITIES'), (8947, 8950, 'SKILLS'), (9460, 9552, 'RESPONSIBILITIES'), (9556, 9654, 'RESPONSIBILITIES'), (9899, 9945, 'RESPONSIBILITIES'), (9949, 10019, 'RESPONSIBILITIES'), (10023, 10068, 'RESPONSIBILITIES'), (10072, 10120, 'RESPONSIBILITIES'), (10124, 10167, 'RESPONSIBILITIES'), (10170, 10203, 'RESPONSIBILITIES'), (10207, 10276, 'RESPONSIBILITIES'), (10280, 10419, 'RESPONSIBILITIES'), (10423, 10527, 'RESPONSIBILITIES'), (10531, 10686, 'RESPONSIBILITIES'), (10690, 10725, 'RESPONSIBILITIES'), (10729, 10799, 'RESPONSIBILITIES'), (10803, 10884, 'RESPONSIBILITIES'), (10888, 10972, 'RESPONSIBILITIES'), (10976, 11082, 'RESPONSIBILITIES'), (11086, 11163, 'RESPONSIBILITIES'), (11167, 11238, 'RESPONSIBILITIES'), (12022, 12103, 'RESPONSIBILITIES'), (12107, 12269, 'RESPONSIBILITIES'), (12273, 12382, 'RESPONSIBILITIES'), (12386, 12546, 'RESPONSIBILITIES'), (13067, 13105, 'RESPONSIBILITIES'), (13132, 13136, 'SKILLS'), (13232, 13327, 'RESPONSIBILITIES'), (13402, 13459, 'RESPONSIBILITIES'), (13463, 13613, 'RESPONSIBILITIES'), (13631, 13634, 'SKILLS'), (13891, 14056, 'RESPONSIBILITIES'), (14144, 14148, 'SKILLS'), (14204, 14207, 'SKILLS'), (14261, 14264, 'SKILLS'), (14320, 14360, 'EDUCATION')]})]

ner.add_label('SKILLS')
ner.add_label('YEARS')
ner.add_label('RESPONSIBILITIES')
ner.add_label('EDUCATION')

pipe_exceptions = ["ner"]

unaffected_pipes = [pipe for pipe in software_resumes.pipe_names if pipe not in pipe_exceptions]

def evaluate(ner_model, examples):
        scorer = Scorer()
        Examples = []
        for input_, annot in examples:
            pred_value = ner_model(input_)
            example = Example.from_dict(pred_value, annot)
            Examples.append(example)    

        scores = scorer.score(Examples)
        return scores

with software_resumes.disable_pipes(*unaffected_pipes):
        for iteration in range(400):
            random.shuffle(TRAIN_SOFTWARE_RESUME_DATA)
            for raw_text,entity_offsets in TRAIN_SOFTWARE_RESUME_DATA:
                resume= software_resumes.make_doc(raw_text)
                example = Example.from_dict(resume, entity_offsets)
                software_resumes.update([example])
       
software_accuracy = evaluate(software_resumes, TEST_SOFTWARE_RESUME_DATA)

print(software_accuracy)

resume = software_resumes("""Amrinder Pelia	                                                                                              Employer Details
Mail: amirindersingh1234@gmail.com                           Mail: Praveen@indiquesolutions.com 
	                                                                  Phone: 703-743-0795

Senior Business Analyst

Summary:

•	Around 10 years of experience in Business process analysis, Business modeling and Business requirements gathering.
•	Extensive experience with Banking and Mortgage clients.
•	Expert in creating diagrams (Use case diagrams, flow charts, activity diagrams, sequence diagrams), use case document, test plans and test case documents.
•	Worked closely with project Stakeholders, SMEs, staff to understand requirements and specifications for new applications along with re-engineering the existing application.
•	Experience in interacting across the hierarchy from architects, to data modelers, underwriters and risk analyst.
•	Experience in iterative agile project management methodology with Scrum to manage the software development life cycle (SDLC).
•	Used MS Project to manage schedules, meet deadlines and plan resources in line with triple constraint. Followed up with weekly Project Status and organized Task Review meetings. Conducted status meetings, managed deadlines, and facilitated prioritization discussions.
•	Writing skills in preparing business requirements documents (BRD), system requirements specifications (SRS) and technical design document (TDD) and defining project plans then translating business requirements/user expectations into detailed specifications employing UML.
•	Performing GAP analysis to check the compatibility of the existing system infrastructure with the new business requirements, 
•	Conducting User Acceptance Testing (UAT) verifying performance, reliability and fault tolerance issues. Also familiar with testing tools (QC) to design as well as develop test plans and test scripts. 
•	Authored business and system requirements analyses and functional specifications with supporting business process flows (data modeling), Traceability matrices, risk analysis and concept of operations for systems utilizing company standards, processes, and procedures.
•	Expertise at using MS Visio, MS Project, MS Excel, PowerPoint, and SharePoint.
•	Good understanding of software development methodologies such as RUP, JAD, and RAD and hands on experience in formulating JAD sessions. 
•	
Skill Set:  

SDLC Methodologies	Waterfall, Agile - RUP, Scrum
Operating System	Windows 2008/XP/2007/2003
Project Management Tool	MS Office suite, SharePoint & Project, Rational Rose, Requisite Pro
Defect Tracking	Test Director/Quality Center, HP Quality Center
Database	Microsoft SQL Server, Oracle, MS Access.
Application environments	.NET Framework, ASP.NET
Education:Bachelors in Applied Sciences and Engineering, Michigan State University, GPA– 3.56

Professional Experience:

Fifth Third Bank, Cincinnati, OH                                                                      Mar 2015 to Present
Senior Business Analyst/QA Lead

Fifth Third Bank is one of the nation’s largest diversified financial services organizations providing retail and banking; residential mortgage banking. 

Worked on implementing the IDS Rapport Solution to provide a front-end workflow processsing system integrating with the existing IDS Infolease solution. This solution was used to create contract documents and eliminated the need for several Access database and Excel spreadsheet solutions that existed. This solution aslo integrated with iLien solution for UCC filing. The product increased the efficiency of transactional submittals and documentation and booking functions.

Responsibilities:

•	Implemented Traceability Matrix and User Requirement Specification Document (URS) to verify the functionality coverage. 
•	Extensive use of MS Project, MS SharePoint (used as the library for Project documentation and the communication of Project information).
•	Created Mortgage Service Platform (MSP) diagram in MS Visio to understand the big picture of the project.
•	Facilitated and managed meeting sessions with committee of SME from various business areas including Mortgage Servicing, Loan Monitoring and Asset Management.
•	Responsible for working with product management to translate business objectives into functional requirements, and great user experiences for our customers.
•	Created detailed Test plans to check the functionality of Application.
•	Participated in QA team and Bug tracking or Defect Review meetings.
•	Designed and Developed front end and Back end Test scenarios and Test cases
•	Performed manual testing on different Modules of the Application by executing the Test Cases.
•	Coordinate with all project team members to ensure project needs are clearly understood and supportable.
•	Identify and remove or mitigate obstacles and risks to projects.
•	Conducted peer review meetings periodically to keep track of the project’s milestones.
•	Assisted the Project Manager with creating detailed project plans and also in developing, scheduling and tracking project timelines.
•	Conducted GAP Analysis of current state (As-Is) and proposed state (To-Be) situations and represented in MS Visio. 
•	Facilitated JAD sessions with the business team and technology team.
•	Responsible for leading all aspects of projects from start to finish, including project team definition, resource allocation decisions.
•	Developed high level design of new processes and graphically presented along with text based requirements.
•	Experience in creating wireframes.
•	Created Activity Diagrams, and Sequence Diagrams using UML in MS Visio.
•	Conducted Previews and User Acceptance Test (UAT) sessions.

Environment: MS Visio, DOORS

Mississippi State Division of Medicaid, Jackson, MS            May 2013- Feb 2015
Sr. Business Analyst 
Mississippi Division of Medicaid’s Management Information System (MMIS) had to comply with the CMS mandated Health Insurance Portability and Accountability Act (HIPAA) requirements. Project was to analyse system impact and perform GAP between current HIPAA 4010 and compliance HIPAA 5010 for state Medicaid Management Information System.

Responsibilities:
•	Actively worked on Business requirement gathering, analysis and Data analysis
•	Facilitated JAD sessions to collect User Requirements, Business Requirements and Functional Requirements.
•	Created Business/User/Functional document using MS Project, MS Word and MS Visio that provided appropriate scope of work for technical team to develop prototype of the overall system.
•	Gathered requirements from the administrative staff and business rules for determining member eligibility and successfully converted them into functional requirements for the developments team.
•	Created Use Cases, various UML Diagrams and Data Flow Diagrams to determine the data flow via various systems
•	Developed and maintained the Requirement Traceability Matrix (RTM) for the project deliverables.
•	Proposed the change and reengineering of the ‘AS IS’ Business processes into the ‘TO BE’ process flow
•	Involved in the day-to-day implementation of the agile methodology of application development with its various work flows, Artefacts and activities.
•	Created Business Rule Comparison (BRC) documents using 4010 / 5010 implementation guides for X12 transactions 
•	Extensively involved in HIPAA 5010 User Acceptance Testing (UAT). Defined and maintained Test Cases for EDI transactions.
•	Thoroughly studied the inherent systems to have a clear understanding of the business processes and associated system workflow.
•	Used HP Quality Centre for error reporting and communicating between developers, product support and test team members
•	Recommended corrective actions, if necessary, along with the progress against Development/Action Plan routinely to the Project Manager.
•	Used MS Share point for sharing documents, calendars and other data between users in different locations.
•	Wrote test cases and test plans for the related and assigned scripts according to the test strategies defined in the project and testing team guidelines in Quality centre.
•	Assisted in regression testing and did UAT to improve overall quality of the Application.
•	
Environment: UML, Windows, Agile, Mainframe, SQL, ETL, Data warehouse, Microsoft Office, Test Director, MMIS, MS Access, HTML, XML, Java Script, Java, ASP, DB2.
Dept of Health, Austin TX						May 2012 - April 2013
Sr. Business Analyst
I worked as a business analyst in the project intended to make the existing application comply with HIPAA 5010 standards. I was involved in the analysis of EDI transactions 834 and 837I, 837Pbased on HIPAA 4010 and mapping them in order to make the application comply with HIPAA 5010 standards. The module that I worked on allowed the agents to track and manage the status of health benefit claims. My daily responsibilities included performing typical BA duties and additionally included doing QA work such as coordinating the testing process during the testing and UAT phase of the application. I was also responsible in maintaining the application during the “warranty period” and making sure all the issues were solved.  

Responsibilities:
•	Coordinated with the developers, testers and users on verifying, documenting and addressing any issues with the newly implemented HIPAA 4010 to 5010 conversion at the time.
•	Created and maintained data mapping document(s) in reference to the HIPAA mandated transactions834 and 837I, 837P.
•	Independently studied the changes being made and helped them implement in the application.
•	Conducted and participated in meetings for requirement elicitation and documentation. 
•	Worked with end users, SMEs, and stakeholders to fully understand issues with the older application and the requirements of the new application being built.
•	Interviewed business users to gather requirements and analyzed the feasibility of their needs by coordinating with the project manager and the technical lead.
•	Conducted and participated in JAD sessions with the system architect, Subject Matter Experts (SMEs) & the project sponsor for fast & effective system requirement development.
•	Used Customer Relationship Management (CRM) in order to meet customer expectation.
•	Identified and gathered the data requirements and wrote SQL queries using tools such as My SQL Workbench and Aqua Data Studio.
•	Wrote very detailed BRDs and FRDs based on the requirements gathered.
•	Used MS Visio to create flow charts, use case diagrams, activity diagrams to illustrate business rules and process flows required for the BRDs and FRDs. 
•	Wrote test cases for testing the migration of EDI 4010 to 5010 and the processing of EDI transactions 820, 834,837I and 837P.
•	Helped coordinate the testing process by helping the QA team prepare for the testing requirements such as environment, writing instructions, organizing walkthroughs, selecting the test groups, etc.  
•	Used Waterfall methodology throughout the development process and was extensively involved with developers on every stage of the application development.

Environment: Waterfall, SQL, MS Word, MS Excel, MS Project, MS Visio, BRDs, FRDs, Quality Assurance, UAT
Prime Therapeutics, Eagan, MN					Jan 2011 - Apr 2012
Business System Analyst
Prime therapeutics is leading Pharmacy benefit Management Company. I worked with member marketing/customer experience team where I was required to work on all the correspondence materials sent out to the existing members for various reasons. I as primarily focus on Prime mail, Guided health and Specialty.

Responsibilities:
•	Worked as a liaison between technology and the business clients to improve business processes and support critical business strategies.
•	Utilized industry knowledge to provide executive management with the development and implementation of interactive business tools and strategic analysis.
•	Setup and manage inter-departmental status meetings, often including off-shore development and QA teams.  
•	Scheduled review presentation meetings with developers, System Analysts (SA) and business owners for project completion and approval using Adobe Connect.
•	Understood the Business Logic, User Requirements & developed Design & User Interface Specifications
•	Worked with the stakeholders to understand the features they wanted to be implemented in the new version such as new notification options, account features, better sorting of the transaction list, preferred UI changes, etc.
•	Worked with SMEs, business users and technical leads in understanding and documenting issues with the older version of the application.
•	Wrote SQL queries for database inquiries whenever needed. Worked with System Admin for any database related task such as creating production scrubs, database access for team members, any issues, etc. 
•	Used Agile methodology throughout the project and extensively involved in all stages of development.
•	Helped update Product Backlog whenever needed and also created Sprint logs by working with the team lead.
•	Conducted multiple meetings in the middle of the sprint to solve any issues encountered during the sprint.
•	Logged issues and presented them during the sprint reviews for discussion.
•	Designed and finalized mockups using Axure. This helped the team in better understanding proposed changes.
•	Helped in coordinating UAT phase for every sprint.
•	Involved in logging post-deployment issues and making sure they were addressed as per their urgency and priority.
•	Successfully completed the project within time and budget despite having a very tight schedule. 
	
Environment: Agile, SCRUM, MS Visio, MS Project, Axure, SQL, My SQL Workbench. HEDIS, Lotus notes

PNC Bank, Norristown, PA                                                                              Oct 2008 to Dec 2010
Business Analyst

The project was aimed at successfully implementing a system that provides an integrated, shared view of the customer across the enterprise that enforces and encourages consistent customer data. The goal was to increase efficiency and customer service through the development of a user-friendly, web-based banking information system, which will allow for maintenance of a centralized database for the managers of Bank. 

Responsibilities:

•	Conducted GAP Analysis to identify key areas of concern and addressed them with the Business team. Documented the AS-IS and TO-BE processes.
•	Actively engaged client and third party integration partners in requirements gathering and validation. 
•	Developed business Use Cases using UML for new product functionality after conducting requirements elaboration sessions with client teams.
•	Used Rational Unified Process for the Software Development Life Cycle of this project. 
•	Documented business and functional requirements
•	Provided assistance in reviewing, analyzing and evaluating business requirements, user needs and functions with the objective of improving business processes and procedures.
•	Generated process flow diagrams
•	Maintained an issue log and driven issues to closure
•	Worked closely with the development team to make sure all the requirements were covered.
•	Maintained versioning in requirements
Environment: MS Visio, Rational Requisite Pro, Quality Center
""")

for ent in resume.ents:
       print(ent.label_, ent.text)



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

    form = forms.ImageForm()

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

    form = forms.ImageForm()

    resumeForm = forms.ResumeForm()

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

    form = forms.ResumeForm()

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

    