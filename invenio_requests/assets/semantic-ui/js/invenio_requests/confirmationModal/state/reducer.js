import {
  OPEN_MODAL,
  CLOSE_MODAL,
  START_ACTION,
  ACTION_SUCCESS,
  HAS_ERROR,
} from "./actions";

const initialState = {
  modalIsOpen: false,
  modalAction: null,
  modalText: null,
  isLoading: false,
  modalError: null,
};

export const confirmationModalReducer = (state = initialState, action) => {
  switch (action.type) {
    case OPEN_MODAL:
      return {
        ...state,
        modalIsOpen: true,
        modalAction: action.payload.action,
        modalText: action.payload.text,
      };
    case CLOSE_MODAL:
      return initialState;
    case START_ACTION:
      return { ...state, isLoading: true };
    case ACTION_SUCCESS:
      return { ...state, isLoading: false };
    case HAS_ERROR:
      return { ...state, modalError: action.payload, isLoading: false };
    default:
      return state;
  }
};
