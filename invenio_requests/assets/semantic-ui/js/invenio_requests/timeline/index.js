import { connect } from "react-redux";
import { getTimelineWithRefresh, timelineStopRefresh } from "./state/actions";
import TimelineFeedComponent from "./TimelineFeed";

const mapDispatchToProps = (dispatch) => ({
  getTimelineWithRefresh: () => dispatch(getTimelineWithRefresh()),
  timelineStopRefresh: () => dispatch(timelineStopRefresh()),
});

const mapStateToProps = (state) => ({
  loading: state.timeline.loading,
  refreshing: state.timeline.refreshing,
  timeline: state.timeline.data,
  error: state.timeline.error,
});

export const Timeline = connect(
  mapStateToProps,
  mapDispatchToProps
)(TimelineFeedComponent);
