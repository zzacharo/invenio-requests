import EventWithStateComponent from "./TimelineEventWithState";
import { connect } from "react-redux";
import { updateComment, deleteComment } from "./state/actions";
import { openModal } from "../confirmationModal/state/actions";

const mapDispatchToProps = (dispatch) => ({
  openConfirmModal: (payload) => dispatch(openModal(payload)),
  updateComment: async (payload) => dispatch(updateComment(payload)),
  deleteComment: async (payload) => dispatch(deleteComment(payload)),
});

export const TimelineEventWithState = connect(
  null,
  mapDispatchToProps
)(EventWithStateComponent);
