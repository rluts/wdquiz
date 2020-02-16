import {QUIZ_LOAD, QUIZ_LOADED} from "../actions/constants";

const initialState = {
  loading: true
};

const quiz = (state = initialState, action) => {
  switch (action.type) {
    case QUIZ_LOADED:
      return [
        ...state,
        {}
      ];
    case QUIZ_LOAD:
      return [
        ...state,
        {}
      ];
    default:
      return state
  }
};
export default quiz