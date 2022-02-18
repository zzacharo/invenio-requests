import { i18next } from "@translations/invenio_requests/i18next";

import React from "react";
import { Button } from "semantic-ui-react";

export const SaveButton = (props) => (
  <Button icon="save" positive size="mini" content={i18next.t("Save")} {...props} />
);

export const CancelButton = (props) => (
  <Button icon="cancel" content={i18next.t("Save")} size="mini" {...props} />
);
