import { connect } from "react-redux";
import ConfirmationModalComponent from "./ConfirmationModal";
import { startAction, closeModal } from "./state/actions";

const mapDispatchToProps = (dispatch) => ({
  startAction: () => dispatch(startAction()),
  closeModal: () => dispatch(closeModal()),
});

const mapStateToProps = (state) => ({
  modalIsOpen: state.confirmationModal.modalIsOpen,
  modalAction: state.confirmationModal.modalAction,
  modalText: state.confirmationModal.modalText,
  modalError: state.confirmationModal.modalError,
  isLoading: state.confirmationModal.isLoading,
});

export const ConfirmationModal = connect(
  mapStateToProps,
  mapDispatchToProps
)(ConfirmationModalComponent);
