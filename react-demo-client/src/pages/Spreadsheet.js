import React, { Component } from "react";
import { Container, Header, Button, Icon, Segment, Grid, Label, Modal } from "semantic-ui-react";
import axios from 'axios';
import { withRouter } from "react-router-dom";
import Dropzone from 'react-dropzone';
// import XLSX from 'xlsx'; DEPRECATED - SEND THE FILE DIRECT TO THE SERVER - DATA PARSED SERVER-SIDE


class Spreadsheet extends Component{

    constructor(props){
        super(props);
        this.state = {
            uploadDisabled: true,
            csvFile: null,
            open: false,
            error: null
        }
        this.uploadData = this.uploadData.bind(this);
        this.removeFile = this.removeFile.bind(this);
    }

    async uploadData(){
        let fileData = new FormData()
        fileData.append("csv_file", this.state.csvFile, 'upload.csv')
        await axios({
          url: `${process.env.REACT_APP_GROWTH_API_BASEURL}/uk-who/spreadsheet`,
          data: fileData,
          method: "POST",
          headers: {
            "Content-Type": "text/csv",
          },
        }).then((response) => {

            console.log(response);
          /*
            The response object from the server is:
                {
                    data: [an array of Measurement class objects]
                    unique: boolean - refers to whether data is from one child or many children
                    valid: boolean - refers to whether imported data was valid for calculation
                    error: string  - error message if invalid file
                }
            */
                if (response) {
                    if (response.data["valid"]) {
                        this.props.history.push({
                          pathname: "/serial_results",
                          data: response.data,
                        });
                      } else {
                        // TODO #7 implement popup in the event of failed validation of uploaded data as well as catch statement
                        this.setState({error: response.data["error"], open: true})
                    }
                } else {
                    this.setState({error: 'No response from server', open: true})
                }
          
        }).catch(error => {
            if (error.response.status === 500){
                this.setState({error: '500 Response from server', open: true})
            }
        });
    }

    removeFile(event){
        event.preventDefault();
        this.setState({csvFile: null});
        this.setState({uploadDisabled: true});
    }

    render(){
        const { open } = this.state
        return (
            <Container>
                <Grid centered>
                    <Modal
                        size='mini'
                        open={open}
                    >
                        <Modal.Header>Error</Modal.Header>
                        <Modal.Content>
                        <p>{this.state.error}</p>
                        </Modal.Content>
                        <Modal.Actions>
                        <Button negative onClick={()=> this.setState({open: false, error: null})}>
                            Cancel
                        </Button>
                        </Modal.Actions>
                    </Modal>
                    <Grid.Column width={12}>
                        <Grid.Row style={{textAlign:"center"  }}>
                            <h1>Upload .CSV Spreadsheet</h1>
                        </Grid.Row>
                        <Grid.Row centered>
                            <Dropzone 
                                onDrop={acceptedFiles => {
                                        this.setState({uploadDisabled: false});
                                        this.setState({csvFile: acceptedFiles[0]})
                                    }
                                }
                                accept='text/csv'
                                minSize={0}
                                maxSize={5242880}
                            >
                                    {({getRootProps, getInputProps, isDragActive, isDragReject, acceptedFiles}) => (
                                        <section>
                                        <div {...getRootProps()}>
                                            <input {...getInputProps()} />
                                            <Segment placeholder color='green'>
                                                <Header icon>
                                                    {this.state.csvFile === null ? <Icon name='file outline' color='green'/> : <Icon name='file' color='green'/>}
                                                </Header>
                                                <h5 style={{textAlign:"center"  }}>
                                                    {!isDragActive && this.state.csvFile === null && "Drag 'n' drop .csv only here, or click to select files"}
                                                    {isDragActive && this.state.csvFile === null && !isDragReject  && "Drop .csv only here "}
                                                    {isDragReject && this.state.csvFile === null && "Only .csv files accepted" }
                                                    {this.state.csvFile !== null && <Label><Icon name="file" color='green'></Icon>{acceptedFiles[0].name}</Label>}
                                                </h5>
                                            </Segment>
                                        </div>
                                        </section>
                                    )}
                            </Dropzone>
                        </Grid.Row>
                        <Grid.Row style={{textAlign:"center", padding: 10 }}>
                            { !this.state.uploadDisabled &&
                                <Button.Group>
                                    <Button color='green' onClick={this.uploadData}>Import Data</Button>
                                    <Button.Or></Button.Or>
                                    <Button color="red" onClick={this.removeFile}>Remove</Button>
                                </Button.Group>
                            }
                        </Grid.Row>
                    </Grid.Column>
                </Grid>
            </Container>
        );
    }
}

export default withRouter(Spreadsheet);