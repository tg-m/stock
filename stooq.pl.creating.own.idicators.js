-------------------------------------------------------------------------
                CREATING YOUR OWN INDICATORS IN FnCharts
-------------------------------------------------------------------------

This document contains the following information:
- sample indicator definitions
- the short description of indicator definition rules
- the list of predefined functions that can be used in indicator
  definitions
- performance related tips
- error messages related information

-------------------------------------------------------------------------
                       SAMPLE INDICATOR DEFINITIONS
-------------------------------------------------------------------------

/* User-defined ROC (Rate of Change)
 * - short version
 * You can copy the following algorithm into the indicator definition
 * window.
 * Remember to enter the default value of the first parameter (i.e. 5)
 * into the parameter field.
 */

var close = Close();
var roc = CreateArray(close.length);
var n = Param(1);
for(var i=n; i<close.length; i++)
	roc[i] = 100.0 * (close[i] - close[i-n]) / close[i-n];
AddGraph(roc,n);
AddHorizLine(0);

/* End of user-defined ROC */

-------------------------------------------------------------------------

/* User-defined ROC (Rate of Change)
 * - long version with comments
 * You can copy the following algorithm into the indicator definition
 * window.
 * Remember to enter the default value of the first parameter (i.e. 5)
 * into the parameter field.
 */

/* Obtain the array of closing price values using predefined Close()
 * function and store these values in the 'close' variable.
 */

var close = Close();

/* Create the array to store calculated ROC values for every trading
 * session. To perform this operation, use predefined CreateArray(length)
 * function.
 * Caution:
 * The length of created 'roc' array must be the same as the length of
 * afore-mentioned 'close' array.
 * Predefined CreateArray() function will initially set values of each
 * array element to zero.
 */

var roc = CreateArray(close.length);

/* Obtain the value of the first indicator parameter and store that value
 * in the variable called 'n'
 * Caution:
 * The default value of the first parameter (i.e. 5) must be entered into
 * the first parameter field.
 */

var n = Param(1);

/* For each trading session (numbered with 'i') calculate ROC value
 * and store that value in corresponding element of the 'roc' array.
 * Caution:
 * Trading sessions are numbered from 0 up to length-1.
 * The oldest trading session is numbered as 0, and the newest trading
 * session (most recent one) is numbered as length-1.
 */

for(var i=n; i<close.length; i++)
	roc[i] = 100.0 * (close[i] - close[i-n]) / close[i-n];

/* Take the array of ROC values, and add graph for that array using
 * predefined function AddGraph(dataArray, firstValidIndex)
 * Caution:
 * 'firstValidIndex' is the first index of the array element that has
 * its value properly calculated.
 */

AddGraph(roc,n);

/* Add graph for horizontal axis (horizontal line at 0 coordinate) */

AddHorizLine(0);

/* End of user-defined ROC */

-------------------------------------------------------------------------

/* User-defined MACD (Moving Average Convergence Divergence)
 * - short version
 * You can copy the following algorithm into the indicator definition
 * window.
 * Remember to fill-in all three parameter fields with default parameter
 * values (i.e. 12, 26, 9)
 */

var close = Close();
var avg1 = ExpAvg(close,Param(1));
var avg2 = ExpAvg(close,Param(2));
var macd = CreateArray(avg1.length);
for(var i=0; i<avg1.length; i++)
	macd[i] = avg1[i] - avg2[i];
AddGraph(macd,Param(2));
var signal = ExpAvg(macd,Param(3));
AddGraph(signal,Param(2)+Param(3));
AddHorizLine(0);

/* The following instructions add buy/sell signals to the MACD chart
 * window.
 */

var begin=Param(2)+Param(3);
for(var i=begin; i<macd.length; i++){
        if((macd[i-1] < signal[i-1]) && (macd[i]>signal[i]))
                AddBuySignal(i);
        else
        if((macd[i-1] > signal[i-1]) && (macd[i]<signal[i]))
                AddSellSignal(i);
}

/* End of user-defined MACD */

-------------------------------------------------------------------------

/* User-defined MACD (Moving Average Convergence Divergence)
 * - long version with comments
 * You can copy the following algorithm into the indicator definition
 * window.
 * Remember to fill-in all three parameter fields with default parameter
 * values (i.e. 12, 26, 9)
 */

/* Define three parameter variables and store actual parameter values
 * in these variables.
 */

var param1 = Param(1);
var param2 = Param(2);
var param3 = Param(3);

/* Obtain the array of closing price values using predefined Close()
 * function and store these values in the 'close' variable.
 */

var close = Close();

/* Calculate first exponential average of closing price values, using
 * predefined ExpAvg(dataArray,period) function and store the result
 * in avg1 variable.
 */

var avg1 = ExpAvg(close,param1);

/* Calculate second exponential average of closing price values, using
 * predefined ExpAvg(dataArray,period) function and store the result
 * in avg2 variable.
 */

var avg2 = ExpAvg(close,param2);

/* Create the array to store calculated MACD values for every trading
 * session. To perform this operation, use predefined CreateArray(length)
 * function.
 */

var macd = CreateArray(avg1.length);

/* For each trading session, calculate MACD value and store that value in
 * 'macd' array.
 */

for(var i=0; i<avg1.length; i++)
	macd[i] = avg1[i] - avg2[i];

/* Take the array of MACD values, and add graph for that array using
 * predefined function AddGraph(dataArray, firstValidIndex)
 * Note the value of the first valid index.
 */

AddGraph(macd,param2);

/* Calculate values for the Signal line and strore them in 'signal' array.
 * (the Signal line is an exponential average of MACD values.
 */

var signal = ExpAvg(macd,param3);

/* Take the array of Signal values, and add graph for that array using
 * predefined function AddGraph(dataArray, firstValidIndex)
 * Note the value of the first valid index.
 */

AddGraph(signal,param2+param3);

/* Add the horizontal zero line to MACD chart.
 */

AddHorizLine(0);

/* Find buy/sell signal occurrences.
 * Begin search from the array element, where both MACD and Signal values
 * are properly calculated.
 */

var begin=param2+param3;

/* Find buy/sell signal occurrences and add them to the MACD chart.
 * Buy signal occurs when the MACD line crosses the Signal line and moves
 * upwards.
 * Buy signal occurs when the MACD line crosses the Signal line and moves
 * upwards.
 */

for(var i=begin; i<macd.length; i++){
        if((macd[i-1] < signal[i-1]) && (macd[i]>signal[i]))
                AddBuySignal(i);
        else
        if((macd[i-1] > signal[i-1]) && (macd[i]<signal[i]))
                AddSellSignal(i);
}

/* End of user-defined MACD */

-------------------------------------------------------------------------

/* User-defined %R (Williams' Percent Range)
 * - short version
 * You can copy the following algorithm into the indicator definition
 * window.
 * Remember to fill-in all three parameter fields with default parameter
 * values (i.e. 10, 20, 80)
 */

var n = Param(1);
var max = Max(High(),n);
var min = Min(Low(),n);
var close = Close();
var percentR = CreateArray(close.length);
for(var i=0; i<close.length; i++)
	if(max[i]-min[i] != 0)
		percentR[i] = 100.0 * (close[i]-min[i]) / (max[i]-min[i]);
	else
		percentR[i] = 100.0;

AddGraph(percentR,n);
AddHorizLine(Param(2));
AddHorizLine(Param(3));

/* End of user-defined %R */

-------------------------------------------------------------------------

/* User-defined %R (Williams' Percent Range)
 * - long version with comments
 * You can copy the following algorithm into the indicator definition
 * window.
 * Remember to fill-in all three parameter fields with default parameter
 * values (i.e. 10, 20, 80)
 */

/* Obtain the value of the first parameter (period) and store it in
 * the variable called 'n'.
 * Caution:
 * The default value of the first parameter (i.e. 10) must be entered
 * into the first parameter field.
 */

var n = Param(1);

/* Calculate maximum values of high price over the selected period
 * (period) using predefined Max(dataArray,period) function.
 * Use predefined High() function to obtain the array of high price
 * values.
 */

var max = Max(High(),n);

/* Calculate minimum values of low price over the selected period
 * using predefined Min(dataArray,period) function.
 * Use predefined Low() function to obtain the array of low price
 * values.
 */

var min = Min(Low(),n);

/* Obtain the array of closing price values using predefined Close()
 * function and store these values in the 'close' variable.
 */

var close = Close();

/* Create the array to store calculated %R values for every trading
 * session. To perform this operation, use predefined CreateArray(length)
 * function.
 * Note that each element of the created array will be initially filled
 * with zero value.
 */

var percentR = CreateArray(close.length);

/* For each trading session, calculate %R value and store that value in
 * 'percentR' array.
 */

for(var i=0; i<close.length; i++)
	if(max[i]-min[i] != 0)
		percentR[i] = 100.0 * (close[i]-min[i]) / (max[i]-min[i]);
	else
		percentR[i] = 100.0;

/* Take the array of %R values, and add graph for that array using
 * predefined function AddGraph(dataArray, firstValidIndex)
 * Note the value of the first valid index.
 */

AddGraph(percentR,n);

/* Take the values of the second and third parameter (Overbought and
 * Oversold levels) and add corresponding horizontal lines to the %R
 * chart.
 */

AddHorizLine(Param(2));
AddHorizLine(Param(3));

/* End of user-defined %R  */


-------------------------------------------------------------------------
          THE SHORT DESCRIPTION OF INDICATOR DEFINITION RULES
-------------------------------------------------------------------------
Indicator algorithms must conform to the following rules:

-they must constitute valid JavaScript code

-the following predefined JavaScript functions may be used to
 simplify indicator construction:
 Open(), High(), Low(), Close(), Volume(), OpenInt(), Param(number),
 CreateArray(length), Min(dataArray,period), Max(dataArray,period),
 ExpAvg(dataArray,period), SimpleAvg(dataArray,period), AddBuySignal(n),
 AddSellSignal(n), StdDev(dataArray,period)

-to add graphs to the indicator area, the following predefined functions
 must be used:
 AddGraph(dataArray,firstValidIndex), AddGraph(dataArray)
 The length of the 'dataArray' argument used in AddGraph function must be
 equal to the length of the array obtained by using such functions as
 Open(), High(), Low(), Close(), Volume(), OpenInt()

-for every indicator calculation, AddGraph function must be used 1, 2, or
 3 times

-to add a horizontal line to the indicator area, the AddHorizLine(value)
 function must be used

-you cannot comment JavaScript code using // string. Use /* ... */
 construct instead.

-the following predefined functions cannot be used in indicator code:
 __checkParams(), __GetValues(), __isIEBrowser()
 They may only be used internally by the FnCharts program.


-------------------------------------------------------------------------
                    THE LIST OF PREDEFINED FUNCTIONS
-------------------------------------------------------------------------

Open()
    Arguments: none
    Returns the array of opening price values for the selected symbol.

High()
    Arguments: none
    Returns the array of high price values for the selected symbol.

Low()
    Arguments: none
    Returns the array of low price values for the selected symbol.

Close()
    Arguments: none
    Returns the array of closing price values for the selected symbol.

Volume()
    Arguments: none
    Returns the array of volume values for the selected symbol.

OpenInt()
    Arguments: none
    Returns the array of open interest values for the selected symbol.

Important information regarding above functions:
1.  Arrays in JavaScript are indexed from 0 to length-1, so the first
    element of an array A is A[0] and the last element is A[A.length-1].
    The first element of the array contains the oldest available data, and
    the last element of the array contains the most recent data.
2.  All afore-mentioned functions always return arrays of the same length.
    For instance, the length of an array returned by Close() function is
    the same, as the length of an array returned by Volume() function.
3.  Arrays returned by Open(), High(), Low() and Close() will always
    contain positive values (values greater than zero).
4.  If there is no Open, High or Low data available for the selected
    symbol, then arrays returned by Open(), High() and Low() functions
    will contain Close values.
5.  If there is no volume or open interest data available for the
    selected symbol, arrays returned by Volume() or OpenInt() functions
    will contain values 0.


Max(array,period)
    Arguments: array - the array for which Max values will be calculated,
               period - the period used in calculations
    Calculates maximum value over the given period.
    Returns the array wherein value of every element is calculated as:
    value[i] = max(array[i],array[i-1],...,array[i-(period-1)])

Min(array,period)
    Arguments: array - the array for which Min values will be calculated,
               period - the period used in calculations
    Calculates minimum value over the given period.
    Returns the array wherein value of every element is calculated as:
    value[i] = min(array[i],array[i-1],...,array[i-(period-1)])

SimpleAvg(array,period)
    Arguments: array - the array for which average values will be
                       calculated,
               period - the period used in calculations
    Calculates simple average over the given period.
    Returns the array wherein value of every element is calculated as:
    value[i] = avg(array[i],array[i-1],...,array[i-(period-1)])

ExpAvg(array,period)
    Arguments: array - the array for which exponential average values
                       will be calculated,
               period - the period used in calculations
    Calculates exponential average over the given period.
    Returns the array wherein value of every element is calculated as:
    value[i] = exp_avg(array[i],array[i-1],...,array[i-(period-1)])

StdDev(array,period)
    Arguments: array - the array for which standard deviation values will
                       be calculated,
               period - the period used in calculations
    Calculates standard deviation over the given period.
    Returns the array wherein value of every element is calculated as:
    value[i] = std_dev(array[i],array[i-1],...,array[i-(period-1)])

CreateArray(length)
    Arguments: length - the length of the array to be created
    Returns new array of the given length with every element initialized
    to zero.

Param(n)
    Arguments: n - parameter number
    Returns the actual value of the given indicator parameter.
    Argument 'n' must be in range between 1 and 3.
    If the value of the given parameter 'n' is not defined then the
    function returns the value of 0.

AddGraph(array,index)
    Arguments: array - the array of data,
               index - index of the first array element containing valid
                       data
    Adds a new graph to the indicator area. The graph is constructed
    based on the data contained in the given array.
    The length of the array must be exactly the same as the length of the
    array returned by such functions as Close(), Volume(), etc.
    Only the part of the graph that represents array elements with
    indices greater than or equal to 'index' will be displayed.
    The 'index' parameter is optional. If omitted, the function call
    AddGraph(array) is equivalent to AddGraph(array,0).

AddHorizLine(value)
    Arguments: value - the y coordinate of the horizontal line.
    Adds a horizontal line to the indicator area.

AddBuySignal(index)
    Arguments: index - the index of the trading session on which the
                       signal occurred
    Adds a new buy signal mark to the indicator area.

AddSellSignal(index)
    Arguments: index - the index of the trading session on which the
                       signal occurred
    Adds a new sell signal mark to the indicator area.


-------------------------------------------------------------------------
                ERROR MESSAGES AND RELATED INFORMATION
-------------------------------------------------------------------------

If an indicator algorithm contains bugs, an error message and description
will be displayed in the indicator field and in Java Console.

Remember however, that error messages may contain the following
inaccuracies (due to the limitations of JavaScript and applet
collaboration):
- if you use Microsoft Internet Explorer then the information regarding
  line numbers and error positions may be incorrect. This is because the
  indicators' code is transformed to a single line before evaluation.
-------------------------------------------------------------------------
Internet Explorer is a registered trademark of Microsoft Corporation.
Netscape Navigator is a registered trademark of Netscape Communications
Corporation.
Java and JavaScript are registered trademarks of Sun Microsystems
Corporation.
-------------------------------------------------------------------------
