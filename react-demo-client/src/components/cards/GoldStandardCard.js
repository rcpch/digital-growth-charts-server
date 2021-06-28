import React, { Component } from "react";
import { Card, Image } from "semantic-ui-react";

export class GoldStandardCard extends Component {
  render() {
    return (
      <Card>
        <Card.Content>
          <Card.Header as="h1">
            <Image src="rcpch_logo.png" size="tiny" />
          </Card.Header>
          <Card.Header>Gold Standard</Card.Header>
          <Card.Description>
            Working with experts in growth monitoring, growth charts, centile
            and SDS calculation, we've created an API that handles the heavy
            lifting of child growth parameters. You get reliable, safe results
            instantly.
          </Card.Description>
        </Card.Content>
      </Card>
    );
  }
}

export default GoldStandardCard;
