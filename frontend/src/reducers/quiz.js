import {QUIZ_ANSWER, QUIZ_LOADED, QUIZ_NEW} from "../actions/constants";

const initialState = {
  loading: true,
  question: null
};

const quiz = (state = initialState, action) => {
  switch (action.type) {
    case QUIZ_LOADED:
      return {
        ...state,
        loading: false,
        answered: false,
        right: false,
        question: action.question,
        imageUrl: action.imageUrl,
        questionId: action.questionId
      };
    case QUIZ_ANSWER:
      return {
        ...state,
        right: action.right,
        answered: true
      };
    case QUIZ_NEW:
      return {
        ...state,
        answered: false,
        loading: true,
      };
    default:
      return state
  }
};
export default quiz