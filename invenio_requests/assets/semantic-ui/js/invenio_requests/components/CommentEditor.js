import React from "react";
import Overridable from "react-overridable";
import { CKEditor } from "@ckeditor/ckeditor5-react";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import PropTypes from "prop-types";

const CommentEditor = (props) => {
  return <CKEditor {...props} />;
};

CommentEditor.propTypes = {
  editor: PropTypes.func,
  data: PropTypes.string,
  config: PropTypes.object,
  id: PropTypes.string,
  disabled: PropTypes.bool,
  onReady: PropTypes.func,
  onChange: PropTypes.func,
  onBlur: PropTypes.func,
  onFocus: PropTypes.func,
};

CommentEditor.defaultProps = {
  editor: ClassicEditor,
};

export default Overridable.component(
  "InvenioRequests.TimelineEventEditor",
  CommentEditor
);
