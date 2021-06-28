import {ChartTheme, ChartObject, GridlineObject, CentilesObject, MeasurementsObject, AxesObject, TextStyleObject, PaddingObject} from './themes'

/* 
Theme 1

Data:  #7159aa - purple
Area:  #c6bddd - purple (tint 40%)
tooltip: #fdc300 - yellow

gridlines: #d9d9d9 - light grey
text: #000000 - black
background colour: #FFFFFF - white
centile width: 1.5 px

font: Montserrat regular

*/

const centileColour = "#7159aa"
const pubertyFill = "#c6bddd"
const tooltipBackGroundColour = "#fdc300"
// const tooltipTextColour = "#FFFFFF"
const gridlineColour = "#d9d9d9"
const gridlineWidth = 0.25
const backgroundColour = "#FFFFFF"
const centileWidth = 1.5
// const axisLabelColour = "#000000"
const axisstroke = "#000000"
const measurementsFill = "#000000"
const measurementsStroke= "#000000"
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
    "#000000",
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
     tooltipBackGroundColour,
     tooltipBackGroundColour,
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

const RCPCHTheme1 = new ChartTheme(RCPCHChart, RCPCHGridlines, RCPCHAxes, RCPCHCentiles, RCPCHMeasurements)

export default RCPCHTheme1