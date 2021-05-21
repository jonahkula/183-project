// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {
  // This is the Vue data.
  app.data = {
    // Complete as you see fit.
    first_name: "",
    last_name: "",
    email: "",
    saved_locations: [],
  };

  app.enumerate = (a) => {
    // This adds an _idx field to each element of the array.
    let k = 0;
    a.map((e) => {
      e._idx = k++;
    });
    return a;
  };

  // Redirects the user to the location page using the
  // zipcode, radius, location name, and address
  app.redirect_saved_location = (location_page, zip, rad, loc, addr) => {
    console.log(location_page);
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

  app.unsave_profile = function(index) {
    axios.post(unsave_profile_url, {
      address:app.vue.saved_locations[index][1]
    })
    .then(function() {
      app.vue.saved_locations.splice(index, 1);
      app.enumerate(app.vue.saved_locations);
      console.log("Success in Deleting Saved Location")
    })
  }

  // This contains all the methods.
  app.methods = {
    // Complete as you see fit.
    redirect_saved_location: app.redirect_saved_location,
    unsave_profile: app.unsave_profile,
  };

  // This creates the Vue instance.
  app.vue = new Vue({
    el: "#vue-target",
    data: app.data,
    methods: app.methods,
  });

  // And this initializes it.
  app.init = async () => {
    // Loading user info such as name, email, and saved locations
    const response = await axios.get(load_user_info_url);
    console.log("Successfully got response:", response);
    console.log(response.data["user_info"]);

    // Putting loaded user info into Vue
    user_info = response.data["user_info"];
    app.vue.first_name = user_info[0];
    app.vue.last_name = user_info[1];
    app.vue.email = user_info[2];
    if (user_info[3].length != 0) {
      app.vue.saved_locations = user_info[3];
      app.enumerate(app.vue.saved_locations)
    }
  };

  // Call to the initializer.
  app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
