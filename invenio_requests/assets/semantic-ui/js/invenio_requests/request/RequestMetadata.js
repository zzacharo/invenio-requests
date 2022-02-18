import React, { Component } from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";
import { Divider, Header, Image, Label, Icon } from "semantic-ui-react";
import { i18next } from "@translations/invenio_requests/i18next";


class RequestMetadata extends Component {
  render() {
    const { request } = this.props;
    return (
      <Overridable id="InvenioRequest.RequestMetadata.Layout" {...this.props}>
        <>
          <Header as="h4">{i18next.t("Requestor")}</Header>
          <Image src="/static/images/square-placeholder.png" avatar rounded />
          <span>{request.created_by.full_name}</span>
          <Divider />
          <Header as="h4">{i18next.t("Request type")}</Header>
          <Label>{request.type}</Label>
          <Divider />
          <Header as="h4">{i18next.t("Status")}</Header>
          {/* TODO state ICONS ?*/}
          <Icon name="clock outline" />
          {request.status}
          {request.expires_at && (
            <>
              <Divider />
              <Header as="h4">{i18next.t("Expires")}</Header>
              {request.state}
            </>
          )}
          <Divider hidden/>
        </>
      </Overridable>
    );
  }
}

RequestMetadata.propTypes = {
  request: PropTypes.object.isRequired,
};

export default Overridable.component(
  "InvenioRequests.RequestMetadata",
  RequestMetadata
);
