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
    map: "",
    all_markers: [],
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
        console.log("Check all_markers before:", app.vue.all_markers);
        app.vue.saved_locations.splice(index, 1);
        app.vue.all_markers[index].remove();
        app.vue.all_markers.splice(index, 1);
        app.enumerate(app.vue.saved_locations);
        console.log("Check all_markers after removal:", app.vue.all_markers);
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

  app.mounted = function () {
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
      app.enumerate(app.vue.saved_locations);
      let lastLocation = app.vue.saved_locations[user_info[3].length - 1];
      let long = lastLocation[4];
      let lat = lastLocation[5];
      mapboxgl.accessToken = 'pk.eyJ1Ijoib29tZWxjaGUiLCJhIjoiY2twM2M2bXlxMDRxOTJ2bzZieXQ5cWZ5eSJ9.mRi_Q_vf9wrup84Lu_1wQA';
      app.vue.map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [long, lat], // where the map is initially centered at
        zoom: 12 // initial zoom level
      });

      // add the long & lat to the map db //
      axios.post(
        save_map_url,
        {
          longitude: long,
          latitude: lat
        });

      const geojson = {
        'type': 'FeatureCollection',
        'features': []
      };

      app.vue.saved_locations.forEach(location => {
        app.vue.coordinates = {'longitude': location[4], 'latitude': location[5]};
        long = app.vue.coordinates['longitude'];
        lat = app.vue.coordinates['latitude'];
        const store = location.slice(0, 1)[0].split("#")[0].trim();
        const address = location.slice(1, 2)[0].split("#")[0].trim();
        const zipCode = location.slice(2, 3);

        geojson['features'].push({
          'type': 'Feature',
          'geometry': {
            'type': 'Point',
            'coordinates': [long, lat]
          },
          'properties': {
            'store': store,
            'address': address,
            'zipCode': zipCode,
            'icon': 'pharmacy-15'
          }
        });

      });

      // add a fullscreen feature //
      app.vue.map.addControl(new mapboxgl.FullscreenControl());
        
      // adds zoom in/out functionality //
      const nav = new mapboxgl.NavigationControl({
        showCompass: false
      });
      app.vue.map.addControl(nav, 'top-left');

      const element = document.getElementsByClassName('marker');
      let index = 0;
      geojson.features.forEach( (location) => { 

        let marker = new mapboxgl.Marker(element[index])
        .setLngLat(location.geometry.coordinates)
        .setPopup(new mapboxgl.Popup().setHTML('<b>' + location.properties.store + '</b>' + 
                                               '<p>' + location.properties.address + ", " + location.properties.zipCode + "</p>")) // only need the store, address, & zipcode
        .addTo(app.vue.map);
        index++;
        app.vue.all_markers.push(marker);
      });
      console.log("Check all_markers after:", app.vue.all_markers);
    } else {
      console.log("In else statement currently");
      axios.get(
        load_map_url
      )
      .then( (response) => {
        mapboxgl.accessToken = 'pk.eyJ1Ijoib29tZWxjaGUiLCJhIjoiY2twM2M2bXlxMDRxOTJ2bzZieXQ5cWZ5eSJ9.mRi_Q_vf9wrup84Lu_1wQA';
        app.vue.map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [response.data['longitude'], response.data['latitude']], // where the map is initially centered at
        zoom: 12 // initial zoom level
        });
        // add a fullscreen feature //
        app.vue.map.addControl(new mapboxgl.FullscreenControl());
          
        // adds zoom in/out functionality //
        const nav = new mapboxgl.NavigationControl({
          showCompass: false
        });
        app.vue.map.addControl(nav, 'top-left');
      });
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
