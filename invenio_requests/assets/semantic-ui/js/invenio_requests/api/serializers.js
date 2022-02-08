export const payloadSerializer = (content, format) => ({
  payload: {
    content,
    format,
  },
});

export const errorSerializer = (error) =>
  error?.response?.data?.message || error?.message;
