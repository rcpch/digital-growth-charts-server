import React, { Component } from "react";
import { Card, Segment } from "semantic-ui-react";
import { OpenSourceCard } from "./cards/OpenSourceCard";
import AwardWinningCard from "./cards/AwardWinningCard";
import GetStartedCard from "./cards/GetStartedCard";
import GoldStandardCard from "./cards/GoldStandardCard";

export class CardsSegment extends Component {
  render() {
    return (
      <Segment basic>
        <Card.Group stackable centered>
          <GoldStandardCard />
          <AwardWinningCard />
          <GetStartedCard />
          <OpenSourceCard />
        </Card.Group>
      </Segment>
    );
  }
}

export default CardsSegment;
