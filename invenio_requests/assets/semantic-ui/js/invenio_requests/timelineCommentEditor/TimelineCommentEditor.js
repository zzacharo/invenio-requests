import FormattedInputEditor from '../components/FormattedInputEditor';
import React from "react";
import { SaveButton } from "../components/Buttons";
import { Container, Message } from "semantic-ui-react";
import PropTypes from "prop-types";

const TimelineCommentEditor = ({
  isLoading,
  commentContent,
  setCommentContent,
  error,
  submitComment,
}) => {
  return (
    <Container className="timeline-comment-editor-container">
      {error && <Message negative>{error}</Message>}
      <FormattedInputEditor
        data={commentContent}
        onChange={(event, editor) => setCommentContent(editor.getData())}
        minHeight="200px"
      />
      <Container className="mt-10" textAlign="right">
        <SaveButton
          icon="send"
          size="medium"
          content="Comment"
          loading={isLoading}
          onClick={() => submitComment(commentContent, "html")}
        />
      </Container>
    </Container>
  );
};

TimelineCommentEditor.propTypes = {
  commentContent: PropTypes.string,
  isLoading: PropTypes.bool,
  setCommentContent: PropTypes.func,
  error: PropTypes.string,
  submitComment: PropTypes.func,
};

export default TimelineCommentEditor;
