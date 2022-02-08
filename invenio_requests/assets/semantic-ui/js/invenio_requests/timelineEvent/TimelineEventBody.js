import React from "react";
import PropTypes from "prop-types";

export const TimelineEventBody = ({ content, format }) => {
  return format === "html" ? (
    <div dangerouslySetInnerHTML={{ __html: content }} />
  ) : (
    content
  );
};

TimelineEventBody.propTypes = {
  content: PropTypes.string,
  format: PropTypes.string,
};

TimelineEventBody.defaultProps = {
  content: "",
  format: "",
};
