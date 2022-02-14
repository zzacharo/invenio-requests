import Overridable from "react-overridable";
import React, { Component } from "react";
import PropTypes from "prop-types";
import { Button, Message, Modal } from 'semantic-ui-react';

export class RequestActionModal extends Component {
  setOpen = (isOpen) => {
    const { setActionModalOpen, modalId } = this.props;
    setActionModalOpen(isOpen, modalId);
  };

  render() {
    const {
      action,
      loading,
      modalOpen,
      handleActionClick,
      modalId,
      error,
      children,
    } = this.props;
    return (
      <Overridable id="InvenioRequests.RequestActionModal.layout" {...this.props}>
        <Modal
          open={modalOpen.modalId === modalId && modalOpen.isOpen}
          trigger={
            <Button onClick={() => this.setOpen(true)} loading={loading}>
              {action}
            </Button>
          }
        >
          <Modal.Header>{action} request</Modal.Header>
          <Modal.Content>
            <Modal.Description>
              {error && (
                <Message
                  error
                  header="Something went wrong."
                  content={error.message}
                />
              )}
              {children}
            </Modal.Description>
          </Modal.Content>
          <Modal.Actions>
            <Button onClick={() => this.setOpen(false)}>Cancel</Button>
            <Button onClick={handleActionClick}>{action}</Button>
          </Modal.Actions>
        </Modal>
      </Overridable>
    );
  }
}

RequestActionModal.propTypes = {
  setActionModalOpen: PropTypes.func.isRequired,
  handleActionClick: PropTypes.func.isRequired,
};

export default Overridable.component(
  "InvenioRequests.RequestActionModal",
  RequestActionModal
);
