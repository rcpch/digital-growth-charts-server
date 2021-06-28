import React, { Component } from "react";
import { Container, Table, Grid, Popup, Icon, Header, Menu } from "semantic-ui-react";
import { withRouter } from "react-router-dom";

class Results extends Component {
    constructor(props){
        super(props);
        let data = this.props.location.data.calculations;
        this.state = {
            results: data,
            activeItem: 'tables',
            chartData: null
        }
        this.handleItemClick.bind(this);
    }

    handleItemClick = (e, { name }) => this.setState({ activeItem: name });

    render() {
        const { activeItem } = this.state;
        return (
            <div>
            <Menu tabular>
                <Menu.Item
                    name='tables'
                    active={activeItem === 'tables'}
                    onClick={this.handleItemClick}
                />
                <Menu.Item
                    name='charts'
                    active={activeItem === 'charts'}
                    onClick={this.handleItemClick}
                />
            </Menu>
            <Container>
                {activeItem === 'tables'? <Tables results={this.state.results}/> : <h5>chartdata would have gone here</h5>}
            </Container>
            </div>
        );
    }
}

export default withRouter(Results);

function Tables(props){
    return (
        <Container>
            <Grid columns={2} padded>
                <Grid.Column>
                    <DatesTable dates={props.results}/>
                </Grid.Column>
                <Grid.Column>
                    <CentilesTable centiles={props.results}/>
                </Grid.Column>
            </Grid>
        </Container>
    );
}


function DatesTable(props) {
    return (
        <>
            {props.dates.map((item, index)=>{
                if(index > 0 && item.measurement_dates.observation_date === props.dates[0].measurement_dates.observation_date){
                    return null;
                } else {
                    return (
                        <Table basic='very' celled collapsing key={index}>
                            <Table.Header>
                                <Table.Row>
                                    <Table.HeaderCell>
                                    </Table.HeaderCell>
                                    <Table.HeaderCell>
                                        Dates/Ages
                                    </Table.HeaderCell>
                                    <Table.HeaderCell>
                                    </Table.HeaderCell>
                                </Table.Row>
                            </Table.Header>
                            <Table.Body>
                                <Table.Row>
                                    <Table.Cell>Date of Birth</Table.Cell>
                                    <Table.Cell>{item.birth_data.birth_date}</Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Date of Measurement</Table.Cell>
                                    <Table.Cell>{item.measurement_dates.observation_date}</Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Due Date</Table.Cell>
                                    <Table.Cell>{item.birth_data.estimated_date_delivery}</Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Gestation</Table.Cell>
                                    <Table.Cell>{item.birth_data.gestation_weeks}+{item.birth_data.gestation_days} weeks</Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Chronological Age</Table.Cell>
                                    <Table.Cell>{item.measurement_dates.chronological_decimal_age} y</Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Chronological Calendar Age</Table.Cell>
                                    <Table.Cell>{item.measurement_dates.chronological_calendar_age}</Table.Cell>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Corrected Age</Table.Cell>
                                    <Table.Cell>{item.measurement_dates.corrected_decimal_age} y</Table.Cell>
                                    <PopupData lay_comment={item.measurement_dates.lay_decimal_age_comment} clinician_comment={item.measurement_dates.clinician_decimal_age_comment}></PopupData>
                                </Table.Row>
                                <Table.Row>
                                    <Table.Cell>Chronological Calendar Age</Table.Cell>
                                    <Table.Cell>{item.measurement_dates.corrected_calendar_age}</Table.Cell>
                                </Table.Row>
                            </Table.Body>
                        </Table>
                    );
                }
            })};
        </>
    );
}

function CentilesTable(props) {
    return (
        <Table basic='very' celled collapsing>
            <Table.Header>
                <Table.Row>
                    <Table.HeaderCell>
                    </Table.HeaderCell>
                    <Table.HeaderCell>
                        Centiles
                    </Table.HeaderCell>
                    <Table.HeaderCell>
                    </Table.HeaderCell>
                </Table.Row>
            </Table.Header>
            {props.centiles.map((item, index)=>{
                return (
                    <Table.Body key={index}>
                        <MeasurementCell item={item}/>
                        <Table.Row>
                            <Table.Cell>SDS</Table.Cell>
                            <Table.Cell> {item.measurement_calculated_values.sds}</Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Centile</Table.Cell>
                            <Table.Cell> {item.measurement_calculated_values.centile} %</Table.Cell>
                            {/* <PopupData lay_comment={item.measurement_calculated_values.lay_comment} clinician_comment={item.measurement_calculated_values.clinician_comment}></PopupData> */}
                        </Table.Row>
                    </Table.Body>
                );
            })}
        </Table>
    );
}

function MeasurementCell(props) {
    
    if (props.item.child_observation_value.measurement_method === 'height') {
        return (
                <Table.Row>
                    <Table.Cell>Height</Table.Cell>
                    <Table.Cell> {props.item.child_observation_value.measurement_value} cm</Table.Cell>
                </Table.Row>
        );
    }
    else if (props.item.child_observation_value.measurement_method === 'weight') {
        return (
            <Table.Row>
                <Table.Cell>Weight</Table.Cell>
                <Table.Cell> {props.item.child_observation_value.measurement_value} kg</Table.Cell>
            </Table.Row>
        );
    }
    else if (props.item.child_observation_value.measurement_method === 'bmi') {
        return (
            <Table.Row>
                <Table.Cell>BMI</Table.Cell>
                <Table.Cell> {props.item.child_observation_value.measurement_value} kg/m²</Table.Cell>
            </Table.Row>
        );
    }
    else if (props.item.child_observation_value.measurement_method === 'ofc') {
        return (
            <Table.Row>
                <Table.Cell>Head Circumference</Table.Cell>
                <Table.Cell> {props.item.child_observation_value.measurement_value} cm</Table.Cell>
            </Table.Row>
        );
    }
    
}

function PopupData(props) {
    return (
        <React.Fragment>
            <Table.Cell>
                <Popup
                    trigger={<Icon name="info circle" color='blue'></Icon>}
                    position='top right'
                    flowing
                    hoverable
                >
                    <Grid centered divided columns={2}>
                        <Grid.Column textAlign='center'>
                            <Header as='h4'>Lay Comment</Header>
                            <p>
                                {props.lay_comment}
                            </p>
                        </Grid.Column>
                        <Grid.Column textAlign='center'>
                            <Header as='h4'>Clinician Comment</Header>
                            <p>
                                {props.clinician_comment}
                            </p>
                        </Grid.Column>
                    </Grid>
                </Popup>
            </Table.Cell>
        </React.Fragment>
    );
}

