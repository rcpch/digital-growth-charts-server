import React, { Component } from "react";
import { Container, Menu } from "semantic-ui-react";
import { withRouter } from "react-router-dom";
import SerialResultsTable from '../components/SerialResultsTable';

class Results extends Component {
    constructor(props){
        super(props);
        let data = this.props.location.data.data;
        this.state = {
            childData: data,
            activeItem: 'tables',
            chartData: null,
            unique_child: this.props.location.data.unique_child,
        }
        this.handleItemClick.bind(this);
        /*
          the object passed in here has the structure:
                {
                    data: [an array of Measurement class objects]
                    unique: boolean - refers to whether data is from one child or many children
                    valid: boolean - refers to whether imported data was valid for calculation
                    error: string  - error message if invalid file
                }
        */
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
                    disabled={!this.state.unique_child}
                />
            </Menu>
            <Container>
                {activeItem === 'tables'? <SerialResultsTable results={this.state.childData}/> : <h5>ChartData would have gone here</h5>}
            </Container>
            </div>
        );
    }
}

export default withRouter(Results);