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
    coordinates: {'longitude': '', 'latitude': ''},
    map: ""
  };

  app.enumerate = (a) => {
    // This adds an _idx field to each element of the array.
    let k = 0;
    a.map((e) => {
      e._idx = k++;
    });
    return a;
  };

  app.unsave_profile = function (index) {
    axios
      .post(unsave_profile_url, {
        address: app.vue.saved_locations[index][1],
      })
      .then(function () {
        app.vue.saved_locations.splice(index, 1);
        app.enumerate(app.vue.saved_locations);
        console.log("Success in Deleting Saved Location");
      });
  };

  // This contains all the methods.
  app.methods = {
    unsave_profile: app.unsave_profile,
  };

  app.mounted = function () {
    console.log("Check app.vue.coordinates before long & lat(1):", app.vue.coordinates);
    if (app.vue.coordinates !== "") {
      mapboxgl.accessToken = 'pk.eyJ1Ijoib29tZWxjaGUiLCJhIjoiY2twM2M2bXlxMDRxOTJ2bzZieXQ5cWZ5eSJ9.mRi_Q_vf9wrup84Lu_1wQA';
      console.log("Check app.vue.coordinates before long & lat:", app.vue.coordinates);
      let long = app.vue.coordinates['longitude'];
      let lat = app.vue.coordinates['latitude'];
      console.log("Check long & lat:", long, lat);
      app.vue.map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        // center: [long[long.length - 1], lat[lat.length - 1]]
      });
    }
  };

  // This creates the Vue instance.
  app.vue = new Vue({
    el: "#vue-target",
    data: app.data,
    created: app.init,
    methods: app.methods,
    mounted: app.mounted
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
      let location = user_info[3][0];
      app.vue.coordinates = {'longitude': location[4], 'latitude': location[5]};
      app.enumerate(app.vue.saved_locations);
    }
    console.log("Check user_info:", user_info, user_info[3][0], user_info[3]);
    console.log("Check app.vue.coordinates:", app.vue.coordinates);
  };

  // Call to the initializer.
  app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
