import { http } from "react-invenio-forms";

const execute_action = async (apiEndpoint) => {
  return await http.post(apiEndpoint);
};

export const ModerationApi = {
  execute_action: execute_action,
};
