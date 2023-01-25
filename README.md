# Laboratory-of-Data-Science
Repository of Laboratory of Data Science Project at UniPi
<br>Decision Support Systems - Module II (6 ECTS): [LABORATORY OF DATA SCIENCE](http://didawiki.cli.di.unipi.it/doku.php/mds/lbi/start) (2022/2023)

[Dataset](http://didawiki.cli.di.unipi.it/lib/exe/fetch.php/mds/lbi/answerdatasetnew.zip)

**BI process** : Data integration, construction of an OLAP cube, qurying of a OPLAP cube and reporting. 
<br>**Main**: PyCharm, Visual Studio, SQL Server, SSIS, SSAS, Power BI.

The goal of this project is to implement from scratch a data warehouse populated using ETL processes starting from a source made mainly by .csv files to a fully functional architecture used for answering business questions and ultimately produce power BI dashboards.

<br>In **the first part** of the project, it was performed data cleaning & data engineering on the source data, through which the data was prepared and adapted to the task at hand. The datawarehouse architecture was built on Microsoft SQL management studio.

<br>In **the second part** it was employed the SISS package of Visual Studio for answering business questions through the construction of data flows.

<br>In **the third part**, it was build a multidimensional data cube employing the MOLAP technology. Hierarchies and measures were created for answering further business questions using the MDX query language.

Ultimately, the snowflake data structure along with the multidimensional cube, we used for creating dashboards in Power BI.
