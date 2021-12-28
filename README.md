# ReturnsScraper

DESCRIPTION:

A tool that allows one to see the leadership of specific sector ETFs in real-time. 
The performance data is first retrieved from SeekingAlpha.com.
The program then proceeds to fetch the useful data into a Pandas DataFrame. 
Finally, using matplotlib, it displays a performance graph, where: x-axis = 1 Year returns (%) and y-axis  = 4-Week returns (%).

HOW TO INTERPRET:

The more upper right the ETF is, the more it is leading (showing strength).
Whereas the more on the lower left part an ETF finds itself in, the more it is lagging (showing weakness)

HOW TO USE:

When starting the program, it will prompt the user with the following text: "Select ETF performance data you would like to see the leadership of: ".
Where the user shall input either the index number (starting from 1, ending at 15) or an acronym.
Once the program receives an input from the user, it proceeds to look for the corresponding function to use.
Immediately after the program finds the correct function, the leadership graph is displayed to the user.

