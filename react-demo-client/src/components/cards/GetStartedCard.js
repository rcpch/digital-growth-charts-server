import React, { Component } from "react";
import { Button, Card, Icon, Image } from "semantic-ui-react";

export class GetStartedCard extends Component {
  render() {
    return (
      <Card>
        <Card.Content>
          <Card.Header as="h1">
            <Image src="hammer.png" size="tiny" />
          </Card.Header>
          <Card.Header>Get Started</Card.Header>
          <Card.Description>
            Looking to integrate digital growth charts in your app? You need the
            Developer portal and API documentation
          </Card.Description>
        </Card.Content>
        <Card.Content extra>
          <Button basic as="a" href="https://dev.rcpch.ac.uk/">
            <Icon name="external" />
            Dev Portal & API Docs
          </Button>
        </Card.Content>
      </Card>
    );
  }
}

export default GetStartedCard;
