# ReturnsScraper

DESCRIPTION:

A tool that lets the user check the momentum leadership of sector ETFs in real-time. 
The performance data is first retrieved from various sites.
Then, the program proceeds to fetch the data that is deemed useful into a Pandas DataFrame. 
Finally, using the MatplotLib library, a performance graph is displayed, where the x-axis represents the asset's gain factor with respect to its 52-Week Low while the y-axis represents the asset's performance relative to its 52-Week High.

HOW TO INTERPRET:

The more upper right the ETF is, the more it is leading (showing strength).
Whereas the more on the lower left part an ETF finds itself in, the more it is lagging (showing weakness)

HOW TO USE:

When starting the program, it prompts the user with the following text: "Select ETF performance data you would like to see the leadership of: ".
Where the user shall input either an index number (starting from 1, ending at 15) or an acronym.
Once the program receives an input from the user, it proceeds to look for the corresponding function to use.
Immediately after the program finds the correct function, the leadership graph is displayed to the user.
