import React, { Component } from "react";
import { Card, Image } from "semantic-ui-react";

export class AwardWinningCard extends Component {
  render() {
    return (
      <Card>
        <Card.Content>
          <Card.Header as="h1">
            <Image src="htn-awards-winner-2020-logo.jpg" size="tiny" />
          </Card.Header>
          <Card.Header>Award Winning</Card.Header>
          <Card.Description>
            Winner of
            <a href="https://www.thehtn.co.uk/health-tech-awards-2020-live/">
              'Best Health Tech Solution' in the Health Tech Awards 2020
            </a>
          </Card.Description>
        </Card.Content>
      </Card>
    );
  }
}

export default AwardWinningCard;
