import { connect } from 'react-redux';
import { performAction, setActionModalOpen } from './state/actions';
import RequestActionCmp from './RequestAction';
import RequestActionModalCmp from './RequestActionModal';

const mapDispatchToProps = (dispatch) => ({
  performAction: (action, payload) => dispatch(performAction(action, payload)),
});

const mapStateToProps = (state) => ({
  loading: state.requestAction.loading,
  error: state.requestAction.error,
});


export const RequestAction = connect(
  mapStateToProps,
  mapDispatchToProps
)(RequestActionCmp);


const mapDispatchToPropsModal = (dispatch) => ({
  setActionModalOpen: (isOpen, modalId) => dispatch(setActionModalOpen(isOpen, modalId)),
});

const mapStateToPropsModal = (state) => ({
  error: state.requestAction.error,
  modalOpen: state.requestAction.actionModalOpen,
});


export const RequestActionModal = connect(
  mapStateToPropsModal,
  mapDispatchToPropsModal
)(RequestActionModalCmp);
