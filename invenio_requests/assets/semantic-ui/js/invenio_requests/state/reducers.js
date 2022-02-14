import { timelineReducer } from "../timeline/state/reducer";
import { confirmationModalReducer } from "../confirmationModal/state/reducer";
import { commentEditorReducer } from "../timelineCommentEditor/state/reducer";
import { combineReducers } from "redux";
import {
  requestActionReducer
} from '../request/actions/state/reducer';
import {
  requestReducer
} from '../request/state/reducer';

export default function createReducers() {
  return combineReducers({
    timeline: timelineReducer,
    confirmationModal: confirmationModalReducer,
    timelineCommentEditor: commentEditorReducer,
    request: requestReducer,
    requestAction: requestActionReducer,
  });
}
