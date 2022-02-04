import {
  RequestActions
} from './request/RequestActions';
import {
  InvenioRequestsTimelineAPI,
  RequestLinkExtractor,
  RequestEventsApi,
  RequestEventsLinkExtractor,
} from "./api/api";
import React, { Component } from "react";
import PropTypes from "prop-types";
import { configureStore } from "./store";
import { OverridableContext } from "react-overridable";
import RequestDetails from "./RequestDetails";
import { Provider } from "react-redux";

export class InvenioRequestsApp extends Component {
  constructor(props) {
    super(props);
    const { requestsApi, requestEventsApi, request } = this.props;

    const defaultRequestsApi = new InvenioRequestsTimelineAPI(
      new RequestLinkExtractor(request.links)
    );
    const defaultRequestEventsApi = (commentLinks) =>
      new RequestEventsApi(new RequestEventsLinkExtractor(commentLinks));

    const appConfig = {
      requestsApi: requestsApi || defaultRequestsApi,
      request,
      requestEventsApi: requestEventsApi || defaultRequestEventsApi,
      refreshIntervalMs: 5000,
    };

    this.store = configureStore(appConfig);
  }

  render() {
    const { overriddenCmps, request } = this.props;
    return (
      <OverridableContext.Provider value={overriddenCmps}>
        <Provider store={this.store}>
          <RequestActions />
          <RequestDetails request={request} />
        </Provider>
      </OverridableContext.Provider>
    );
  }
}

InvenioRequestsApp.propTypes = {
  requestsApi: PropTypes.object,
  requestEventsApi: PropTypes.object,
  overriddenCmps: PropTypes.object,
  request: PropTypes.object.isRequired,
};

InvenioRequestsApp.defaultProps = {
  overriddenCmps: {},
  requestsApi: null,
};
