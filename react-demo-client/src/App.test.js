import React from "react";
import { render } from "@testing-library/react";
import App from "./App";

test("renders RCPCH Growth Charts text", () => {
  const { getByText } = render(<App />);
  const textElement = getByText(/Digital Growth Charts Demo/i);
  expect(textElement).toBeInTheDocument();
});
