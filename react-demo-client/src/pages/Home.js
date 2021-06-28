import React from "react";
import { withRouter } from "react-router-dom";
import HeroSegment from "../components/HeroSegment";
import CardsSegment from "../components/CardsSegment";
import MeasurementSegment from "../components/MeasurementSegment";

function Home() {
  return (
    <div>
      <HeroSegment />
      <MeasurementSegment />
      <CardsSegment />
    </div>
  );
}

export default withRouter(Home);
