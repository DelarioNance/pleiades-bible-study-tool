import { getIndexScreen } from "./screens/indexScreen.js";
import { Router } from "./Router.js";

const router = new Router({
    "": getIndexScreen,
})