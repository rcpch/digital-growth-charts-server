import React from 'react';

import {
  Container,
  Segment,
  Form,
  Input,
  Select,
  Button,
  Header,
  Message,
  Modal,
} from 'semantic-ui-react';

const sexOptions = [
  { key: 'male', value: 'male', text: 'Boy' },
  { key: 'female', value: 'female', text: 'Girl' },
];
let gestationWeeksOptions = [];
let gestWeeks = 23;
while (gestWeeks <= 42) {
  gestationWeeksOptions.push({
    key: gestWeeks.toString(10),
    value: gestWeeks,
    text: gestWeeks.toString(10),
  });
  gestWeeks++;
}

const gestationDaysOptions = [
  { key: '0', value: 0, text: '0' },
  { key: '1', value: 1, text: '1' },
  { key: '2', value: 2, text: '2' },
  { key: '3', value: 3, text: '3' },
  { key: '4', value: 4, text: '4' },
  { key: '5', value: 5, text: '5' },
  { key: '6', value: 6, text: '6' },
];

const references = [
  { key: 'uk-who', value: 'uk-who', text: 'UK-WHO' },
  { key: 'turner', value: 'turner', text: "Turner's syndrome" },
  { key: 'trisomy-21', value: 'trisomy-21', text: "Down's Syndrome" },
];

const ROBERT_WADLOW = 272; // interesting fact - Robert Wadlow (22/2/1918 – 15/7/1940) was the world's tallest man
const JON_BROWER_MINNOCH = 635; // interesting fact -  Jon Brower Minnoch (Born USA) was the world's heaviest man
const KHALID_BIN_MOHSEN_SHAARI = 204; // Khalid bin Mohsen Shaari (2/8/1991) from Saudi Arabia had the highest recorded BMI

let measurementOptions = [
  { key: 'height', value: 'height', text: 'Height (cm)', disabled: false },
  { key: 'weight', value: 'weight', text: 'Weight (kg)', disabled: false },
  { key: 'bmi', value: 'bmi', text: 'BMI (kg/m²)', disabled: false },
  {
    key: 'ofc',
    value: 'ofc',
    text: 'Head Circumference (cm)',
    disabled: false,
  },
];

const formatDate = (inputDate) => {
  let date;
  let month;
  let day;
  let year;
  try {
    date = new Date(inputDate);
    month = '' + (date.getMonth() + 1);
    day = '' + date.getDate();
    year = date.getFullYear();
    if (month.length < 2) {
      month = '0' + month;
    }
    if (day.length < 2) {
      day = '0' + day;
    }

    return [year, month, day].join('-');
  } catch (error) {
    throw new Error('Input date for formatDate not recognised');
  }
};

const isValidDate = (inputDate) => {
  try {
    const workingDate = new Date(inputDate);
    if (typeof workingDate.getTime() === 'number') {
      return true;
    }
  } catch (error) {
    return false;
  }
};

class MeasurementForm extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      birth_date: formatDate(new Date()),
      observation_date: formatDate(new Date()),
      measurement: {
        measurement_method: 'height',
        observation_value: 0,
        units: 'cm',
        show_add: true,
        show_remove: false,
        disabled: false,
      },
      sex: 'male',
      gestation_weeks: 40,
      gestation_days: 0,
      birth_date_error: '',
      observation_date_error: '',
      observation_value_error: '',
      form_valid: false,
      formData: {},
      measurementResult: [],
      reference: 'uk-who',
      measurementOptions: measurementOptions,
      networkError: '',
      modalOpen: false,
    };

    this.handleChangeDate = this.handleChangeDate.bind(this);
    this.handleChangeMeasurementMethod = this.handleChangeMeasurementMethod.bind(
      this
    );
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChangeGestation = this.handleChangeGestation.bind(this);
    this.handleChangeSex = this.handleChangeSex.bind(this);
    this.handleObservationChange = this.handleObservationChange.bind(this);
    this.handleChangeReference = this.handleChangeReference.bind(this);
  }

  handleGrowthResults = (results) => {
    this.props.measurementResult(results);
  };

  handleChangeReference = (ref, data) => {
    this.setState({ reference: data.value });

    if (data.value === 'turner') {
      this.disableMeasurement('weight', true);
      this.disableMeasurement('ofc', true);
      this.disableMeasurement('bmi', true);
      this.setState({ sex: 'female' });
      this.setState({ measurementMethod: 'height' });
      this.props.handleChangeReference(data.value); //call back
      return;
    }
    if (data.value === 'uk-who') {
      this.disableMeasurement('weight', false);
      this.disableMeasurement('ofc', false);
      this.disableMeasurement('bmi', false);
      this.props.handleChangeReference(data.value); //call back
      return;
    }
    if (data.value === 'trisomy-21') {
      this.disableMeasurement('weight', false);
      this.disableMeasurement('ofc', false);
      this.disableMeasurement('bmi', false);
      this.props.handleChangeReference(data.value); //call back
      return;
    }
  };

  disableMeasurement = (measurement_method, disable) => {
    if (measurement_method === 'height') {
      let options = this.state.measurementOptions;
      options[0].disabled = disable;
      this.setState({ measurementOptions: options });
    }
    if (measurement_method === 'weight') {
      let options = this.state.measurementOptions;
      options[1].disabled = disable;
      this.setState({ measurementOptions: options });
    }
    if (measurement_method === 'ofc') {
      let options = this.state.measurementOptions;
      options[2].disabled = disable;
      this.setState({ measurementOptions: options });
    }
    if (measurement_method === 'bmi') {
      let options = this.state.measurementOptions;
      options[3].disabled = disable;
      this.setState({ measurementOptions: options });
    }
  };

  handleChangeDate(event) {
    this.setState({ [event.target.name]: event.target.value });
    if (isValidDate(event.target.value)) {
      const observation_date_object =
        event.target.name === 'birth_date'
          ? new Date(this.state.observation_date)
          : new Date(event.target.value);
      const birth_date_object =
        event.target.name === 'birth_date'
          ? new Date(event.target.value)
          : new Date(this.state.birth_date);
      const timeInterval =
        observation_date_object.getTime() - birth_date_object.getTime();
      if (timeInterval < 0) {
        if (event.target.name === 'birth_date') {
          this.setState({
            birth_date_error:
              'Date of birth cannot come after the date of measurement',
          });
        } else if (event.target.name === 'observation_date') {
          this.setState({
            observation_date_error:
              'Date of measurement cannot come before the date of birth.',
          });
        }
        this.setState({ form_valid: false });
      } else if (timeInterval > 631139040000) {
        if (event.target.name === 'birth_date') {
          this.setState({
            birth_date_error: 'No centile data exists over 20 years of age.',
          });
        } else if (event.target.name === 'observation_date') {
          this.setState({
            observation_date_error:
              'No centile data exists over 20 years of age.',
          });
        }
        this.setState({ form_valid: false });
      } else {
        this.setState({ birth_date_error: '' });
        this.setState({ observation_date_error: '' });
        if (
          this.state.observation_value_error === '' &&
          this.state.measurement.observation_value
        ) {
          this.setState({ form_valid: true });
        } else {
          this.setState({ form_valid: false });
        }
      }
    } else {
      this.setState({ form_valid: false });
    }
  }

  handleObservationChange = (observation, data) => {
    // this is updating an observation value

    const observation_value = data.value;
    let { measurement, observation_value_error } = this.state;
    measurement.observation_value = observation_value;
    observation_value_error = this.validateObservationValue(
      this.state.measurement.measurement_method,
      observation_value
    );
    this.setState({
      measurement: measurement,
      observation_value_error: observation_value_error,
    });
    if (
      this.state.birth_date_error === '' &&
      this.state.observation_date_error === '' &&
      observation_value_error === ''
    ) {
      this.setState({ form_valid: true });
    } else {
      this.setState({ form_valid: false });
    }
  };

  validateObservationValue(measurement_method, observation_value) {
    if (measurement_method === 'height') {
      if (observation_value < 35) {
        return 'The ' + measurement_method + ' you entered is too low.';
      } else if (observation_value > ROBERT_WADLOW) {
        return 'The ' + measurement_method + ' you entered is too tall.';
      } else {
        return '';
      }
    }
    if (measurement_method === 'weight') {
      if (observation_value < 0.01) {
        return 'The ' + measurement_method + ' you entered is too low.';
      } else if (observation_value > JON_BROWER_MINNOCH) {
        return 'The ' + measurement_method + ' you entered is too heavy.';
      } else {
        return '';
      }
    }
    if (measurement_method === 'bmi') {
      if (observation_value < 5) {
        return 'The ' + measurement_method + ' you entered is too low.';
      } else if (observation_value > KHALID_BIN_MOHSEN_SHAARI) {
        return 'The ' + measurement_method + ' you entered is too high.';
      } else {
        return '';
      }
    }
    if (measurement_method === 'ofc') {
      if (observation_value < 30) {
        return 'The ' + measurement_method + ' you entered is too low.';
      } else if (observation_value > 70) {
        return 'The ' + measurement_method + ' you entered is too high.';
      } else {
        return '';
      }
    }
  }

  formIsValid() {
    let valid = true;
    if (this.state.observation_value_error !== '') {
      valid = false;
    }
    if (
      this.state.birth_date_error === '' &&
      this.state.observation_date_error === '' &&
      valid
    ) {
      return true;
    } else {
      return false;
    }
  }

  handleSubmit(event) {
    // passes the form data back to the parent (measurement segment)
    let measurementArray = [];

    let formData = {
      birth_date: this.state.birth_date,
      observation_date: this.state.observation_date,
      measurement_method: this.state.measurement.measurement_method,
      observation_value: this.state.measurement.observation_value,
      gestation_weeks: this.state.gestation_weeks,
      gestation_days: this.state.gestation_days,
      sex: this.state.sex,
    };
    measurementArray.push(formData);

    this.handleGrowthResults(measurementArray);
  }

  handleChangeMeasurementMethod(event, data) {
    let measurement = this.state.measurement;

    this.props.handleChangeMeasurementMethod(data.value);
    if (data.value !== measurement.measurement_method) {
      measurement.measurement_method = data.value;
      measurement.units = this.changeUnits(data.value);
      if (
        this.state.reference === 'turner' &&
        measurement.measurement_method !== 'height'
      ) {
        this.disableMeasurement('weight', true);
        this.disableMeasurement('bmi', true);
        this.disableMeasurement('ofc', true);
      } else {
        this.disableMeasurement('weight', false);
        this.disableMeasurement('bmi', false);
        this.disableMeasurement('ofc', false);
      }
    }
    this.setState({ measurement: measurement });
    this.setState({ form_valid: this.formIsValid() });
  }

  handleChangeGestation(event, data) {
    const { name, value } = data;
    if (name === 'gestation_weeks') {
      this.setState({ gestation_weeks: value });
      if (value === 42) {
        this.setState({ gestation_days: 0 });
      }
    } else if (name === 'gestation_days') {
      if (this.state.gestation_weeks === 42) {
        this.setState({ gestation_days: 0 });
      } else {
        this.setState({ gestation_days: value });
      }
    }
  }

  handleChangeSex(event, data) {
    this.setState({ sex: data.value });
    this.props.handleChangeSex(data.value);
  }

  changeUnits(measurement_method) {
    if (measurement_method === 'height') {
      return 'cm';
    }
    if (measurement_method === 'weight') {
      return 'kg';
    }
    if (measurement_method === 'bmi') {
      return 'kg/m²';
    }
    if (measurement_method === 'ofc') {
      return 'cm';
    }
  }

  render() {
    return (
      <Container>
        <Segment textAlign={'center'}>
          <Form onSubmit={this.handleSubmit}>
            <Form.Field>
              <Header as="h5" textAlign="left">
                Reference
              </Header>
              <Select
                name="reference"
                value={this.state.reference}
                options={references}
                onChange={this.handleChangeReference}
                placeholder="Select reference"
              />
            </Form.Field>
            <Form.Field required>
              <Header as="h5" textAlign="left">
                Dates
              </Header>
              <Input
                label="Birth Date"
                type="date"
                name="birth_date"
                value={this.state.birth_date}
                placeholder="Date of Birth"
                onChange={this.handleChangeDate}
              />
            </Form.Field>
            <Form.Field required>
              <Input
                label="Measurement Date"
                type="date"
                name="observation_date"
                value={this.state.observation_date}
                placeholder="Date of Measurement"
                onChange={this.handleChangeDate}
              />
            </Form.Field>
            {/* <Segment> */}
            <Header as="h5" textAlign="left">
              Measurements
            </Header>

            <Form.Group>
              <Form.Field required>
                <Select
                  value={this.state.measurement.measurement_method}
                  name="measurement_method"
                  placeholder="Measurement Type"
                  options={measurementOptions}
                  onChange={this.handleChangeMeasurementMethod}
                />
              </Form.Field>
              <Form.Field required width={8}>
                <Input
                  type="decimal"
                  name="observation_value"
                  placeholder="Measurement"
                  value={this.state.measurement.observationValue}
                  label={{
                    content: this.state.measurement.units.toString(),
                    basic: true,
                    color: 'blue',
                  }}
                  labelPosition="right"
                  onChange={this.handleObservationChange}
                />
              </Form.Field>
            </Form.Group>
            {this.state.observation_value_error !== '' ? (
              <Message color="red">
                {this.state.observation_value_error}
              </Message>
            ) : null}
            {this.state.observation_date_error !== '' ? (
              <Message color="red">{this.state.observation_date_error}</Message>
            ) : null}
            {this.state.birth_date_error !== '' ? (
              <Message color="red">{this.state.birth_date_error}</Message>
            ) : null}
            {/* </Segment> */}
            <Header as="h5" textAlign="left">
              Sex
            </Header>
            <Form.Field required>
              <Select
                name="sex"
                placeholder="Sex"
                value={this.state.sex}
                onChange={this.handleChangeSex}
                options={sexOptions}
              />
            </Form.Field>

            <Form.Group>
              <Form.Field>
                <Header as="h5" textAlign="left">
                  Gestation
                </Header>
                <span>
                  <Select
                    compact
                    name="gestation_weeks"
                    value={this.state.gestation_weeks}
                    options={gestationWeeksOptions}
                    onChange={this.handleChangeGestation}
                  />
                  &nbsp;+
                  <Select
                    compact
                    name="gestation_days"
                    value={this.state.gestation_days}
                    options={gestationDaysOptions}
                    onChange={this.handleChangeGestation}
                  />
                  &nbsp; weeks
                </span>
              </Form.Field>
              {/* </Segment> */}
            </Form.Group>

            <Form.Field>
              <Button
                content="Calculate Centiles and Create Chart"
                type="submit"
                fluid={true}
                disabled={!this.state.form_valid}
                color="pink"
                icon="line graph"
                labelPosition="right"
              />
            </Form.Field>
          </Form>
        </Segment>
        <ErrorModal
          error={this.state.networkError}
          open={this.state.modalOpen}
          handleClose={() => {
            this.setState({ modalOpen: false });
          }}
        />
      </Container>
    );
  }
}

const ErrorModal = (props) => {
  return (
    <Modal
      error={props.error}
      open={props.open}
      size="small"
      closeOnEscape={true}
    >
      <Modal.Header>{props.error}</Modal.Header>
      <Modal.Content>
        It is likely the server is down. Please check back later
      </Modal.Content>
      <Modal.Actions>
        <Button negative onClick={props.handleClose}>
          Cancel
        </Button>
      </Modal.Actions>
    </Modal>
  );
};

export default MeasurementForm;
