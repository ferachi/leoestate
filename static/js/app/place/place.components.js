/**
 * Module PlaceComponents
 *
 * @desc the components module for the module called Place
 * @type {Module}
 */
var app = angular.module('place.components', []);

/**
 * SearchComponent
 * @name search
 * @type {Component}
 * @desc component to handle search  for Place Module
 */
app.component('search', {
    templateUrl:'/static/place/templates/place_search.component.html',
    controller:'SearchCtrl',
    bindings : {
        searchExp : '=',
        options : '='
    }
});

/**
 * SearchController
 * @name search controller
 * @type {Controller}
 * @desc controller for the search component
 */
app.controller('SearchCtrl', ['$timeout',function($timeout){
    this.$onInit = function(){
        this.isAdvancedSearch = true;
        // this.searchExp={slug: 'kappa'};
    }

}])


/**
 * SearchBarComponent
 * @name search bar
 * @type {Component}
 * @desc component to handle quick search within the search component
 */
app.component('searchBar', {
    templateUrl:'/static/place/templates/place_search-bar.component.html',
    controller:'SearchBarCtrl',
    bindings : {
        searchExp : "="
    }
});

/**
 * SearchBarController
 * @name search bar controller
 * @type {Controller}
 * @desc controller for the search bar component
 */
app.controller('SearchBarCtrl', [function(){
    this.$onInit = function(){
        var self = this;
        this.purchaseTypes = [
            {label:'All', value:""},
            {label:'Buy', value:'buyableplace'},
            {label:'Rent', value:'rentableplace'}
        ];
        this.location = "";
        this.purchaseType = "";
        // self.searchExp  = {other_fields:{$:'gas',$:'chimney'}};
        self.searchExp  = function(values,index){

            for(var j=0; j < Object.keys(values).length ; j++)
            {
                var value = Object.keys(values)[j];
                if(values['buyableplace'] && !'buyableplace'.startsWith(self.purchaseType)) return false;
                else if(values['rentableplace'] && !'rentableplace'.startsWith(self.purchaseType)) return false;

                if(!values["address"]['location'].startsWith(self.location)) return false;
                return true
            }

        }
    }

    this.change = function(){
    }
}]);


/**
 * SearchPaneComponent
 * @name search pane
 * @type {Component}
 * @desc component to handle advanced search within the search component
 */
app.component('searchPane', {
    templateUrl:'/static/place/templates/place_search-pane.component.html',
    controller:'SearchPaneCtrl',
    bindings : {
        searchExp : '=',
        options : '='
    }
});


/**
 * SearchPaneController
 * @name search pane controller
 * @type {Controller}
 * @desc controller for the search pane component
 */
app.controller('SearchPaneCtrl', ['utils',function(utils){
    this.propertyOptions = [];
    this.propertyTypes = [];
    this.facilityOptions = [];
    this.location = "";
    this.showFacilities = false;
    this.$onInit = function(){
        var self = this;
        this._facilityOptions = [];
        this._propertyTypeOptions = [];
        this._otherOptions = [];
        angular.copy(this.options['facilities'] , this._facilityOptions);
        angular.copy(this.options['propertyTypes'] , this._propertyTypeOptions);
        angular.copy(this.options['otherFields'] , this._otherOptions);
        this._noOfRoomOptions = [{id:1, val:"1"},{ id:2, val:"2"}, {id:3, val : "3"}, {id:4, val:"4"}, {id:5, val:"5"}, {id:6, val:"6+"}];

        this.purchaseType = "";
        this.purchaseTypes = [
            {label:'All', value:""},
            {label:'Buy', value:'buyableplace'},
            {label:'Rent', value:'rentableplace'}
        ];
        this.durations = [
            {label:'Week', value:"w"},
            {label:'Month', value:'m'},
            {label:'Year', value:'y'}
        ];
        this.ages = [
            {label:'Any', value:''},
            {label:'Old', value:'o'},
            {label:'New', value:'n'}
        ]
        this.age = "";
        this.duration = "m";
        this.propertyType = "";
        this.price = [0,1000000];
        this.area = "";
        this.rooms ="";
        this.priceMinMax = [0,1000000];

        self.searchExp  = function(values,index){
            var location = parseInt(self.location);
            if(!isNaN(location)){
                var zipcode = values["address"]['zip_code']+'';
                var _zip = self.location + '';
                if(!zipcode.startsWith(_zip)) return false;
            }
            else{
                if(!values["address"]['location'].toLowerCase().startsWith(self.location.toLowerCase())) return false;
            }

            if(!values["property_type"].startsWith(self.propertyType)) return false;

            if(self.price[1] < self.priceMinMax[1]){
                if(self.price[1] < parseInt(values['price'])  || self.price[0] > parseInt(values['price'])) return false;
            }
            else{
                if(self.price[0] > parseInt(values['price'])) return false;
            }

            if(self.area && self.area > parseInt(values['area'])) return false;

            if(self.rooms && self.rooms < 6){
                if(self.rooms < parseInt(values['no_rooms'])) return false;
            }
            else if(self.rooms && self.rooms >= 6){
                if(self.rooms > parseInt(values['no_rooms'])) return false;
            }

            // if(self.rooms[1] < self.roomMinMax[1]){
            //     if(self.rooms[1] < parseInt(values['no_rooms'])  || self.rooms[0] > parseInt(values['no_rooms'])) return false;
            // }
            // else{
            //     if(self.rooms[0] > parseInt(values['no_rooms'])) return false;
            // }


            // returns an array of the  name fields in facilities
            var _facilityValues = utils.valuesToArray(values["facilities"],'name');

            // if any facility is selected
            // note: this ensures that a property has all the selected options
            if(self.facilityOptions.length > 0){
                var _indexes = [];
                self.facilityOptions.forEach(function(value){
                    var _index = _facilityValues.indexOf(value);
                    _indexes.push(_index);
                });
                if(_indexes.indexOf(-1) != -1) return false;
            }

            // // this works if any property has at least on of the selected facilities
            // if(self.facilityOptions.length > 0){
            // 	var _index;
            // 	self.facilityOptions.forEach(function(value){
            // 		_index = _facilityValues.indexOf(value);
            // 		if(_index == -1) return;
            // 	});
            // 	if(_indexes == -1) return false;
            // }

            var _optionsValues = utils.valuesToArray(values["other_fields"],'field_name');
            if(self.propertyOptions.length > 0){
                var _indexes = [];
                console.log(self.propertyOptions, _optionsValues)
                self.propertyOptions.forEach(function(value){
                    var _index = _optionsValues.indexOf(value);
                    _indexes.push(_index);
                });
                if(_indexes.indexOf(-1) != -1) return false;
            }
            return true
        }
    };

    this.change = function(){
        console.log(this.room)
    }
    this.facilitiesChanged = function(){
        var self = this;
        this._facilityOptions.forEach(function(v,i){
            if("selected" in v){
                if(v['selected']){
                    if(self.facilityOptions.indexOf(v['name']) === -1)
                        self.facilityOptions.push(v['name']);
                }
                else{
                    var index = self.facilityOptions.findIndex(function(n){
                        return n === v['name'];
                    });
                    if(index != -1){
                        self.facilityOptions.splice(index,1);
                    }
                }
            }
        });
    }
    this.propertyTypeChanged = function(){
        var self = this;
        this._propertyTypeOptions.forEach(function(v,i){
            if("selected" in v){
                if(v['selected']){
                    if(self.propertyTypes.indexOf(v['name']) === -1)
                        self.propertyTypes.push(v['name']);
                }
                else{
                    var index = self.propertyTypes.findIndex(function(n){
                        return n === v['name'];
                    });
                    if(index != -1){
                        self.propertyTypes.splice(index,1);
                    }
                }
                console.log(self.propertyTypes);
            }
        });
    }
    this.optionsChanged = function(){
        var self = this;

        this._otherOptions.forEach(function(v,i){
            if("selected" in v){
                if(v['selected']){
                    if(self.propertyOptions.indexOf(v['field_name']) === -1)
                        self.propertyOptions.push(v['field_name']);
                }
                else{
                    var index = self.propertyOptions.findIndex(function(n){
                        return n === v['field_name'];
                    });
                    if(index != -1){
                        self.propertyOptions.splice(index,1);
                    }
                }
            }
            console.log(self._otherOptions,self.propertyOptions)
        });
    }
}]);


/**
 * MapComponent
 * @name map
 * @type {Component}
 * @desc component to handle the map functionality
 */

app.component('map', {
    templateUrl:'/static/place/templates/place_map.component.html',
    controller:'MapCtrl',
    bindings:{
        places:"=",
        searchExp : "=",
    }
});


/**
 * MapController
 * @name map controller
 * @type {Controller}
 * @desc controller for the map component
 */
app.controller('MapCtrl', ['$filter','$scope','$interval', '$http',function($filter, $scope, $timeout,$http){
    this.title = "Map";
    var self = this;
    self.placeCount;
    this.$onInit = function(){
        var filter = $filter('filter');
        var _places, villes, latCenter, longCenter;

        $http.get("/static/location_final.json").then(function(response){
            villes = response.data;
        }, function(err){
            console.log(err);
        });

        $scope.places = this.places;
        $timeout(function(){
            $scope.places = filter(self.places,self.searchExp);
        },10);
        $scope.$watchCollection('places',function(n,o){
            if(n !== o) {
                _places = [];
                var ville;
                $scope.places.forEach(function (place) {
                    var lat = parseFloat(place.address.latitude);
                    var lng = parseFloat(place.address.longitude);
                    var zip = parseInt(place.address.zip_code);
                    var location = place.address.location;
                    var latlng = {lat: lat, lng: lng};
                    var title = place.title;
                    var price = place.price;
                    var slug = place.slug;
                    var imgUrl = place.image;
                    _places.push({title: title, latlng: latlng, zip:zip,location:location, image: imgUrl, price: price, slug: slug});
                });

                if(_places.length > 0){



                    var city = _places[0].location.toUpperCase();
                    var zip = _places[0].zip;

                    var sameCity = _.every(_places,function(place){
                        return place.location == city;
                    });
                    var sameZip = _.every(_places,function(place){
                        return place.zip == zip;
                    });
                    if(sameCity){
                        ville = _.findWhere(villes, {place:city});
                    }
                    else if(sameZip){
                        ville = _.findWhere(villes, {zip:zip});
                    }
                    else{
                        ville = null;
                    }

                    // if the location field is not empty
                    if(ville){
                        latCenter = ville.latitude;
                        longCenter = ville.longitude;
                    }
                    else{
                        // location field must be empty or different locations where selected
                        latCenter = _places.map(function (place){
                            return place.latlng.lat;
                        }).reduce(function (acc, val, index, list) {
                            if (index == list.length - 1) return (acc + val) / list.length;
                            else return acc + val;
                        });
                        longCenter = _places.map(function (place) {
                            return place.latlng.lng;
                        }).reduce(function (acc, val, index, list) {
                            if (index == list.length - 1) return (acc + val) / list.length;
                            else return acc + val;
                        });
                    }
                }
                else{
                    latCenter = 45;
                    longCenter = 5;
                }
                var center = {lat: latCenter, lng: longCenter};
                var mapOptions = {
                    zoom: 10,
                    center: center,
                    mapTypeControl: false,
                };
                self.map = new google.maps.Map(document.getElementById("map"), mapOptions);

                _places.forEach(function (place) {
                    var marker = new google.maps.Marker({
                        position: place.latlng,
                        title: place.title,
                        map: self.map,
                    });
                    marker.addListener('click', function () {
                        infowindow.setContent(contentInfo(place.image, place.title, place.price))
                        infowindow.open(map, marker);
                    });
                });
            }

        });

        var infowindow = new google.maps.InfoWindow({
            maxWidth:200
        });

    };

    function contentInfo(img, name, price, slug){
        var content = ' <div id="content" style="width: 200px;">'+
            '<img  class="img-responsive center-block" src="'+img+'" alt="'+name+'">'+
            '<h4>'+name+'</h4>'+
            '<h4>&euro;'+price+'</h4>'+
            '</div>';
        return content;
    }
}]);

/**
 * ProperyListComponent
 * @name property list
 * @type {Component}
 * @desc component to handle the listing of the places functionality
 */

app.component('propertyList', {
    templateUrl:'/static/place/templates/place_property-list.component.html',
    controller:'PropertyListCtrl',
    bindings : {
        places : "=",
        searchExp : "=",
        showDetail:"&",
    }
});


/**
 * PropertyListController
 * @name property list controller
 * @type {Controller}
 * @desc controller for the property list component
 */
app.controller('PropertyListCtrl', [function(){
    var self = this;
    this.title = "Propery List";

    var count = 10;


    this.$onInit = function(){
        this.inc = count;
        this.isComplete = this.inc >= this.places.length? true : false;

    };
    this.navToDetail = function(isList, place){
        this.showDetail({isList:isList,place:place});
    };

    this.loadMore = function(){
        this.inc = this.inc + count;
        this.isComplete = this.inc >= this.places.length? true : false;

    }
}]);


/**
 * propertyPaletteComponent
 * @name property palette
 * @type {Component}
 * @desc component that is a thumbnail for each individual place
 */
app.component('propertyPalette',{
        templateUrl: '/static/place/templates/place_property-palette.component.html',
        controller : 'PropertyPaletteController',
        bindings:{
            property:'=place',
            showDetail: '&',
        },

    }
);


/**
 * PropertyPaletteController
 * @name property list controller
 * @type {Controller}
 * @desc controller for the property palette component
 */
app.controller('PropertyPaletteController', ["$location",function($location){
    this.$onInit = function(){
    }
    this.navToDetail = function(){
        var path = 'estate/property/'+this.property.slug + '/';
        window.location = path;
    }
}]);


/**
 * propertyPaletteComponent
 * @name property palette
 * @type {Component}
 * @desc component that is a thumbnail for each individual place
 */
app.component('propertySummary',{
        templateUrl: '/static/place/templates/place_property-summary.component.html',
        controller : 'PropertySummaryController',
        bindings:{
            property:'=place',
            showDetail: '&',
        },

    }
);


/**
 * PropertyPaletteController
 * @name property list controller
 * @type {Controller}
 * @desc controller for the property palette component
 */
app.controller('PropertySummaryController', [function(){
    this.$onInit = function(){
    }
}]);


function Utils(){}


Utils.prototype.valuesToArray = function(collection, key){
    var _results = [];
    collection.forEach(function(value, index){
        if(typeof value == 'object' && !Array.isArray(value)){
            var keys = Object.keys(value);
            if(keys.indexOf(key) != -1){
                _results.push(value[key]);
            }
        }
    });
    return _results;
}

app.service('utils',[Utils])
