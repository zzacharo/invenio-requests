import React from "react";
import { Button } from "semantic-ui-react";

export const SaveButton = (props) => (
  <Button icon="save" positive size="mini" content="Save" {...props} />
);

export const CancelButton = (props) => (
  <Button icon="cancel" content="Cancel" size="mini" {...props} />
);
