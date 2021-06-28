import React, { Component } from "react";
import {
  Icon,
  Image,
  Segment,
  List,
  Grid,
  Header,
  Divider,
  Container,
} from "semantic-ui-react";

export default class Footer extends Component {
  render() {
    return (
      <Segment
        basic
        inverted
        style={{ margin: "5em 0em 0em", padding: "5em 0em" }}
        vertical
      >
        <Container textAlign="center" className="footer">
          <Grid columns={4} divided stackable inverted>
            <Grid.Row>
              <Grid.Column>
                <Header inverted as="h4" content="Source Code" />
                <Icon name="github" size="big" />
                <List link inverted>
                  <List.Item
                    as="a"
                    href="https://github.com/rcpch/digital-growth-charts-react-client"
                  >
                    React Demo Client
                  </List.Item>
                  <List.Item
                    as="a"
                    href="https://github.com/rcpch/digital-growth-charts-react-chart-library"
                  >
                    React Chart Component Library
                  </List.Item>
                  <List.Item
                    as="a"
                    href="https://github.com/rcpch/digital-growth-charts-server"
                  >
                    Digital Growth Charts API Server
                  </List.Item>
                  <List.Item
                    as="a"
                    href="https://github.com/rcpch/growth-references"
                  >
                    Growth References Repository
                  </List.Item>
                </List>
              </Grid.Column>
              <Grid.Column>
                <Header inverted as="h4" content="Support" />
                <List celled inverted>
                  <List.Item
                    as="a"
                    href="https://join.slack.com/t/dpchrworkspace/shared_invite/zt-iz9ifaww-PWZ_3rfnsDaQxsvK9Wf51A"
                  >
                    <List.Icon name="slack" size="big" />
                  </List.Item>
                  <List.Content>
                    <List.Header>Slack</List.Header>
                    Join the DPCHR Slack Workspace
                  </List.Content>
                  <List.Item as="a">Link Two</List.Item>
                  <List.Item as="a">Link Three</List.Item>
                  <List.Item as="a">Link Four</List.Item>
                </List>
              </Grid.Column>
              <Grid.Column>
                <Header inverted as="h4" content="Group 3" />
                <List link inverted>
                  <List.Item as="a">Link One</List.Item>
                  <List.Item as="a">Link Two</List.Item>
                  <List.Item as="a">Link Three</List.Item>
                  <List.Item as="a">Link Four</List.Item>
                </List>
              </Grid.Column>
              <Grid.Column>
                <Header inverted as="h4" content="Group 4" />
                <List link inverted>
                  <List.Item as="a">Link One</List.Item>
                  <List.Item as="a">Link Two</List.Item>
                  <List.Item as="a">Link Three</List.Item>
                  <List.Item as="a">Link Four</List.Item>
                </List>
              </Grid.Column>
            </Grid.Row>
          </Grid>
          <Divider inverted section />

          <List horizontal inverted divided link size="small">
            <List.Item as="a" href="https://www.rcpch.ac.uk/">
              <Image
                circular
                src="dynamic-child-favicon.png"
                centered
                size="mini"
              />
            </List.Item>
            <List.Item as="a" href="https://www.rcpch.ac.uk/">
              © 2020-21 Copyright RCPCH
            </List.Item>
            <List.Item as="a" href="#">
              dGC Privacy Policy
            </List.Item>
          </List>
        </Container>
      </Segment>
    );
  }
}
