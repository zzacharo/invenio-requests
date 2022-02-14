import FormattedInputEditor from "../../components/FormattedInputEditor";
import React, { Component } from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";
import { Divider, Modal } from "semantic-ui-react";
import { RequestActionModal } from "./index";

export class RequestAction extends Component {
  constructor(props) {
    super(props);
    this.state = { actionComment: "", modalOpen: false };
  }

  onCommentChange = (event, editor) => {
    this.setState({ actionComment: editor.getData() });
  };

  handleActionClick = () => {
    const { action, performAction } = this.props;
    const { actionComment } = this.state;
    performAction(action, actionComment);
  };

  render() {
    const { action, loading } = this.props;
    return (
      <Overridable id="InvenioRequests.RequestAction.layout" {...this.props}>
        <RequestActionModal
          action={action}
          loading={loading}
          handleActionClick={this.handleActionClick}
          modalId={action}
        >
          <Modal.Content>
            <Modal.Description>
              Comment on your {action} request action (optional).
              <Divider hidden />
              <FormattedInputEditor onChange={this.onCommentChange} />
            </Modal.Description>
          </Modal.Content>
        </RequestActionModal>
      </Overridable>
    );
  }
}

RequestAction.propTypes = {
  action: PropTypes.string.isRequired,
  performAction: PropTypes.func.isRequired,
  loading: PropTypes.bool,
};

RequestAction.defaultProps = {
  loading: false,
};

export default Overridable.component(
  "InvenioRequests.RequestAction",
  RequestAction
);
