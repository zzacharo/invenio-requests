import React from "react";
import { Modal, Button, Message } from "semantic-ui-react";
import PropTypes from "prop-types";

export const ConfirmationModal = ({
  modalIsOpen,
  modalText,
  closeModal,
  startAction,
  isLoading,
  modalError,
}) => {
  return (
    <Modal onClose={closeModal} open={modalIsOpen}>
      <Modal.Header>Confirm</Modal.Header>
      <Modal.Content>{modalText}</Modal.Content>
      <Modal.Actions>
        {modalError && (
          <Message negative compact>
            {modalError}
          </Message>
        )}

        <Button content="cancel" onClick={() => closeModal()} />
        <Button
          content="confirm"
          negative
          onClick={() => startAction()}
          loading={isLoading}
        />
      </Modal.Actions>
    </Modal>
  );
};

ConfirmationModal.propTypes = {
  modalIsOpen: PropTypes.bool,
  modalText: PropTypes.string,
  closeModal: PropTypes.func,
  startAction: PropTypes.func,
  isLoading: PropTypes.bool,
  modalError: PropTypes.string,
};

export default ConfirmationModal;
