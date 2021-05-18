// This will be the object that will contain the Vue attributes
// and be used to initialize it.

let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {
  // This is the Vue data.
  app.data = {
    // Complete as you see fit.
    location_name: "",
    location_address: "",
    location_phone: "",
    location_stock: false,
    review_num: 0,
    review_message: "",
    review_avg_num: 0,
    locations: {
      "Costco": "assets/Costco.jpg",
      "Ralphs": "assets/Ralphs.jpg",
      "CVS": "assets/CVS.jpg",
      "Rite": "assets/Riteaid.jpg",
      "SAFEWAY": "assets/Safeway.jpg",
      "Walgreens": "assets/Walgreens.jpg",
      "Walmart": "assets/Walmart.jpg"
    }
  };

  // console.log("Check location_name:", app.vue.location_name);

  app.enumerate = (a) => {
    // This adds an _idx field to each element of the array.
    let k = 0;
    a.map((e) => {
      e._idx = k++;
    });
    return a;
  };

  // https://stackoverflow.com/questions/8358084/regular-expression-to-reformat-a-us-phone-number-in-javascript
  // app.formatPhoneNumber = function formatPhoneNumber(phoneNumberString) {
  //   var cleaned = ("" + phoneNumberString).replace(/\D/g, "");
  //   var match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
  //   if (match) {
  //     return "(" + match[1] + ") " + match[2] + "-" + match[3];
  //   }
  //   return null;
  // }

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
  app.init = async () => {
    try {
      // Parsing a python dictionary that was converted to a string
      // and turning it into a JavaScript Object.
      console.log("We are initializing the location page");
      location_info = location_info.replace(/'/g, '"');
      location_info = location_info.replace("True", "true");
      location_info = location_info.replace("False", "false");
      location_info = JSON.parse(location_info);
      console.log(location_info);

      // Storing loaded information into Vue
      const { name, address1, zip, phone, in_stock } = location_info;
      console.log(name, address1, zip, phone, in_stock);
      app.vue.location_name = name;
      app.vue.location_address = address1;
      app.vue.location_phone = phone;
      app.vue.location_stock = in_stock;

      console.log("Check location_name:", app.vue.location_name);

      // GET Request to get the information of the location
      // const location_response = await axios.get(load_location_info_url);
      // // app.vue.location_name = location_name;
      // // // Destructing the object to make it look neater.
      // // const { location_name, location_address } = location_response.data;

      // // // Storing the location information from the GET in Vue
      // // app.vue.location_name = location_name;
      // // app.vue.location_address = location_address;

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
