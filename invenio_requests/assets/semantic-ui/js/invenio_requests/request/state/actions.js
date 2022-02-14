import isEmpty from "lodash/isEmpty";

export const REQUEST_INIT = "request/INIT";

export const initRequest = (newRequest) => {
  return async (dispatch, getState, config) => {
    if (isEmpty(newRequest)) {
      dispatch({
        type: REQUEST_INIT,
        payload: config.request,
      });
    }
    else{
      dispatch({
        type: REQUEST_INIT,
        payload: newRequest,
      });
    }
  };
};
