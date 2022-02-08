import { timelineReducer } from "../timeline/state/reducer";
import { confirmationModalReducer } from "../confirmationModal/state/reducer";
import { commentEditorReducer } from "../timelineCommentEditor/state/reducer";

import { combineReducers } from "redux";

export default function createReducers() {
  return combineReducers({
    timeline: timelineReducer,
    confirmationModal: confirmationModalReducer,
    timelineCommentEditor: commentEditorReducer,
  });
}
