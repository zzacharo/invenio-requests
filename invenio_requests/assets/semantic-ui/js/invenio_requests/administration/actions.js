import React, { Component } from "react";
import PropTypes from "prop-types";
import { Button } from "semantic-ui-react";
import { ModerationApi } from "./api";

export class ModerationActions extends Component {
  constructor(props) {
    super(props);
  }


  onClick = async (e, { dataName, dataActionKey }) => {
    const { resource } = this.props;

    const links = resource.links.actions;
    const action_link = links[dataActionKey];
    // Execute action
    try {
      if (action_link) {
        const result = await ModerationApi.execute_action(action_link);
        // TODO show a notification to the user. Should the entry be moved automatically? (if we have two tabs "Open"/"Closed")
      }
    } catch (e) {
      console.error(e);
    }
  };


  render() {
    const { actions } = this.props;
    return (
      <>
        {
          Object.entries(actions).map(([actionKey, actionConfig]) => {
            return (
              <Button
                key={actionKey}
                onClick={this.onClick}
                payloadSchema={actionConfig.payload_schema}
                dataName={actionConfig.text}
                dataActionKey={actionKey}
              >
                {actionConfig.text}
              </Button>
            );
          })
        }
      </>
    )
  }
}



ModerationActions.propTypes = {
};

ModerationActions.defaultProps = {
};
