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
    uploading: false,
    uploaded_file: "",
    uploaded: false,
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

  app.upload_complete = function (file_name, file_type) {
    app.vue.uploading = false;
    app.vue.upload_done = true;
    app.vue.uploaded_file = file_name;
  };

  app.upload_file = function (event) {
    // We need the event to find the file.
    let self = this;
    // Reads the file.
    let input = event.target;
    let file = input.files[0];
    if (file) {
      self.uploading = true;
      let file_type = file.type;
      let file_name = file.name;
      console.log(encodeURIComponent(file_name));
      // let full_url =
      //   file_upload_url +
      //   "&file_name=" +
      //   encodeURIComponent(file_name) +
      //   "&file_type=" +
      //   encodeURIComponent(file_type);
      // // Uploads the file, using the low-level streaming interface. This avoid any
      // // encoding.
      // app.vue.uploading = true;
      // let req = new XMLHttpRequest();
      // req.addEventListener("load", function () {
      //   app.upload_complete(file_name, file_type);
      //   console.log(file_name);
      // });
      // req.open("PUT", full_url, true);
      // req.send(file);
    }
  };

  // This contains all the methods.
  app.methods = {
    unsave_profile: app.unsave_profile,
    upload_file: app.upload_file,
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
