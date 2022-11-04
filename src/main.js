import { ViteSSG } from "vite-ssg";
import routes from "./js/router";
import App from './App.vue'

import './assets/main.css'

export const createApp = ViteSSG(
    App,
    { routes },
    ({ app, router, initialState }) => {

    }
)
