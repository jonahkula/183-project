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
    selection_done: false,
    img_url: "../static/assets/no-img.jpg",
  };

  app.file = null;

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

  app.select_file = function (event) {
    // Reads the file.
    let input = event.target;
    app.file = input.files[0];
    if (app.file) {
      // Making sure the image is less than 1MB, otherwise show an error.
      if (app.file.size > 1000000) {
        app.vue.img_url = "../static/assets/picture-too-big.png";
        return;
      }
      app.vue.selection_done = true;
      // We read the file.
      let reader = new FileReader();
      reader.addEventListener("load", function () {
        app.vue.img_url = reader.result;
        console.log(app.vue.img_url);
        localStorage.setItem(`${app.vue.email}`, app.vue.img_url);

        // Update it on the same page on the navbar
        let pfp = document.getElementById("pfp");
        pfp.src = localStorage.getItem(`${app.vue.email}`);
      });
      reader.readAsDataURL(app.file);
    }
  };

  // This contains all the methods.
  app.methods = {
    unsave_profile: app.unsave_profile,
    select_file: app.select_file,
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
      app.enumerate(app.vue.saved_locations);
    }

    if (localStorage.getItem(`${app.vue.email}`) !== null) {
      app.vue.img_url = localStorage.getItem(`${app.vue.email}`);
    }
  };

  // Call to the initializer.
  app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
