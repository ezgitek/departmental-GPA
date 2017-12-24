# Departmental Average Calculation Tool

This is a simple tool for calculating department-based averages for Boğaziçi Unversity students. 

### Program Execution
You need Python2.7 in order to run this program. Fire up the terminal and type: 

    python dgpa.py path/to/file [-d <deptname1> <deptname2> ...]

path/to/file: This is the pdf version of the Academic Records. You can download it by following Registration -> Academic Records -> Print.

-d: This is an optional argument for departments. For example, if I only want my "phys" and "cmpe" courses to be included in my average, I would type "-d phys cmpe". If this argument is not given, overall GPA and SPAs are calculated.

### Program Output
In order not to make abundant requests to [PDFTables API](https://pdftables.com/api) the program produces a .csv file. You might want to acquire an API key yourselves since mine is limited to 50 requests. GPA and SPAs are outputed to the console.

Feel free to collaborate. Also let me know if you have any problems, since I could not test the program with many pdfs. 
