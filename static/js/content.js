// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {
  // This is the Vue data.
  app.data = {
    // Complete as you see fit.
    windowWidth: window.screen.width,
    zipCode: "",
    radius: "",
    locations: [],
    savedLocations: [],
    radii: [
      {
        distance: "10 miles",
      },
      {
        distance: "25 miles",
      },
      {
        distance: "50 miles",
      },
    ],
  };

  app.enumerate = (a) => {
    // This adds an _idx field to each element of the array.
    let k = 0;
    a.map((e) => {
      e._idx = k++;
    });
    return a;
  };

  app.get_radius = function (radius, event) {
    // console.log(
    //   "Check get_radius event.target.value, radius.distance:",
    //   event.target.value,
    //   radius.distance
    // );
    // console.log(typeof radius.distance);
    if (radius.distance !== undefined) {
      app.vue.radius = radius.distance.split(/\s+/)[0];
    }
  };

  app.add_locations = function () {
    // console.log("Check radius before sending POST:", app.vue.radius);
    axios
      .post(add_locations_url, {
        zipCode: app.vue.zipCode,
        radius: app.vue.radius,
      })
      .then(function (response) {
        app.vue.locations = response.data.content;
        app.vue.savedLocations = response.data.saved;
        sessionStorage.setItem("zipCode", app.vue.zipCode);
        sessionStorage.setItem("radius", app.vue.radius);
        // console.log("Hi", app.vue.radius);
        // console.log("Received response from POST request:", app.vue.locations);
      })
      .catch(function (error) {
        console.log("The error attempting to send a POST request:", error);
      });
  };

  app.save_option = function (index) {
    axios
      .post(save_url, {
        location_data: app.vue.locations[index],
        address: app.vue.locations[index]['address1'],
        name: app.vue.locations[index]['name'],
        zipCode: app.vue.zipCode,
        radius: app.vue.radius,
      })
      .then(function (response) {
        // app.vue.savedLocations = response.data.saved
        // console.log(
        //   "Received POST response after saving:",
        //   response.data.saved
        // );

        // Doing this because the save/unsave response is not giving back saved data???
        axios.get(load_saved_url).then(function (response) {
          app.vue.savedLocations = response.data.saved;
          // console.log("Saved stuff in here", app.vue.savedLocations);
        });
      })
      .catch(function (error) {
        console.log("There was an error sending the POST request:", error);
      });
  };

  app.unsave_option = function (index) {
    axios
      .post(unsave_url, {
        address: app.vue.locations[index]['address1'],
      })
      .then(function (response) {
        // app.vue.savedLocations = response.data.saved
        // console.log(
        //   "Received POST response after saving:",
        //   response.data.saved
        // );

        // Doing this because the save/unsave response is not giving back saved data???
        axios.get(load_saved_url).then(function (response) {
          app.vue.savedLocations = response.data.saved;
          // console.log("Saved stuff in here", app.vue.savedLocations);
        });
      })
      .catch(function (error) {
        console.log("There was an error sending the POST request:", error);
      });
  };

  // This contains all the methods.
  app.methods = {
    add_locations: app.add_locations,
    save_option: app.save_option,
    get_radius: app.get_radius,
    // unsave_option: app.unsave_option
    unsave_option: app.unsave_option,
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
        // console.log("response to GET request:", response);
      })
      .catch(function (error) {
        console.log("The error attempting to send a GET request:", error);
      });

    // If there is storage of the zipcode and radius, run it to show previous session when
    // clicking the back button.
    if (
      sessionStorage.getItem("zipCode") !== null &&
      sessionStorage.getItem("radius")
    ) {
      app.vue.zipCode = sessionStorage.getItem("zipCode");
      app.vue.radius = sessionStorage.getItem("radius");
      app.add_locations();
    }
  };

  // Call to the initializer.
  app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code in it
init(app);

let dropdown = document.getElementsByClassName("dropdown");
dropdown[0].addEventListener("click", function () {
  dropdown[0].classList.toggle("is-active");
});
