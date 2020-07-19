TWENTY_FOUR_WEEKS_GESTATION = round((-((40 * 7)/365.25) - ((24 * 7)/365.25)), 9)
TWENTY_FIVE_WEEKS_GESTATION = round((-((40 * 7)/365.25) - ((25 * 7)/365.25)), 9)
FORTY_WEEKS_GESTATION = 0
FORTY_TWO_WEEKS_GESTATION =   round(((42 * 7)/365.25 - ((40 * 7)/365.25)), 9)
THIRTY_SEVEN_WEEKS_GESTATION = round((((37 * 7)-(40 * 7))/365.25), 9)
TERM_PREGNANCY_LENGTH_DAYS = 40 * 7
TERM_LOWER_THRESHOLD_LENGTH_DAYS = 37 * 7
EXTREME_PREMATURITY_THRESHOLD_LENGTH_DAYS = 32 * 7

"""
Debate here: cf issue #51
LMSGrowth, our current gold standard, written in visual basic for Excel by Pan Huiqi and Tim Cole does not 
agree with RCPCHGrowth beyond ~6 decimal places.On reexamining the original LMS Growth code reasons for this are not clear.

The difficulty with floating point numbers is that these constants, which act as cut offs often between references,
 at 16 dp may be more accurate than the ages supplied. For example, calculating decimal ages from 2 dates, where days are
 whole integers, 14 days for example may actually calculate out to 13.999999999999998.

 For this reason, constants have been rounded to 9 dp, ensuring that any cut offs should be respected.
"""