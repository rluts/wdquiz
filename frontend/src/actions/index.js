import {QUIZ_NEW, QUIZ_ANSWER, QUIZ_LOADED} from './constants';
import axios from 'axios';

const apiUrl = 'http://localhost/api';

export const ask = () => {
  return (dispatch) => {
    return axios.post(`${apiUrl}/ask`)
      .then(response => {
        dispatch(quizLoaded(response.data))
      })
      .catch(error => {
        console.warn(error.response);
        dispatch(ask())
      });
  };
};

export const newQuiz = () => {
  return {
    type: QUIZ_NEW
  }
};

export const quizLoaded =  (data) => {
  return {
    type: QUIZ_LOADED,
    question: data.question,
    imageUrl: data.url,
    questionId: data.question_id
  }
};

export const check = (answer) => {
  return (dispatch) => {
    return axios.post(`${apiUrl}/check`, {answer})
      .then(response => {
        dispatch(answerChecked(response.data))
      })
      .catch(error => {
        throw(error);
      });
  };
};

export const answerChecked = (data) => {

  return {
    type: QUIZ_ANSWER,
    right: data.result === "OK",
  }
};
