import React from "react";
import { Sidebar, Menu, Icon, Header, Container } from "semantic-ui-react";

function Technical(props) {
  return (
    <div>
      <Sidebar
        as={Menu}
        animation="push"
        direction="right"
        icon="labeled"
        inverted
        vertical
        visible={props.technicalSidebarVisible}
        width="wide"
      >
        <Container textAlign="left">
          <Icon
            inverted
            name="close"
            size="big"
            onClick={props.toggleTechnical}
          />
        </Container>
        <Header inverted>Technical</Header>
        <Menu.Item as="a">
          <Icon inverted name="server" />
          Configured API Server URL:
          {process.env.REACT_APP_GROWTH_API_BASEURL}
        </Menu.Item>
      </Sidebar>
    </div>
  );
}

export default Technical;
