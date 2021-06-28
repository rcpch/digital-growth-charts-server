import React, { Component } from "react";
import { Card, Icon } from "semantic-ui-react";

export class OpenSourceCard extends Component {
  render() {
    return (
      <Card>
        <Card.Content>
          <Card.Header as="h1">
            <Icon name="github" size="huge" />
          </Card.Header>
          <Card.Header>Open Source</Card.Header>
          <Card.Description>
            For transparency, accuracy, and maximum reuse, our Growth Charts API
            and associated libraries are 100% open source. We welcome code
            reviews, feedback, issues and pull requests.
            <a href="https://github.com/rcpch">Check us out on GitHub</a> -
            we're the first Royal College to have clinical code in it's own
            GitHub organisation!
          </Card.Description>
        </Card.Content>
      </Card>
    );
  }
}

export default OpenSourceCard;
