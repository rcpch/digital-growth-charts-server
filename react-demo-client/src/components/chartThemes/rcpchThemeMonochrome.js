import {ChartTheme, ChartObject, GridlineObject, CentilesObject, MeasurementsObject, AxesObject, TextStyleObject, PaddingObject} from './themes'

/* 
Theme 4 - monochrome

Data:   #000000 - black
Area:   #b3b3b3 - midgrey
tooltip: #FFFFF - white

gridlines: #d9d9d9 - light grey
text: #000000 - black
background colour: #FFFFFF - white
centile width: 1.5 px

font: Montserrat regular
 
*/

const centileColour = "#000000"
const pubertyFill = "#b3b3b3"
const tooltipBackgroundColour = "#b3b3b3"
const tooltipTextColour = "#000000"
const gridlineColour = "#d9d9d9"
const gridlineWidth = 0.25
const backgroundColour = "#FFFFFF"
const centileWidth = 1.5

const axisstroke = "#000000"
const measurementsFill = "#000000"
const measurementsStroke = "#000000"
const measurementsSize = 2

const titleStyle = new TextStyleObject(
   "Arial",
   "#000000",
   12,
   'bold'
)
const subTitleStyle = new TextStyleObject(
   "Arial",
   "#000000",
   10,
   'regular'
)

const tooltipTextStyle = new TextStyleObject(
   "Montserrat",
   tooltipTextColour,
   0.25,
   "regular"
)
const infoBoxTextStyle = new TextStyleObject(
   "Montserrat",
   "#000000",
   6,
   "regular"
)

const axisLabelTextStyle = new TextStyleObject(
   "Arial",
   "000000",
   10,
   'regular'
)
const tickLabelTextStyle = new TextStyleObject(
   "Arial",
   "000000",
   8,
   'regular'
)

const chartPadding = new PaddingObject(
   50,
   50,
   50,
   50
)

const RCPCHChart = new ChartObject(
    backgroundColour,
    700,
    500,
    chartPadding,
    titleStyle,
    subTitleStyle,
    tooltipBackgroundColour,
    tooltipBackgroundColour,
    tooltipTextStyle,
    "#CDCDCD",
    "#CDCDCD",
    "#CDCDCD",
    "#CDCDCD",
   infoBoxTextStyle,
   '#E497C1',
   "#cb3083",
   "#FFFFFF"
)



const RCPCHGridlines = new GridlineObject(
   true,
   gridlineColour,
   gridlineWidth,
   false
)

const RCPCHCentiles = new CentilesObject(
   centileColour,
   centileWidth,
   pubertyFill
)

const RCPCHAxes = new AxesObject(
   axisstroke,
   axisLabelTextStyle,
   tickLabelTextStyle
)

const RCPCHMeasurements = new MeasurementsObject(
   measurementsFill,
   measurementsStroke,
   measurementsSize,
)

const RCPCHThemeMonochrome = new ChartTheme(RCPCHChart, RCPCHGridlines, RCPCHAxes, RCPCHCentiles, RCPCHMeasurements)
export default RCPCHThemeMonochrome