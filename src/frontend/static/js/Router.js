export class Router {
    constructor(routes) {
        this.routes = routes;
        this.initUI();
    }

    initUI() {
        window.addEventListener("hashchange", () => {
            this.handleRouteChange();
        })
        this.handleRouteChange();
    }

    handleRouteChange() {
        const currPath = window.location.hash.slice(1);
        const routeFunction = this.routes[currPath];
        routeFunction();
    }
}