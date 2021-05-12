// This will be the object that will contain the Vue attributes
// and be used to initialize it.
console.log("hi");
console.log("hi");

let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {
  // This is the Vue data.
  app.data = {
    // Complete as you see fit.
    rating_cards: rating_cards,
    location_name: "",
    location_address: "",
  };

  app.enumerate = (a) => {
    // This adds an _idx field to each element of the array.
    let k = 0;
    a.map((e) => {
      e._idx = k++;
    });
    return a;
  };

  // This contains all the methods.
  app.methods = {
    // Complete as you see fit.
  };

  // This creates the Vue instance.
  app.vue = new Vue({
    el: "#vue-target",
    data: app.data,
    methods: app.methods,
  });

  // And this initializes it.
  app.init = () => {
    console.log("We are initializing the location page");

    // GET Request to get the information of the location
    axios.get(load_location_info_url).then((response) => {
      // Destructing the object to make it look neater.
      const { location_name, location_address } = response.data;

      // Storing the recevied information from the GET in Vue
      app.vue.location_name = location_name;
      app.vue.location_address = location_address;

      console.log("We have returned", app.vue.location_name);
      console.log("DONE LETS GO");
    });
  };

  // Call to the initializer.
  app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
console.log("hi");
init(app);
