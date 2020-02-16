import {QUIZ_ANSWER, QUIZ_LOADED} from "../actions/constants";

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
        question: action.question,
        imageUrl: action.imageUrl,
        questionId: action.questionId
      };
    case QUIZ_ANSWER:
      return {
        ...state,
        right: action.right
      };
    default:
      return state
  }
};
export default quiz