import RequestComponent from './Request';
import { connect } from 'react-redux';
import { initRequest } from './state/actions'

const mapDispatchToProps = (dispatch) => ({
  initRequest: () => dispatch(initRequest()),
});

const mapStateToProps = (state) => ({
  request: state.request.data,
});

export const Request = connect(
  mapStateToProps,
  mapDispatchToProps
)(RequestComponent);

