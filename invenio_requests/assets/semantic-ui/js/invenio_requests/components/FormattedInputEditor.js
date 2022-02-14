import React, { Component } from "react";
import Overridable from "react-overridable";
import CKEditor from "@ckeditor/ckeditor5-react";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import PropTypes from "prop-types";

function MinHeightPlugin(editor) {
  this.editor = editor;
}

function setMinHeight(minHeight) {

  MinHeightPlugin.prototype.init = function () {
    this.editor.ui.view.editable.extendTemplate({
      attributes: {
        style: {
          minHeight: minHeight,
        },
      },
    });
  };
  ClassicEditor.builtinPlugins.push(MinHeightPlugin);
}


class FormattedInputEditor extends Component {

  constructor(props) {
    super(props);
    const { minHeight } = this.props;
    if (minHeight !== undefined) {
      setMinHeight(minHeight);
    }
  }

  render() {
    return <CKEditor {...this.props} />;
  }
}

FormattedInputEditor.propTypes = {
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

FormattedInputEditor.defaultProps = {
  editor: ClassicEditor,
};

export default Overridable.component(
  "InvenioRequests.FormattedInputEditor",
  FormattedInputEditor
);
