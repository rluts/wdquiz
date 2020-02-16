import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import {createStore, applyMiddleware, compose} from 'redux';
import quizReducer from "./reducers/quiz";
import ReduxThunk from 'redux-thunk';
import {Provider} from "react-redux";


const store = createStore(quizReducer, compose(applyMiddleware(ReduxThunk),
    window.devToolsExtension ? window.devToolsExtension() : f => f,));


const app = (
    <Provider store={store}>
        <App />
    </Provider>
);

ReactDOM.render(app, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
