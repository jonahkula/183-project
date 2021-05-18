// This will be the object that will contain the Vue attributes
// and be used to initialize it.

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
    review_num: 0,
    review_message: "",
    review_avg_num: 0,
    add_review_text: "",
    add_review_wait: "",
    add_review_service: "",
    add_review_vaccine: "",
    add_review_title: "",
    review_list: [],
  };

  app.enumerate = (a) => {
    // This adds an _idx field to each element of the array.
    let k = 0;
    a.map((e) => {
      e._idx = k++;
    });
    return a;
  };

  // Adds a review to the review db and push to current review_list
  // Saving to db not implemented yet
  // Working on pushing to review_list
  app.add_review = function() {

    axios.post(add_review_url, {
      text: app.vue.add_review_text,
    })
    .then(function(response) {
      app.vue.review_list.push({
      text:app.vue.add_review_text,
      wait:app.vue.add_review_wait,
      service:app.vue.add_review_service,
      vaccine:app.vue.add_review_vaccine,
      title:app.vue.add_review_title,
      name:response.data.name,
    })
    app.vue.add_review_text = ""
    app.vue.add_review_wait = ""
    app.vue.add_review_title = ""
      console.log("Received response from POST request:", response.data)
    })
    .catch(function(error) {
      console.log("The error attempting to send a POST request:", error)
    })

  }

  // This contains all the methods.
  app.methods = {
    // Complete as you see fit.
    add_review: app.add_review,
  };

  // This creates the Vue instance.
  app.vue = new Vue({
    el: "#vue-target",
    data: app.data,
    methods: app.methods,
  });

  // And this initializes it.
  app.init = async () => {
    try {
      console.log("We are initializing the location page");

      // GET Request to get the information of the location
      const location_response = await axios.get(load_location_info_url);

      // Destructing the object to make it look neater.
      const { location_name, location_address } = location_response.data;

      // Storing the location information from the GET in Vue
      app.vue.location_name = location_name;
      app.vue.location_address = location_address;

      // GET Request to get the information of the location reviews
      const review_response = await axios.get(load_review_info_url);

      // Destructing the object to make it look neater.
      const { review_num, review_avg_num, review_message } =
        review_response.data;

      // Storing the location review information from the GET in Vue
      app.vue.review_num = review_num;
      app.vue.review_message = review_message;
      app.vue.review_avg_num = review_avg_num;
    } catch (error) {
      console.log(error);
    }
  };

  // Call to the initializer.
  app.init();
};

// This takes the (empty) app object, and initializes it,
init(app);
