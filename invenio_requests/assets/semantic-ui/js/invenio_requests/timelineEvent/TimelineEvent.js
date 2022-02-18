import FormattedInputEditor
  from '../components/FormattedInputEditor';
import React, { Component } from "react";
import {
  Feed,
  Image,
  Container,
  Dropdown,
  Label,
  Grid,
  Message,
} from "semantic-ui-react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";
import { SaveButton, CancelButton } from "../components/Buttons";
import { TimelineEventBody } from "./TimelineEventBody";

class TimelineEvent extends Component {
  // TODO i18n

  constructor(props) {
    super(props);

    const { event } = props;

    this.state = {
      commentContent: event?.payload?.content,
    };
  }

  render() {
    const {
      isLoading,
      isEditing,
      error,
      event,
      updateComment,
      deleteComment,
      toggleEditMode,
    } = this.props;
    const { commentContent } = this.state;

    const commentHasBeenEdited = event.revision_id > 1 && event.payload;
    const commentHasBeenDeleted = !event.payload;
    const commentCanBeDeleted = event.payload;

    return (
      <Overridable id="TimelineEvent.layout" event={event}>
        <Feed.Event>
          <Feed.Label>
            <Image src="/static/images/square-placeholder.png" as={Image} rounded />
          </Feed.Label>
          <Feed.Content>
            <Grid>
              <Grid.Row>
                <Grid.Column width={15}>
                  <Feed.Summary>
                    {/*TODO replace with event.icon and add a translated event description*/}
                    <Feed.User as="a">{event.created_by?.user}</Feed.User>{" "}
                    commented
                    <Feed.Date>{event.created}</Feed.Date>
                  </Feed.Summary>
                </Grid.Column>
                <Grid.Column width={1}>
                  {commentCanBeDeleted && (
                    <Dropdown icon="ellipsis horizontal">
                      <Dropdown.Menu>
                        <Dropdown.Item onClick={() => toggleEditMode()}>
                          Edit
                        </Dropdown.Item>
                        <Dropdown.Item onClick={() => deleteComment()}>
                          Delete
                        </Dropdown.Item>
                      </Dropdown.Menu>
                    </Dropdown>
                  )}
                </Grid.Column>
              </Grid.Row>
            </Grid>

            <Feed.Extra text className="timeline-event-body">
              {error && <Message negative>{error}</Message>}

              {isEditing ? (
                <FormattedInputEditor
                  data={event?.payload?.content}
                  onChange={(event, editor) =>
                    this.setState({ commentContent: editor.getData() })
                  }
                />
              ) : (
                <TimelineEventBody
                  content={event?.payload?.content}
                  format={event?.payload?.format}
                />
              )}

              {isEditing && (
                <Container className="mt-15" textAlign="right">
                  <CancelButton onClick={() => toggleEditMode()} />
                  <SaveButton
                    onClick={() => updateComment(commentContent, "html")}
                    loading={isLoading}
                  />
                </Container>
              )}
            </Feed.Extra>
            <Feed.Meta>
              {commentHasBeenEdited && "Edited"}
              {commentHasBeenDeleted && "Deleted"}
            </Feed.Meta>
          </Feed.Content>
        </Feed.Event>
      </Overridable>
    );
  }
}

TimelineEvent.propTypes = {
  event: PropTypes.object.isRequired,
  deleteComment: PropTypes.func.isRequired,
  updateComment: PropTypes.func.isRequired,
  toggleEditMode: PropTypes.func.isRequired,
  isLoading: PropTypes.bool,
  isEditing: PropTypes.bool,
  error: PropTypes.string,
};

export default Overridable.component("TimelineEvent", TimelineEvent);
