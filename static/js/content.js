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
  };

  app.enumerate = (a) => {
    // This adds an _idx field to each element of the array.
    let k = 0;
    a.map((e) => {
      e._idx = k++;
    });
    return a;
  };

  app.add_locations = function() {
    axios.post(add_locations_url, {
      zipCode: app.vue.zipCode,
      radius: app.vue.radius
    })
    .then(function(response) {
      console.log("response to POST request:", response)
    })
    .catch(function(error) {
      console.log("The error attempting to send a POST request:", error)
    })
  };

  // This contains all the methods.
  app.methods = {
    // Complete as you see fit.
    add_locations: app.add_locations
  };

  // This creates the Vue instance.
  app.vue = new Vue({
    el: "#vue-target",
    data: app.data,
    methods: app.methods,
  });

  // And this initializes it.
  app.init = () => {
    axios.get(load_home_url)
    .then(function(response) {
      console.log("response to GET request:", response);
    })
    .catch(function(error) {
      console.log("The error attempting to send a GET request:", error);
    })
  };

  // Call to the initializer.
  app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code in it
init(app);
