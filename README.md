# Quandl_Analysis

#### How To Run:
To run this code, simply close the repository and in the command line, enter "python analyze_stocks.py".  To display the "biggest_loser", simply run "python analyze_stocks.py loser".  Make sure that quandl is properly installed in your environment with "pip install quandl".  Also, a QUANDL_CODE environment variable must be accessible with a valid api key.

#### How To Test:
To run the tests, make sure pytest is properly installed in your environment with "pip install quandl".  Then from the root of this repository, simply enter "pytest" into the command line.

#### Additional Notes:
Contrary to the specifications in the requirements, it was decided to structure the output (see output.txt) as a multi-leveled dictionary with outer keys as ticker and inner keys as month.  The inner most dictionary has average open and average close with corresponding values.  The reason for this is to enable constant O(1) lookup time for a chosen ticker and month.

Dataframes were used for 'heavy processing' in this case as this is more optimal than using native python data structures. 
