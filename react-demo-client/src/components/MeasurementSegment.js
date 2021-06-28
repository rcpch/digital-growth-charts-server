// React
import React, { useState, useEffect } from 'react';
import RCPCHTheme1 from '../components/chartThemes/rcpchTheme1';
import RCPCHTheme2 from '../components/chartThemes/rcpchTheme2';
import RCPCHTheme3 from '../components/chartThemes/rcpchTheme3';
import RCPCHThemeMonochrome from '../components/chartThemes/rcpchThemeMonochrome';
import RCPCHThemeTraditionalBoy from '../components/chartThemes/RCPCHThemeTraditionalBoy';
import RCPCHThemeTraditionalGirl from '../components/chartThemes/RCPCHThemeTraditionalGirl';

// Semantic UI React
import {
  Grid,
  Segment,
  Message,
  Flag,
  Tab,
  Dropdown,
  Button,
  Table,
  List
} from 'semantic-ui-react';
import ChartData from '../api/Chart';
import MeasurementForm from '../components/MeasurementForm';
import '../index.css';

import axios from 'axios';

function MeasurementSegment() {
  
  const defaultTheme = RCPCHThemeMonochrome;

  const [measurementMethod, setMeasurementMethod] = useState('height');
  const [reference, setReference] = useState('uk-who');
  const [sex, setSex] = useState('male');
  const [chartStyle, setChartSyle] = useState(defaultTheme.chart);
  const [axisStyle, setAxisStyle] = useState(defaultTheme.axes);
  const [centileStyle, setCentileStyle] = useState(defaultTheme.centiles);
  const [gridlineStyle, setGridlineStyle] = useState(defaultTheme.gridlines);
  const [measurementStyle, setMeasurementStyle] = useState(
    defaultTheme.measurements
  );
  const [heights, setHeights] = useState([]);
  const [weights, setWeights] = useState([]);
  const [ofcs, setOfcs] = useState([]);
  const [bmis, setBmis] = useState([]);

  const [theme, setTheme] = useState({
    value: 'tanner4',
    text: 'Monochrome',
  });
  const [activeIndex, setActiveIndex] = useState(0); //set tab to height
  const [flip, setFlip] = useState(false); // flag to determine if results or chart showing
  const [heightDisabled, setHeightDisabled] = useState(false);
  const [weightDisabled, setWeightDisabled] = useState(false);
  const [bmiDisabled, setBMIDisabled] = useState(false);
  const [ofcDisabled, setOFCDisabled] = useState(false);
  const [apiResult, setAPIResult] = useState({
    height: [],
    weight: [],
    bmi: [],
    ofc: [],
  });
  const [currentMeasurements, setCurrentMeasurements] = useState([]);

  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchCentilesForMeasurement = async (array) => {
      let url;
      if (reference === 'uk-who') {
        url = `${process.env.REACT_APP_GROWTH_API_BASEURL}/uk-who/calculation`;
      }
      if (reference === 'turner') {
        url = `${process.env.REACT_APP_GROWTH_API_BASEURL}/turner/calculation`;
      }
      if (reference === 'trisomy-21') {
        url = `${process.env.REACT_APP_GROWTH_API_BASEURL}/trisomy-21/calculation`;
      }

      const results = array.map(async (payload) => {
        const response = await axios({
          url: url,
          data: payload,
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        return response.data;
      });

      return Promise.all(results);
    };

    let ignore = false; // this prevents data being added to state if unmounted

    let submitArray = [];

    switch (measurementMethod) {
      case 'height':
        setCurrentMeasurements(heights);
        submitArray = heights;
        break;
      case 'weight':
        setCurrentMeasurements(weights);
        submitArray = weights;
        break;
      case 'bmi':
        setCurrentMeasurements(bmis);
        submitArray = bmis;
        break;
      case 'ofc':
        setCurrentMeasurements(ofcs);
        submitArray = ofcs;
        break;
      default:
        console.error(
          'No valid active index picked up when preparing results to server fetch'
        );
    }

    if (isLoading) {
      if (submitArray.length > 0) {
        fetchCentilesForMeasurement(submitArray).then((final) => {
          if (final.length > 0 && !ignore) {
            const orderedFinal = final.sort((a, b) =>
              a.measurement_dates.corrected_decimal_age <
              b.measurement_dates.corrected_decimal_age
                ? 1
                : -1
            );
            setIsLoading(false);
            setAPIResult((prevState) => ({
              ...prevState,
              ...{ [measurementMethod]: orderedFinal },
            }));
          }
        });
      } else {
        return;
      }
    }

    return () => {
      // this prevents data being added to state if unmounted
      ignore = true;
    };
  }, [
    isLoading,
    measurementMethod,
    reference,
    apiResult,
    heights,
    weights,
    ofcs,
    bmis,
    currentMeasurements,
  ]);

  const handleTabChange = (e, { activeIndex }) => setActiveIndex(activeIndex);

  const changeReference = (reference) => {
    // call back from MeasurementForm
    setReference(reference);
    if (reference === 'turner') {
      setMeasurementMethod('height');
      setSex('female');
      setHeightDisabled(false);
      setWeightDisabled(true);
      setBMIDisabled(true);
      setOFCDisabled(true);
    }
    if (reference === 'trisomy-21') {
      setHeightDisabled(false);
      setWeightDisabled(false);
      setBMIDisabled(false);
      setOFCDisabled(true);
    }
    if (reference === 'uk-who') {
      setHeightDisabled(false);
      setWeightDisabled(false);
      setBMIDisabled(false);
      setOFCDisabled(false);
    }
  };

  const changeSex = (sex) => {
    // call back from MeasurementForm
    setSex(sex);
    let selectedTheme;
    if (reference === 'uk-who') {
      if (sex === 'male') {
        selectedTheme = RCPCHThemeTraditionalBoy;
      } else {
        selectedTheme = RCPCHThemeTraditionalGirl;
      }
      setCentileStyle(selectedTheme.centiles);
      setChartSyle(selectedTheme.chart);
      setMeasurementStyle(selectedTheme.measurements);
      setAxisStyle(selectedTheme.axes);
      setGridlineStyle(selectedTheme.gridlines)
      setTheme({ value: 'tanner1', text: 'Tanner 1' });
    }
  };

  const changeMeasurement = (measurementMethod) => {
    // call back from MeasurementForm
    switch (measurementMethod) {
      case 'height':
        setActiveIndex(0); // move focus to height tab
        break;
      case 'weight':
        setActiveIndex(1); // move focus to weight tab
        break;
      case 'bmi':
        setActiveIndex(2); // move focus to bmi tab
        break;
      case 'ofc':
        setActiveIndex(3); // move focus to ofc tab
        break;
      default:
        return;
    }
    setMeasurementMethod(measurementMethod);
  };

  const handleResults = (results) => {
    // delegate function from MeasurementForm
    // receives form data and stores in the correct measurement array
    // this will trigger a rerender

    let concatenated;
    switch (measurementMethod) {
      case 'height':
        concatenated = heights.concat(results);
        setActiveIndex(0); // move focus to height tab
        setHeights(concatenated);
        break;
      case 'weight':
        concatenated = weights.concat(results);
        setActiveIndex(1); // move focus to weight tab
        setWeights(concatenated);
        break;
      case 'bmi':
        concatenated = bmis.concat(results);
        setBmis(concatenated);
        setActiveIndex(2); // move focus to bmi tab
        break;
      case 'ofc':
        concatenated = ofcs.concat(results);
        setOfcs(concatenated);
        setActiveIndex(3); // move focus to ofc tab
        break;
      default:
      //
    }
    setIsLoading(true);
  };

  const returnNewChart = (
    Sex,
    MeasurementMethod,
    MeasurementsArray,
    ChartStyle,
    AxisStyle,
    GridlineStyle,
    CentileStyle,
    MeasurementStyle
  ) => {
    const Chart = (
      <ChartData
        key={MeasurementMethod + '-' + reference}
        reference={reference} //the choices are ["uk-who", "turner", "trisomy-21"] REQUIRED
        sex={Sex} //the choices are ["male", "female"] REQUIRED
        measurementMethod={MeasurementMethod} //the choices are ["height", "weight", "ofc", "bmi"] REQUIRED
        measurementsArray={MeasurementsArray} // an array of Measurement class objects from dGC Optional
        chartStyle={ChartStyle}
        axisStyle={AxisStyle}
        gridlineStyle={GridlineStyle}
        centileStyle={CentileStyle}
        measurementStyle={MeasurementStyle}
      />
    );
    return Chart;
  };

  const handleChangeTheme = (event, { value }) => {
    let selectedTheme;
    let text;

    if (value === 'trad') {
      if (sex === 'male') {
        selectedTheme = RCPCHThemeTraditionalBoy;
      } else {
        selectedTheme = RCPCHThemeTraditionalGirl;
      }
      text = 'Traditional';
    }
    if (value === 'tanner1') {
      selectedTheme = RCPCHTheme1;
      text = 'Tanner 1';
    }
    if (value === 'tanner2') {
      selectedTheme = RCPCHTheme2;
      text = 'Tanner 2';
    }
    if (value === 'tanner3') {
      selectedTheme = RCPCHTheme3;
      text = 'Tanner 3';
    }
    if (value === 'monochrome') {
      selectedTheme = RCPCHThemeMonochrome;
      text = 'Monochrome';
    }

    setCentileStyle(selectedTheme.centiles);
    setChartSyle(selectedTheme.chart);
    setMeasurementStyle(selectedTheme.measurements);
    setAxisStyle(selectedTheme.axes);
    setTheme({ value: value, text: text });
  };

  const handleFlipResults = () => {
    setFlip(!flip);
  };

  const units = (measurementMethod) => {
    if (measurementMethod === 'height') {
      return 'cm';
    }
    if (measurementMethod === 'weight') {
      return 'kg';
    }
    if (measurementMethod === 'bmi') {
      return 'kg/m²';
    }
    if (measurementMethod === 'ofc') {
      return 'cm';
    }
  };

  const Acknowledgements = () => {
    // list={["Freeman JV, Cole TJ, Chinn S, Jones PRM, White EM, Preece MA. Cross sectional stature and weight reference curves for the UK, 1990. Arch Dis Child 1995; 73:17-24.", "<a href='www.who.int/childgrowth/en'>www.who.int/childgrowth/en</a>", "For further relevant references see fact sheet downloadable from www.growthcharts.RCPCH.ac.uk"]}
    return (
      <Message>
        <Message.Header>References</Message.Header>
        <List>
          <List.Item>
            Freeman JV, Cole TJ, Chinn S, Jones PRM, White EM, Preece MA. Cross
            sectional stature and weight reference curves for the UK, 1990. Arch
            Dis Child 1995; 73:17-24.
          </List.Item>
          <List.Item>
            <a href="www.who.int/childgrowth/en">www.who.int/childgrowth/en</a>
          </List.Item>
          <List.Item>
            For further relevant references see fact sheet downloadable from{' '}
            <a href="www.growthcharts.RCPCH.ac.uk">
              www.growthcharts.RCPCH.ac.uk
            </a>
          </List.Item>
        </List>
      </Message>
    );
  };

  const panes = [
    {
      menuItem: 'Height',
      render: () => (
        <Tab.Pane attached={'top'} disabled={heightDisabled}>
          {returnNewChart(
            sex,
            'height',
            apiResult.height,
            chartStyle,
            axisStyle,
            gridlineStyle,
            centileStyle,
            measurementStyle
          )}
          <Acknowledgements />
        </Tab.Pane>
      ),
    },
    {
      menuItem: 'Weight',
      render: () => (
        <Tab.Pane attached={'top'} disabled={weightDisabled}>
          {returnNewChart(
            sex,
            'weight',
            apiResult.weight,
            chartStyle,
            axisStyle,
            gridlineStyle,
            centileStyle,
            measurementStyle
          )}
          <Acknowledgements />
        </Tab.Pane>
      ),
    },
    {
      menuItem: 'BMI',
      render: () => (
        <Tab.Pane attached={'top'} disabled={bmiDisabled}>
          {returnNewChart(
            sex,
            'bmi',
            apiResult.bmi,
            chartStyle,
            axisStyle,
            gridlineStyle,
            centileStyle,
            measurementStyle
          )}
          <Acknowledgements />
        </Tab.Pane>
      ),
    },
    {
      menuItem: 'Head Circumference',
      render: () => (
        <Tab.Pane attached={'top'} disabled={ofcDisabled}>
          {returnNewChart(
            sex,
            'ofc',
            apiResult.ofc,
            chartStyle,
            axisStyle,
            gridlineStyle,
            centileStyle,
            measurementStyle
          )}
          <Acknowledgements />
        </Tab.Pane>
      ),
    },
  ];

  const TabPanes = () => (
    <Tab
      menu={{ attached: 'top' }}
      panes={panes}
      activeIndex={activeIndex}
      onTabChange={handleTabChange}
    />
  );

  const themeOptions = [
    { key: 'trad', value: 'trad', text: 'Traditional' },
    { key: 'tanner1', value: 'tanner1', text: 'Tanner 1' },
    { key: 'tanner2', value: 'tanner2', text: 'Tanner 2' },
    { key: 'tanner3', value: 'tanner3', text: 'Tanner 3' },
    { key: 'monochrome', value: 'monochrome', text: 'Monochrome' },
  ];

  const ThemeSelection = () => (
    // <Menu compact className="selectUpperMargin">
    <span>
      Theme{' '}
      <Dropdown
        options={themeOptions}
        floating
        inline
        onChange={handleChangeTheme}
        text={theme.text}
      />
    </span>
    // </Menu>
  );

  const ResultsSegment = () => (
    <Segment>
      <Table basic="very" celled collapsing compact>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell></Table.HeaderCell>
            <Table.HeaderCell>
              Corrected Results
            </Table.HeaderCell>
            <Table.HeaderCell>
              Chronological Results
            </Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {apiResult.height.length > 0 &&
            <Table.Row>
              <Table.HeaderCell></Table.HeaderCell>
              <Table.HeaderCell>Heights</Table.HeaderCell>
              <Table.HeaderCell></Table.HeaderCell>
            </Table.Row>
          }
        {apiResult.height.length > 0 && apiResult.height.map((measurement, index) => {
          return <TableBody
            measurement={measurement}
            key={index}
          />
        })}
        {apiResult.weight.length > 0 &&
            <Table.Row>
              <Table.HeaderCell></Table.HeaderCell>
              <Table.HeaderCell>Weights</Table.HeaderCell>
              <Table.HeaderCell></Table.HeaderCell>
            </Table.Row>
          }
        {apiResult.weight.length > 0 && apiResult.weight.map((measurement, index) => {
          return (
            <TableBody 
              key={index} 
              measurement={measurement}/>
          );
        })}
        {apiResult.bmi.length > 0 &&
            <Table.Row>
              <Table.HeaderCell></Table.HeaderCell>
              <Table.HeaderCell>BMIs</Table.HeaderCell>
              <Table.HeaderCell></Table.HeaderCell>
            </Table.Row>
          }
        {apiResult.bmi.length > 0 && apiResult.bmi.map((measurement, index) => {
          return (
            <TableBody 
              key={index} 
              measurement={measurement}/>
          );
        })}
        {apiResult.ofc.length > 0 &&
            <Table.Row>
              <Table.HeaderCell></Table.HeaderCell>
              <Table.HeaderCell>Head Circumferences</Table.HeaderCell>
              <Table.HeaderCell></Table.HeaderCell>
            </Table.Row>
        }
        {apiResult.ofc.length > 0 && apiResult.ofc.map((measurement, index) => {
          return (
            <TableBody 
              key={index}
              measurement={measurement}
            />
          );
        })}
        </Table.Body>
      </Table>
    </Segment>
  );

  const TableBody = (props) => {
      const measurement = props.measurement
      return  (<>
                <Table.Row>
                  <Table.Cell>Ages</Table.Cell>
                  <Table.Cell>{measurement.measurement_dates.chronological_calendar_age}</Table.Cell>
                  <Table.Cell>
                  {measurement.measurement_dates.corrected_calendar_age}
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                <Table.Cell>Measurement</Table.Cell>
                  <Table.Cell>{measurement.child_observation_value.observation_value}{' '}
                  {units(measurement.child_observation_value.measurement_method)}
                  </Table.Cell>
                  <Table.Cell>
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>SDS</Table.Cell>
                  <Table.Cell>
                    {Math.round(
                      measurement.measurement_calculated_values.corrected_sds *
                        1000
                    ) / 1000}
                  </Table.Cell>
                  <Table.Cell>
                    {Math.round(
                      measurement.measurement_calculated_values.chronological_sds *
                        1000
                    ) / 1000}
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>Centiles</Table.Cell>
                  <Table.Cell>
                    {measurement.measurement_calculated_values.corrected_centile}
                  </Table.Cell>
                  <Table.Cell>
                    {measurement.measurement_calculated_values.chronological_centile}
                  </Table.Cell>
                </Table.Row>
              </>)
  }

  return (
    <Grid padded>
      <Grid.Row>
        <Grid.Column width={6}>
          <Grid.Row>
            <Segment raised>
              <MeasurementForm
                measurementResult={handleResults}
                handleChangeReference={changeReference}
                handleChangeSex={changeSex}
                handleChangeMeasurementMethod={changeMeasurement}
                className="measurement-form"
              />
            </Segment>
          </Grid.Row>
          <Grid.Row>
            <Grid.Column width={5}>
              <Segment raised>
                <Message>
                  <Flag name="gb" />
                  This calculator uses the UK-WHO references to calculate gold
                  standard accurate child growth parameters. In the future we
                  are planning to add other growth references such as specialist
                  Trisomy 21 and Turner's Syndrome references, CDC and WHO.
                </Message>

                <Message color="red">
                  This site is under development. No responsibility is accepted
                  for the accuracy of results produced by this tool.
                </Message>
              </Segment>
            </Grid.Column>
          </Grid.Row>
        </Grid.Column>
        <Grid.Column width={10}>
          <Segment raised>
            {flip ? (
              <ResultsSegment selectedMeasurement={measurementMethod} />
            ) : (
              <TabPanes />
            )}
            <Grid verticalAlign="middle">
              <Grid.Row columns={2}>
                <Grid.Column textAlign="left">
                  <ThemeSelection />
                </Grid.Column>
                <Grid.Column textAlign="right">
                  <Button
                    className="selectUpperMargin"
                    onClick={handleFlipResults}
                  >
                    Results
                  </Button>
                </Grid.Column>
              </Grid.Row>
            </Grid>
          </Segment>
        </Grid.Column>
      </Grid.Row>
    </Grid>
  );
}

export default MeasurementSegment;