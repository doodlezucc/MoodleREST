import { ViteSSG } from "vite-ssg";
import routes from "./router/index";
import App from './App.vue'

import './assets/main.css'

export const createApp = ViteSSG(
    App,
    { routes },
    // function to have custom setups
    ({ app, router, initialState }) => {
        console.log("custom setup here :)")
    }
)
