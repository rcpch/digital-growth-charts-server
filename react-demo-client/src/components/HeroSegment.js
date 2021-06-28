import React, { Component } from "react";

import { Segment, Header } from "semantic-ui-react";

export class HeroSegment extends Component {
  render() {
    return (
      <Segment
        className="hero-segment"
        basic={true}
        inverted={true}
        color="blue"
        style={{
          backgroundImage: `url(${"dynamic-child-banner-wallpaper.png"})`,
          backgroundSize: "cover",
        }}
      >
        <Header inverted as="h1" style={{ fontSize: "3em" }}>
          <p>Royal College of Paediatrics and Child Health</p>
          <p>Digital Growth Charts</p>
        </Header>
        <Header inverted as="h3">
          A first-of-its-kind 'Best Practice As Code' innovation by the RCPCH.
          Digital clinical tools provided to developers of clinician and patient
          facing technology.
          <a href="https://marcus-baw.medium.com/royal-colleges-3-0-best-practice-as-code-7065bce821a7" className="royalcolleges">
            #royalcolleges3.0
          </a>
        </Header>
        <Header inverted as="h2">
          Free basic access to all, fully open source, and sustainably managed
          as a non-profit enterprise.
        </Header>
      </Segment>
    );
  }
}

export default HeroSegment;
