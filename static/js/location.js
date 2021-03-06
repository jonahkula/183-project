let app = {};

let init = (app) => {
  // vue data
  app.data = {
    location_data: [],
    location_name: "",
    location_address: "",
    location_phone: "",
    location_stock: false,
    locations: {
      "Costco": {
        "img":"assets/new_Costco.png",
        "site": "https://www.costco.com/covid-vaccine.html",
      },
      "Ralphs": {
        "img": "assets/Ralphs.png",
        "site": "https://www.ralphs.com/rx/covid-eligibility",
      },
      "CVS": {
        "img":  "assets/CVS.png",
        "site": "https://www.cvs.com/immunizations/covid-19-vaccine",
      },
      "Rite": {
        "img": "assets/Riteaid.jpg",
        "site": "https://www.riteaid.com/pharmacy/covid-qualifier",
      },
      "SAFEWAY": {
        "img": "assets/new_safeway.png",
        "site": "https://www.safeway.com/pharmacy/covid-19.html",
      },
      "Walgreens": {
        "img": "assets/Walgreens.jpg",
        "site": "https://www.walgreens.com/findcare/vaccination/covid-19",
      },
      "Walmart": {
        "img": "assets/new_Walmart.png",
        "site": "https://www.walmart.com/cp/flu-shots-immunizations/1228302",
      },
      "Other": {
        "img": "assets/vaccine.jpg",
        "site": "https://www.cdc.gov/coronavirus/2019-ncov/vaccines/index.html",
      }
    },
    image: "",
    add_review_text: "",
    add_review_wait: "",
    add_review_service: "",
    add_review_vaccine: "",
    add_review_title: "",
    save_radius: "",
    save_zip: "",
    review_list: [],
    bad_input: false,
    save_state: "",
  };

  // displays the necessary images based on which review page is clicked on //
  app.display_image = () => {
    let image = app.vue.locations[app.vue.location_name.split(" ")[0]];
    if (image === undefined) {
      app.vue.image = app.vue.locations["Other"]["img"];
    } else {
      app.vue.image = image["img"];
    }
  };

  // displays dynamic information on the top of the review page //
  app.vaccine_site = () => {
    // console.log("In app.vaccine_site!!");
    // console.log("check app.vue.locations:", app.vue.locations[app.vue.location_name.split(' ')[0]]);
    let location = app.vue.locations[app.vue.location_name.split(' ')[0]];
    window.location.href = location !== undefined ? location["site"] : app.vue.locations["Other"]["site"];
  };

  // console.log("Check location_name:", app.vue.location_name);

  // relabel current rows
  app.enumerate = (a) => {
    let k = 0;
    a.map((e) => {
      e._idx = k++;
    });
    return a;
  };

  // initialize row specific fields
  app.complete = (a) => {
    a.map((e) => {
      e.name = "";
      e.show_review_likers = false;
      e.likers = 0;
      e.dislikers = 0;
      e.rating = 0;
      e.num_thumbs_display = 0;
      e.thread_list = [];
      e.thread_text = "";
    });
    return a;
  };

  // set review rating
  app.set_review_rating = (_idx, new_rating) => {
    let review = app.vue.review_list[_idx];

    if (review.rating === new_rating) {
      // if new rating is same as old, undo current rating
      // change review rating to 0, the unrated value, and update server
      review.rating = 0;
      axios.post(set_review_rating_url, {
        review_id: review.id,
        rating: review.rating,
      });

      // take user out of respective likers or dislikers number
      if (new_rating === 1) {
        review.likers--;
      } else if (new_rating === 2) {
        review.dislikers--;
      }
    } else {
      // update old rating to new rating
      // update review rating to new rating and update server
      let old_rating = review.rating;
      review.rating = new_rating;
      axios.post(set_review_rating_url, {
        review_id: review.id,
        rating: new_rating,
      });

      // add user to respective likers or dislikers total
      if (new_rating === 1) {
        // add user to likers total and delete from dislikers if applicable
        review.likers++;
        if (old_rating === 2) {
          review.dislikers--;
        }
      } else if (new_rating === 2) {
        // add user to dislikers total and delete from likers if applicable
        review.dislikers++;
        if (old_rating === 1) {
          review.likers--;
        }
      }
    }

    // update server with updated likers and dislikers totals
    axios.post(set_review_raters_url, {
      review_id: review.id,
      likers: review.likers,
      dislikers: review.dislikers,
    });
  };

  // display original rating after hover
  app.review_ratings_out = (_idx) => {
    let review = app.vue.review_list[_idx];
    review.num_thumbs_display = review.rating;
    review.show_review_likers = false;
  };

  // display hovered rating
  app.review_ratings_over = (_idx, rating) => {
    let review = app.vue.review_list[_idx];
    review.num_thumbs_display = rating;
    review.show_review_likers = true;

    // get current likers and dislikers of the review
    axios
      .get(get_review_raters_url, { params: { review_id: review.id } })
      .then((result) => {
        review.likers = result.data.likers;
        review.dislikers = result.data.dislikers;
      });
  };

  // adds review to db
  app.add_review = function () {
    // if any value is not filled out, return
    if (
      app.vue.add_review_service === "" ||
      app.vue.add_review_text === "" ||
      app.vue.add_review_title === "" ||
      app.vue.add_review_vaccine === "" ||
      app.vue.add_review_wait === ""
    ) {
      app.vue.bad_input = true;
      return;
    }

    // update server with new review
    axios
      .post(add_review_url, {
        text: app.vue.add_review_text,
        wait: app.vue.add_review_wait,
        service: app.vue.add_review_service,
        vaccine: app.vue.add_review_vaccine,
        title: app.vue.add_review_title,
        address: app.vue.location_address,
        location_name: app.vue.location_name,
      })
      .then(function (response) {
        app.vue.review_list.push({
          id: response.data.id,
          review_message: app.vue.add_review_text,
          wait_time: app.vue.add_review_wait,
          service: app.vue.add_review_service,
          vaccine: app.vue.add_review_vaccine,
          title: app.vue.add_review_title,
          name: response.data.name,
          rating: 0,
          num_thumbs_display: 0,
          likers: 0,
          dislikers: 0,
          show_review_likers: false,
          thread_list: [],
          thread_text: "",
        });
        app.enumerate(app.vue.review_list);
        app.review_input_clear();
        app.vue.bad_input = false;
      })
      .catch(function (error) {
        console.log("The error attempting to send a POST request:", error);
      });
  };

  // adds a new thread to db on a review
  app.add_review_thread = function (_idx) {
    let review = app.vue.review_list[_idx];

    // if input value is not filled out, return
    if (review.thread_text === "") {
      return;
    }

    // update server with new review thread message
    axios
      .post(add_review_thread_url, {
        review: review.id,
        thread_message: review.thread_text,
      })
      .then(function (response) {
        review.thread_list.push({
          id: response.data.id,
          thread_message: review.thread_text,
          thread_name: response.data.name,
        });
        app.enumerate(review.thread_list);
        review.thread_text = "";
      })
      .catch(function (error) {
        console.log("The error attempting to send a POST request:", error);
      });
  };

  // clear review input field
  app.review_input_clear = () => {
    app.vue.add_review_text = "";
    app.vue.add_review_wait = "";
    app.vue.add_review_title = "";
    app.vue.add_review_service = "";
    app.vue.add_review_vaccine = "";
  };

  app.save = () => {
    axios
      .post(save_url, {
        location_data: app.vue.location_data,
        zipCode: app.vue.save_zipCode,
        radius: app.vue.save_radius,
      })
      .then(
        app.vue.save_state = false
      )
  }

  app.unsave = () => {
    axios
      .post(unsave_url, {
        address: app.vue.location_address,
      })
      .then(
        app.vue.save_state = true
      )
  }

  // load reviews on location
  app.load = function () {
    axios
      .get(load_review_url, {
        params: {
          address: app.vue.location_address,
        },
      })
      .then(function (response) {
        let reviews = response.data.reviews;
        app.enumerate(reviews);
        app.complete(reviews);
        app.vue.review_list = reviews;
      })
      .then(() => {
        for (let review of app.vue.review_list) {
          axios
            .get(get_name_url, { params: { id: review.id } })
            .then((result) => {
              review.name = result.data.name;
            });
          axios
            .get(get_review_rating_url, { params: { review_id: review.id } })
            .then((result) => {
              review.rating = result.data.rating;
              review.num_thumbs_display = result.data.rating;
            });
          axios
            .get(load_review_thread_url, { params: { review: review.id } })
            .then((result) => {
              review.thread_list = result.data.threads;
            });
        }
      })
      .catch(function (error) {
        console.log("Error loading reviews");
      });
  };

  // contains all the methods.
  app.methods = {
    display_image: app.display_image,
    add_review: app.add_review,
    add_review_thread: app.add_review_thread,
    load: app.load,
    set_review_rating: app.set_review_rating,
    review_ratings_out: app.review_ratings_out,
    review_ratings_over: app.review_ratings_over,
    save: app.save,
    unsave: app.unsave,
    vaccine_site: app.vaccine_site,
  };

  // creates the vue instance
  app.vue = new Vue({
    el: "#vue-target",
    data: app.data,
    methods: app.methods,
  });

  // initialize vue instance
  app.init = async () => {
    try {
      // parsing a python dictionary that was converted to a string and turning it into a JavaScript Object.
      location_info = location_info.replace(/'/g, '"');
      location_info = location_info.replace("True", "true");
      location_info = location_info.replace("False", "false");
      location_info = JSON.parse(location_info);

      app.vue.location_data = location_info
      app.vue.save_radius = radius
      app.vue.save_zipCode = zipCode
      if (save_state == 'True') {
        app.vue.save_state = true
      } else if (save_state == 'False') {
        app.vue.save_state = false
      }
      
      // storing loaded information into vue
      const { name, address1, zip, phone, in_stock } = location_info;
      app.vue.location_name = name;
      app.vue.location_address = address1;
      app.vue.location_phone = phone;
      app.vue.location_stock = in_stock;

      // console.log("Check location_name:", app.vue.location_name);
      app.display_image();
      // load reviews
      app.load();
    } catch (error) {
      console.log(error);
    }
  };

  app.init();
};

init(app);
