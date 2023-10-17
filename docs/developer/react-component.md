---
title: React Chart Component
reviewers: Dr Marcus Baw, Dr Simon Chapman, Dr Anchit Chandran
audience: developers
---

# React Chart Component

{% set repository_name="rcpch/digital-growth-charts-react-component-library" -%}

[![Github Issues](https://img.shields.io/github/issues/{{ repository_name }})](https://github.com/{{ repository_name }}/issues)
[![Github Stars](https://img.shields.io/github/stars/{{ repository_name }})](https://github.com/{{ repository_name }}/stargazers)
[![Github Forks](https://img.shields.io/github/forks/{{ repository_name }})](https://github.com/{{ repository_name }}/network/members)
[![Github Licence](https://img.shields.io/github/license/{{ repository_name }})](https://github.com/{{ repository_name }}/blob/live/LICENSE)
[![NPM Publish](https://github.com/{{ repository_name }}/actions/workflows/main.yml/badge.svg)](https://github.com/{{ repository_name }}/actions/workflows/main.yml)

[:octicons-mark-github-16: GitHub repository](https://github.com/{{ repository_name }})

[:material-web: Online Demo](https://growth.rcpch.ac.uk/)

![height-chart-girl-component](../_assets/_images/height-chart-girl-component.png)

!!! success "Use our Growth Chart React Component"
    The dGC React Component is the recommended way to display Digital Growth Charts to end users. We have built the component to be easy to integrate into existing web-based views, even if your stack does not currently use React. You can use the component as-is in a React app, or include it in plain HTML or any other JavaScript framework.

    Displaying growth charts is a complex task, and we have built the component to make it as easy as possible for developers to display charts correctly. The component is designed to be customisable, so you can change the look and feel to match your app.

## Background

### React.js

React is a popular UI library for Javascript. It has endured well and remains a popular choice for developers. Importantly, unlike some other Javascript frameworks which are primarily designed for Single Page Applications, React doesn't expect to have the entire webpage to itself. It can be used as a small component in any other web page, even if the main framework being used is completely different.

!!! question "Tell us what you think"
    Let us know what you think of our design decisions, on this or any other area of the dGC Project, by chatting to us on our [dGC Forum](https://openhealthhub.org/c/rcpch-digital-growth-charts/) :fontawesome-brands-discourse:, or our RCPCH Community [Signal chat channel :fontawesome-brands-signal:](https://signal.group/#CjQKIAjLf5lS9OZIAI6lsJKWP1LmeJXkUW_fzZH1ryEw3oFEEhBH-4F7WnlyYjKerjfzD6B0)

### What about other frameworks/UI libraries?

If you need us to develop a charting component in a different language or framework, we may be able to do this with you or your company. We would need to discuss the requirements and quote for this service. You should be aware that all such RCPCH-developed artefacts will also be open source. We ensure the licensing of open source components is compatible with commercial use.

!!! note "Contact us"
    To contact us for this service, email <mailto:commercial@rcpch.ac.uk>.

## Getting started

`git clone` the repo
```console
git clone https://github.com.rcpch/{{ repository_name }}
```

Install dependencies
```console
npm install
```

Run Storybook to view the component in isolation
```console
npm run storybook
```

### Running the Charts Package locally

To run the package locally alongside the React client, there are some extra steps. Since the Chart library and the React client both use React, the Charts will throw an error if you import them in the ```package.json``` of your app from a folder on your local machine.

For example, in your React app:

```json
"dependencies": {
    "@rcpch/digital-growth-charts-react-component-library": "file:/Users/FooBar/Development/react/component-libraries/digital-growth-charts-react-component-library",
}
```

This causes a problem as it leads to 2 versions of React running. To overcome this, in your application:

```console
cd node_modules/react
npm link
```

In the root folder of your Chart library:

```console
npm link react
```

Repeat the same for ```react-dom``` ensuring all the package versions are the same for your app and the library. The library currently uses version `17.0.2` of React and React-dom.

Now, you can view your changes made live in your app:

```console
npm run build
```

Refresh your app.

If the invalid hooks error persists, an alternative method is to add the following line to ```package.json``` in the library. This removes the node_modules from the build folder:

```json
"scripts": {
        "postinstall": "rm -rf node_modules",
        ...
    },
```

## Structure

This library has been written in Typescript. The main component is `RCPCHChart`, which takes the following `props`. Note that each component will only render a single chart type, so if you wanted to render a weight *and* a height chart, these must be done as two separate instances of the component. We find that on modern screens you can render two charts side-by-side, but on smaller screens, you may wish to render one chart at a time, perhaps in tabs for height, weight, BMI, head circumference etc, as in our [demo client](https://growth.rcpch.ac.uk/).

### RCPCHChart component

??? note "`RCPCHChart` component props"
    ```js
    {
    title: string,
    subtitle: string,
    measurementMethod: 'height' | 'weight' | 'ofc' | 'bmi',
    sex: 'male' | 'female',
    measurementsArray: [Measurement],
    reference: 'uk-who' | 'turner' | 'trisomy-21',
    width: number,
    height: number,
    chartStyle: ChartStyle,
    axisStyle: AxisStyle,
    gridlineStyle: GridlineStyle,
    centileStyle: CentileStyle,
    sdsStyle?: SDSStyle;
    measurementStyle: MeasurementStyle
    midParentalHeightData?: MidParentalHeightObject,
    enableZoom?: boolean,
    chartType?: 'centile' | 'sds',
    enableExport: boolean,
    exportChartCallback: function(svg: any),
    clinicianFocus?: boolean;
    }
    ```

### Measurement interface

The `Measurement` interface is structured to reflect the JSON `Measurement` object which is returned by the API. The `RCPCHChart` component uses the `reference` prop to determine which chart to render. So far, 3 references are supported: UK-WHO (`uk-who`), Turner Syndrome (`turner`) and Down Syndrome (`trisomy-21`). The reference data for the centiles are included in the library in plottable format in the `chartdata` folder.

!!! tip
    **You simply need to pass JSON from the dGC API directly in to the component asan array of `Measurement` JSON objects. The component 'knows' how to render this correctly. You don't need to parse, restructure, or even understand the JSON returned from the API: just pass it directly to the component inside an array containing one or more `Measurement` objects.**

## Styling

The styling components allow the user to customise elements of the chart. Chart styles control the chart and the tooltips.

!!! note "Styling options available through `ChartStyle`"
    ```js
    interface ChartStyle{
        backgroundColour?: string,
        width?: number,
        height?: number,
        padding?: requires {left?: number, right?: number, top?: number, bottom?: number},
        titleStyle?: requires {name?: string, colour?: string, size?: number, weight?: 'bold' | 'italic' | 'regular'}
        subTitleStyle?: requires {name?: string, colour?: string, size?: number, weight?: 'bold' | 'italic' | 'regular'},,
        tooltipBackgroundColour?: string,
        tooltipStroke?: string,
        tooltipTextStyle?: requires {name?: string, colour?: string, size?: number, weight?: 'bold' | 'italic' | 'regular'}
        termFill?: string,
        termStroke?: string,
        infoBoxFill?: string,
        infoBoxStroke?: string
        infoBoxTextStyle?: requires {name?: string, colour?: string, size?: number, weight?: 'bold' | 'italic' | 'regular'}
        toggleButtonInactiveColour: string // relates to the toggle buttons present if age correction is necessary
        toggleButtonActiveColour: string
        toggleButtonTextColour: string
    }
    ```

Note for the tooltips and infobox text sizes, these are strokeWidths, not point sizes as the text here is SVG.

### Axis Styles

??? note "Axis styles control axes and axis labels"
    ```js
    interface AxisStyle{
        axisStroke?: string,
        axisLabelTextStyle?: requires {name?: string, colour?: string, size?: number, weight?: 'bold' | 'italic' | 'regular'}
        tickLabelTextStyle?: requires {name?: string, colour?: string, size?: number, weight?: 'bold' | 'italic' | 'regular'}
    }
    ```

### Gridline Styles

??? note "Gridline styles allow/hide gridlines and control line width, presence of dashes, colour"
    ```js
    interface GridlineStyle{
        gridlines?: boolean,
        stroke?: string,
        strokeWidth?: number,
        dashed?: boolean
    }
    ```

### Centile Styles

??? note "Centile styles control the width and colour of the centile and SDS lines"
    ```js
    interface CentileStyle{
        sdsStroke?: string,
        sdsStrokeWidth?: string,
        centileStroke?: string,
        centileStrokeWidth?: number,
        delayedPubertyAreaFill?: string,
        midParentalCentileStroke?: number;
        midParentalCentileStrokeWidth?: number;
        midParentalAreaFill?: string;
    }
    ```

### SDS Styles

SDS styles control the colour and width of the SDS lines. As all measurement methods are rendered on a single chart, the user is offered the option of different colours for each measurement method (height, weight, head circumference(OFC) and body mass index (BMI)). If no SDS style is supplied, the centile line colour is used with an opacity applied to each measurement.

??? note "SDS Styles"
    ```js
    interface SDSStyle {
        lineStrokeWidth?: number;
        heightStroke?: string;
        weightStroke?: string;
        ofcStroke?: string;
        bmiStroke?: string;
    }
    ```

### Measurement Styles

Measurement styles control the plotted data points: colour, size and shape. Corrected ages are always rendered as crosses. Circles for chronological ages are preferred. On the SDS charts, measurement points are grey by default, with the measurement method in focus highlighted by rendering as a line. Points which are not highlighted can be emphasised on mouse hover, with the highlighted colour being set by the `highlightedMeasurementFill` prop.

??? note "Measurement Styles"
    ```js
    interface MeasurementStyle{
        measurementFill?: string,
        highLightedMeasurementFill?: string;
    }
    ```

### Mid-Parental Height

`midParentalHeightData`: This is the return value from the RCPCH API and takes the structure:

??? note "`midParentalHeightData`"
    ```js
    export interface MidParentalHeightObject {
        mid_parental_height?: number;
        mid_parental_height_sds?: number;
        mid_parental_height_centile?: number;
        mid_parental_height_centile_data?: Reference[]
        mid_parental_height_upper_centile_data?: Reference[]
        mid_parental_height_lower_centile_data?: Reference[]
        mid_parental_height_lower_value?: number
        mid_parental_height_upper_value?: number
    }
    ```

This returns a mid-parental height, mid-parental SDS and centile, along with the centile data if the user wishes to plot a mid-parental centile. The structure of the Reference and Centile interfaces is:

??? note "`Reference` and `Centile` interface structures"
    ```js
    export interface Reference {
        [name: string]: ISexChoice
    }

    export interface ICentile {
        centile: number,
        data: IPlottedCentileMeasurement[],
        sds: number
    }

    export interface IPlottedCentileMeasurement {
        "l": string | number,
        "x": number,
        "y": number
    }

    export interface ISexChoice {
        male: IMeasurementMethod,
        female: IMeasurementMethod
    }

    export interface IMeasurementMethod{
        height?: ICentile[],
        weight?: ICentile[],
        bmi?: ICentile[],
        ofc?: ICentile[],
    }
    ```

Centile data are returned from the RCPCH API in this same structure, though no API call is made from this component - all the centile data for all the references is included.

### `enableZoom`

```enableZoom```: a boolean optional prop which defaults to false. If true, the user can press and mouse click to zoom in or out once measurements are being displayed. A reset zoom button also appears.

### `chartType`

```chartType```: a string mandatory prop and must be one of ```'centile' | 'sds'```. It toggles between centile and SDS charts.

### `enableExport`

```enableExport```: a boolean optional prop, defaults to false. If true, ```exportChartCallback``` must be implemented and a copy-paste button is rendered below the chart.

### `exportChartCallBack`

```exportChartCallback``` callback function implemented if `enableExport` is true. It receives an SVG element. This can be saved in the client to clipboard by converting to canvas using HTML5. An example implementation of this is [here](https://github.com/rcpch/digital-growth-charts-react-client/blob/live/src/functions/canvasFromSVG.js) in our demo client.

### `clinicianFocus`

```clinicianFocus```: a boolean optional prop which defaults to false. If true, the advice strings that are reported to users in tooltips are more technical and aimed at clinicians familiar with centile charts. If false, the advice strings will be less technical and more suitable for parents, guardians, carers or other laypersons.

!!! example "Requests for additional functionality in props"
    In time, more props can be added if users request them. If you have requests, please post issues on our [GitHub](https://github.com/rcpch/digital-growth-charts-react-component-library/issues) or get involved to contribute as below.

## Troubleshooting

### Circular import errors

Victory Charts are a dependency (see below), built on top of D3.js. On build, it is likely you will get an error relating to circular dependencies for some files in the d3-interpolate module. This issue is logged [here](https://github.com/d3/d3-interpolate/issues/58).

## Contributing

See [Contributing](../developer/contributing.md) for information on how to get involved in the project.

You can get in touch with the primary developers to talk about the project using any of the methods on our [contact page](../about/contact.md).

## Acknowledgements

This Typescript library was built from the starter created by [Harvey Delaney](https://blog.harveydelaney.com/creating-your-own-react-component-library/)

The charts are built using [Victory Charts](https://formidable.com/open-source/victory/docs/victory-chart/) for React. We tried several chart packages for React, but we chose Victory because of their documentation and their ability to customise components.

## Licensing

This chart component software is is subject to copyright and is owned by the RCPCH, but is released under the MIT license.
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

There is important chart line rendering data bundled in the component, which subject to copyright and is owned by the RCPCH. It is specifically excluded from the MIT license mentioned above. If you wish to use this software, please [contact the RCPCH](../about/contact.md) so we can ensure you have the correct license for use. Subscribers to the Digital Growth Charts API will automatically be assigned licenses for the chart plotting data.
