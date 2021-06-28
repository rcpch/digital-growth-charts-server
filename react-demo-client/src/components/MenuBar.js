import React from "react";
import { Menu } from "semantic-ui-react";

function MenuBar(props) {
  return (
    <Menu borderless inverted color="blue" as="h2" className="rcpch-menu">
      <Menu.Item
        href="https://growth-blog.rcpch.ac.uk/"
        name="Growth Blog"
        position="right"
      />
      <Menu.Item
        href="https://dev.rcpch.ac.uk/"
        name="API Documentation"
        position="right"
      />
      <Menu.Item
        href="https://github.com/rcpch/growth-references"
        name="Growth References"
        position="right"
      />
      <Menu.Item
        name="Technical"
        onClick={props.toggleTechnical}
        position="right"
      />
    </Menu>
  );
}

export default MenuBar;
