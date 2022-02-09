export const IS_LOADING = "timeline/IS_LOADING";
export const SUCCESS = "timeline/SUCCESS";
export const HAS_ERROR = "timeline/HAS_ERROR";
export const IS_REFRESHING = "timeline/REFRESHING";

class intervalManager {
  static IntervalId = undefined;

  static setIntervalId(intervalId) {
    this.intervalId = intervalId;
  }
}

const fetchTimeline = (loadingState = true) => {
  return async (dispatch, getState, config) => {
    if (loadingState) {
      dispatch({
        type: IS_LOADING,
      });
    }
    dispatch({
      type: IS_REFRESHING,
    });
    try {
      const response = await config.apiClient.getTimeline();
      dispatch({
        type: SUCCESS,
        payload: response.data,
      });
    } catch (error) {
      dispatch({
        type: HAS_ERROR,
        payload: error,
      });
    }
  };
};

const timelineReload = (dispatch, getState, config) => {
  const state = getState();
  const { loading, refreshing, error } = state.timeline;
  const intervalId = intervalManager.intervalId;
  if (error) {
    // stop requesting if error
    clearInterval(intervalId);
  }
  // avoid concurrent requests if the previous one did not finish
  return !loading && !refreshing && dispatch(fetchTimeline(false));
};

export const getTimelineWithRefresh = () => {
  return async (dispatch, getState, config) => {
    dispatch(fetchTimeline());
    const intervalId = setInterval(
      () => timelineReload(dispatch, getState, config),
      config.refreshIntervalMs
    );
    intervalManager.setIntervalId(intervalId);
  };
};

export const timelineStopRefresh = () => {
  return (dispatch, getState, config) => {
    const intervalId = intervalManager.intervalId;
    clearInterval(intervalId);
  };
};
