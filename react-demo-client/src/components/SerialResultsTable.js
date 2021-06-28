import React, { Component } from "react";
import { Container, Table, Header } from "semantic-ui-react";
import { withRouter } from "react-router-dom";

class SerialResultsTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: this.props.results
        }
    }

    render() {
        return (
            <Container>
                <Header as='h1'>
                        Uploaded Data Table
                </Header>
                <Table basic='very' celled collapsing>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell>
                                Birth Date
                            </Table.HeaderCell>
                            <Table.HeaderCell>
                                Gestation
                            </Table.HeaderCell>
                            <Table.HeaderCell>
                                Estimated Delivery Date
                            </Table.HeaderCell>
                            <Table.HeaderCell>
                                Measurement Date
                            </Table.HeaderCell>
                            <Table.HeaderCell>
                                Age
                            </Table.HeaderCell>
                            <Table.HeaderCell>
                                Measurement
                            </Table.HeaderCell>
                            <Table.HeaderCell>
                                Value
                            </Table.HeaderCell>
                            <Table.HeaderCell>
                                SDS
                            </Table.HeaderCell>
                            <Table.HeaderCell>
                                Centile
                            </Table.HeaderCell>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {this.state.data.map((item, index)=>{
                            return (
                                <DataRow data={item} key={index}/>
                            );
                        })}
                    </Table.Body>
                </Table>
            </Container>
        )
    }
}

export default withRouter(SerialResultsTable);


    
function DataRow(props) {

    const birth_data = props.data.birth_data;
    const measurement_calculated_values = props.data.measurement_calculated_values;
    const measurement_dates= props.data.measurement_dates;
    const child_observation_value = props.data.child_observation_value;

    const birth_date = new Date(birth_data.birth_date).toLocaleDateString('en-UK');
    const measurement_date = new Date(measurement_dates.observation_date).toLocaleDateString('en-UK');
    const edd = (birth_data.estimated_date_delivery !== null) ? new Date(birth_data.estimated_date_delivery).toLocaleDateString('en-UK') : "";

    return (
        <Table.Row>
            <Table.Cell>
                {birth_date}
            </Table.Cell>
            <Table.Cell>
                {birth_data.gestation_weeks}<sup>+{birth_data.gestation_days}</sup>
            </Table.Cell>
            <Table.Cell>
                {edd}
            </Table.Cell>
            <Table.Cell>
                {measurement_date}
            </Table.Cell>
            <Table.Cell>
                {measurement_dates.corrected_decimal_age}
            </Table.Cell>
            <Table.Cell>
                {child_observation_value.measurement_method}
            </Table.Cell>
            <Table.Cell>
                {child_observation_value.measurement_value}
            </Table.Cell>
            <Table.Cell>
                {measurement_calculated_values.sds}
            </Table.Cell>
            <Table.Cell>
                {measurement_calculated_values.centile}
            </Table.Cell>
        </Table.Row>
    );
}