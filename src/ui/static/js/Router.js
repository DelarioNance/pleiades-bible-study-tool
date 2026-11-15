export class Router {
  constructor(routes) {
    this.routes = routes;
    this.initUI();
  }

  initUI() {
    // hashchange is used to detect when the user navigates 
    // to a different route in the SPA. Not very applicable 
    // to Pleiades since the user never navigates to a 
    // different UI page.
    window.addEventListener("hashchange", () => {
      this.handleRouteChange();
    });
    this.handleRouteChange();
  }

  handleRouteChange() {
    const currPath = window.location.hash.slice(1);
    const routeFunction = this.routes[currPath];
    routeFunction();
  }
}
