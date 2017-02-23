Assumptions:
------------

* Schema: Position_ID is foreign key referencing Insturment ID
* Average Cost Valuation: Not sure, if the unit price is to be returned or total cost, so returning average unit price


* Requirements:
---------------
	i) MySQLdb-python
	ii) nosetests for running tests

* Running: 
----------
	TESTING: from inside "application" folder, run the command: `nosetests -w tests -vv --nocapture`
	API: from inside "application" folder, run `python api.py <port>`


NOTE: Trying to follow some principles from Hexagona layered design, which is why, sending context with io related info around


