import {ChartTheme, ChartObject, GridlineObject, CentilesObject, MeasurementsObject, AxesObject, TextStyleObject, PaddingObject} from './themes'

/* 
Traditional: girl

// girl 201 85 157 - #c9559d

Data:   #c9559d - pink
Area:   df99c4 - pink tint 40%
tooltip: #b3b3b3 - midgrey

gridlines: #d9d9d9 - light grey
text: #000000 - black
background colour: #FFFFFF - white
centile width: 1.5 px

font: Montserrat regular

*/

const centileColour = "#c9559d"
const pubertyFill = "#df99c4"
const tooltipBackgroundColour = "#df99c4"
const tooltipTextColour = "#000000"
const gridlineColour = "#d9d9d9"
const gridlineWidth = 0.25
const backgroundColour = "#FFFFFF"
const centileWidth = 1.5
// const axisLabelColour = "#000000"
const axisstroke = "#000000"
const measurementsFill = "#000000"
const measurementsStroke = '#000000'
const measurementsSize = 2
// const axisLabelSize = 10
// const tickLabelSize = 8
// const axisLabelFont = "Montserrat"


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
    tooltipBackgroundColour,
    tooltipBackgroundColour,
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

const RCPCHThemeTraditionalGirl = new ChartTheme(RCPCHChart, RCPCHGridlines, RCPCHAxes, RCPCHCentiles, RCPCHMeasurements)

export default RCPCHThemeTraditionalGirl