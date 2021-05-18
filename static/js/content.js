// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {
  // This is the Vue data.
  app.data = {
    // Complete as you see fit.
    zipCode: "",
    radius: "",
    locations: [],
    savedLocations: [],
  };

  app.enumerate = (a) => {
    // This adds an _idx field to each element of the array.
    let k = 0;
    a.map((e) => {
      e._idx = k++;
    });
    return a;
  };

  app.add_locations = function () {
    axios
      .post(add_locations_url, {
        zipCode: app.vue.zipCode,
        radius: app.vue.radius,
      })
      .then(function (response) {
        app.vue.locations = response.data.content;
        app.vue.savedLocations = response.data.saved;
        console.log("Received response from POST request:", app.vue.locations);
      })
      .catch(function (error) {
        console.log("The error attempting to send a POST request:", error);
      });
  };

  app.save_option = function (index) {
    axios
      .post(save_url, {
        address: app.vue.locations[index],
        zipCode: app.vue.zipCode,
        radius: app.vue.radius,
      })
      .then(function (response) {
        // app.vue.savedLocations = response.data.saved
        console.log(
          "Received POST response after saving:",
          response.data.saved
        );

        // Doing this because the save/unsave response is not giving back saved data???
        axios.get(load_saved_url).then(function (response) {
          app.vue.savedLocations = response.data.saved;
          console.log("Saved stuff in here", app.vue.savedLocations);
        });
      })
      .catch(function (error) {
        console.log("There was an error sending the POST request:", error);
      });
  };

  app.unsave_option = function (index) {
    axios
      .post(unsave_url, {
        address: app.vue.locations[index],
      })
      .then(function (response) {
        // app.vue.savedLocations = response.data.saved
        console.log(
          "Received POST response after saving:",
          response.data.saved
        );

        // Doing this because the save/unsave response is not giving back saved data???
        axios.get(load_saved_url).then(function (response) {
          app.vue.savedLocations = response.data.saved;
          console.log("Saved stuff in here", app.vue.savedLocations);
        });
      })
      .catch(function (error) {
        console.log("There was an error sending the POST request:", error);
      });
  };

  app.redirect_location = (location_page, location_info) => {
    console.log(location_page);
    const zip = location_info["zip"];
    const rad = 25; // This can be configured to be faster, but for safety it is 25 for now.
    const loc = location_info["name"];
    const addr = location_info["address1"];
    console.log("ZIP IS:", zip);
    let queries = {
      ZIP_REMOVE: zip,
      RAD_REMOVE: rad,
      LOC_REMOVE: loc,
      ADDR_REMOVE: addr,
    };

    // Formatting url to make the link url compatible
    for (const [k, v] of Object.entries(queries)) {
      console.log(k, v);
      location_page = location_page.replace(k, v);
      location_page = location_page.replace(/ /g, "%20");
      location_page = location_page.replace("#", "%23");
    }
    console.log(location_page);

    // Redirects user to the location page
    window.location.replace(location_page);
  };

  // This contains all the methods.
  app.methods = {
    add_locations: app.add_locations,
    save_option: app.save_option,
    unsave_option: app.unsave_option,
    redirect_location: app.redirect_location,
  };

  // This creates the Vue instance.
  app.vue = new Vue({
    el: "#vue-target",
    data: app.data,
    methods: app.methods,
  });

  // And this initializes it.
  app.init = () => {
    axios
      .get(load_home_url)
      .then(function (response) {
        console.log("response to GET request:", response);
      })
      .catch(function (error) {
        console.log("The error attempting to send a GET request:", error);
      });
  };

  // Call to the initializer.
  app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code in it
init(app);
