import Overridable from "react-overridable";
import Loader from "../components/Loader";
import { RequestActionsPortal } from "./actions/RequestActions";
import RequestDetails from "./RequestDetails";
import React, { Component } from "react";
import PropTypes from "prop-types";
import isEmpty from "lodash/isEmpty";

export class Request extends Component {
  componentDidMount() {
    const { initRequest } = this.props;
    initRequest();
  }

  render() {
    const { request } = this.props;

    return (
      <Overridable id="InvenioRequest.Request.layout">
        <Loader isLoading={isEmpty(request)}>
          <RequestActionsPortal request={request} />
          <RequestDetails request={request} />
        </Loader>
      </Overridable>
    );
  }
}

Request.propTypes = {
  request: PropTypes.object.isRequired,
  initRequest: PropTypes.func.isRequired,
};

export default Overridable.component("InvenioRequests.Request", Request);
